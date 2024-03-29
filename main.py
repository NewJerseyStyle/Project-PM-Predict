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
    assert not( args.loop == args.dry_run and args.loop == True)

    with TinyDB('db.json') as db:
        config = db.table('config')
        config.insert({'url': 'https://twitter.com/i/flow/login', 'user': args.tw, 'pass': args.tw_pw})

    flag = True
    while flag:
        if not args.dry_run:
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
            print(p[0], f'{p[2]}%')
        print(f'===== {str(datetime.now().date())} =====')

        draw_magi_ui()

        if not args.dry_run:
            tweet_n_ig(f'{top5[0][0]}.png')

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
    parser.add_argument('--tw', help='Twitter username')
    parser.add_argument('--tw-pw', help='Twitter password')
    parser.add_argument('--loop', action='store_true',
                        help='Sleep 20 hours & loop until Sep 4th 2022')
    parser.add_argument('--dry-run', action='store_true',
                        help='No download and Tweet, predict and render image only')

    main(parser.parse_args())
