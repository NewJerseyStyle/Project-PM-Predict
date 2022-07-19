# Project-PM-Predict

## Goal
Predict if johnson boris have to leave and who will become the new Prime Minister.

## Run forrest run
```bash
pip install -r request
python main.py --loop
```
Now the script will crawl information about the members of parliament in UK and some rich guys that insterested in the
next Prime Minister, and find the candidates of next Prime Minister.
Then do some AI things try to figure out who is the most popular candidate.

The script runs itself every 20 hours if `--loop` argument is added, to update its prediction.
The top 5 possible candidates are printed on screen after every prediction.

## Procudures
1. Collect contact data of members of parliament from [parliament.uk](https://members.parliament.uk/members/commons)
    > Write name & twitter URL to `TinyDB`
<!-- 2. Read Tweets of members of parliament about how they support the Prime Minister / potential candidates -->
<!--     > Write tweets to `TinyDB` -->
2. Google their name together collect texts
    > Write first 2 page search result to `TinyDB`
3. Collect names of rich people from [bbc.com](https://www.bbc.com/zhongwen/trad/uk-50713656)
    > Write name to `TinyDB`
4. Google their name together collect texts
    > Write first 2 page search result to `TinyDB`
5. Sentiment analysis and collect result by name of Prime Minister candidates
    > Read text from TinyDB and do analysis with `NLTK`/`huggingface`
6. Quantify the supportness and see what a math model predicts
    > Reuse the model from `magi-test`
7. Output the name top 5 candidates

### Add-on
- Reuse UI from `magi-test.sabie.ai`
- `Flask` app render the UI with candidate prediction
- A bot that runs itself every 20 hours predicts top 5 candidates, capture screen of `Flask` app and post the output UI to twitter

## Technology
To simplify the tech stack...
- `TinyDB` will be used for data storage/share during the crawling and prediction.
- `pyppeteer` & `pyppeteer_stealth` will be used for crawling, Googling and posting tweets
- `NLTK` & `huggingface` will be used for sentiment analysis
