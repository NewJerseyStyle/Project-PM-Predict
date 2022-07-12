import argparse
from crawler import run as download_data
from model import run as analysis_data
from magi import run as top_five_predict
from model import Engine

def main(args):
    download_data()
    if args.engine.upper() == 'NLTK':
        analysis_data(Engine.NLTK)
    elif args.engine.upper() == 'HUGGINGFACE':
        analysis_data(Engine.HUGGINGFACE)
    else:
        raise NotImplementedError
    top5 = top_five_predict()
    for p in top5:
        print(p[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='#MAGI_SYS challenge UK Politics')
    parser.add_argument('--engine', type=str,
                        default='NLTK', choices=['HUGGINGFACE', 'NLTK'],
                        help='Engine to be used in sentiment analysis')

    main(parser.parse_args())
