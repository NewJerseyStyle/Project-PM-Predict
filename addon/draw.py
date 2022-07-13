from multiprocessing import Process
from flask import Flask, render_template
from pyppeteer import launch
import asyncio

async def draw():
  rs_db = db.table('ranks')
  for ds in rs_db:
    app = Flask(__name__)
    @app.route('/')
    def html():
      return render_template('index.html',
                             name=ds['name'],
                             data_melchior=ds['a'],
                             data_balthasar=ds['b'],
                             data_casper=(ds['a'] + ds['b']) / 2)
    server = Process(target=app.run) #app.run(host='127.0.0.1', port=8000)
    server.start()
    #screeen cap
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('http://127.0.0.1:8000/')
    await page.screenshot({'path': f'{ds['name']}.png'})
    await browser.close()
    server.terminate()
    server.join()


def main():
  asyncio.get_event_loop().run_until_complete(draw())
