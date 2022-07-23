# Project-PM-Predict

## Goal
Predict if johnson boris have to leave and who will become the new Prime Minister.

> ⚠️ Crawling data from Internet takes forever 👼 (~3 days) Patch it or just wait...

## Run forrest run
```bash
git clone https://github.com/NewJerseyStyle/Project-PM-Predict.git
cd Project-PM-Predict
pip install -r requirements.txt
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

> Data passed though TinyDB 👼 (Just in case are confused because not seeing variable passing but a lot of DB R/W)

### Add-on
- Reuse UI from `magi-test.sabie.ai`
- `Html2Image` render the HTML UI of candidate prediction
- A bot that keeps itself running and predicts top 5 candidates
- Post the `Html2Image` rendered image with caption (the top 1 candidate) to twitter

## Technology
To simplify the tech stack...
- `TinyDB` will be used for data storage/share during the crawling and prediction.
- `pyppeteer` & `pyppeteer_stealth` will be used for crawling, Googling and posting tweets
- `NLTK` & `huggingface` will be used for sentiment analysis
- `Html2Image` render the MAGI SYS style output predict candidate is popular or not

## Troubleshoot
### Runtime error
```bash
# Some information including the path pyppeteer saved the chromium
# some tracings...
...
pyppeteer.errors.BrowserError: Browser closed unexpectedly:
```
If you have not installed Chrome on the machine before, and it is a Debian family machine.
You need to install the dependencies of Chome.
That is complicated and I do not worry of installing too many useless things (I used container).
I install Chrome-stable at once. [refer to solution on StackOverflow](https://stackoverflow.com/questions/57217924/pyppeteer-errors-browsererror-browser-closed-unexpectedly)
```bash
sudo apt install wget
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update 
sudo apt install google-chrome-stable
```

Now check the dependencies again...
```bash
ldd ~/.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome | grep 'not found'
```
The path of `local-chromium` was printed first time you run pyppeteer (and saw the error message)

And I got
```bash
libXss.so.1 => not found
```

Then fix it with
```bash
apt install libxss1
```

### Crawling takes more than two days
With Google search rate limit this cannot be resolved.
Using VPN / Proxies may help. You can fork and patch.

A solution can be sharing a database server with many crawling workers.
- A timestamp should be added to each set of crawled data.
- For each worker connected to the database server, will check if any data lifetime longer than 20 hours.
- For any data older than 20 hours, worker will have to crawl on Internet to update that set of data.
- If all data lifetime within 24 hours, prediction shall be made at once.
