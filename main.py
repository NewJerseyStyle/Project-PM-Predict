import time
import argparse
from datetime import datetime

from tinydb import TinyDB

from crawler import run as download_data
from model import run as analysis_data
from magi import run as top_five_predict
from addon import run as draw_magi_ui
from addon import post as tweet_n_ig
from model import Engine

def main(args):
    with TinyDB('db.json') as db:
        config = db.table('config')
        config.insert({'url': 'https://www.instagram.com/', 'user': args.ig, 'pass': args.ig_pw})
        config.insert({'url': 'https://twitter.com/i/flow/login', 'user': args.tw, 'pass': args.tw_pw})

    flag = True
    while flag:
        download_data()

        if args.engine.upper() == 'NLTK':
            analysis_data(Engine.NLTK)
        elif args.engine.upper() == 'HUGGINGFACE':
            analysis_data(Engine.HUGGINGFACE)
        else:
            raise NotImplementedError

        top5 = top_five_predict()
        print('===== Most popular candidates =====')
        for p in top5:
            print(p[0])
        print(f'===== {str(datetime.now().date())} =====')

        draw_magi_ui()

        for p in top5:
            tweet_n_ig(f'{p[0]}.png', post_delay=args.delay)

        # sleep 20 hours
        time.sleep(20*60*60)

        flag = args.loop
        if datetime.now().date() < datetime.strptime('05/09/2022', '%d/%m/%Y').date():
            flag = False

    with TinyDB('db.json') as db:
        db.drop_table('config')

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='#MAGI_SYS challenge UK Politics')
    parser.add_argument('--engine', type=str,
                        default='NLTK', choices=['HUGGINGFACE', 'NLTK'],
                        help='Engine to be used in sentiment analysis')
    parser.add_argument('--ig', help='Instagram username')
    parser.add_argument('--ig-pw', help='Instagram password')
    parser.add_argument('--tw', help='Twitter username')
    parser.add_argument('--tw-pw', help='Twitter password')
    parser.add_argument('--delay', default=1800, help='Interval in seconds between posting IG/Tweet')
    parser.add_argument('--loop', action='store_true', help='Sleep 20 hours & loop until Sep 4th 2022')

    main(parser.parse_args())
