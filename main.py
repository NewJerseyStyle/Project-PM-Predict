from crawler import run as download_data
from model import run as analysis_data
from magi import run as top_five_predict
from model import Engine

def main():
    download_data()
    analysis_data()
    top5 = top_five_predict()
    for p in top5:
        print(p[0])

if __name__ == '__main__':
    main()
