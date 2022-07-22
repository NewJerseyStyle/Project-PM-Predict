import os
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
from tinydb import TinyDB, Query


async def ig_poster(url, u, p, filename):
  pass
#   browser = await launch(headless=True)
#   page = await browser.newPage()
#   await stealth(page)
#   # chrome goto ig, login
#   await page.setExtraHTTPHeaders({
#     'Accept-Language': 'zh'
#   });
#   await page.goto(url)
#   await page.waitForSelector('#loginForm > div > div:nth-child(1) > div > label > input')
#   await page.type('#loginForm > div > div:nth-child(1) > div > label > input', u)
#   await page.type('#loginForm > div > div:nth-child(2) > div > label > input', p)
#   element = await page.querySelector('#loginForm > div > div:nth-child(3) > button')
#   await page.evaluate('(element) => element.click()', element)
#   await asyncio.sleep(6)
#   # post with image
#   await page.waitForSelector('nav')
#   elements = await page.querySelectorAll('nav')
#   for element in elements:
#     el = await element.querySelector('button')
#     if el:
#       await page.evaluate('(element) => element.click()', el)
#       break
#   elements = await page.querySelectorAll('div[role="dialog"]')
#   basepath = os.getcwd()
#   element = await page.querySelector('input[type="file"]')
#   element.uploadFile(os.path.join(basepath, filename))
#   # too complex... lets do manual or apply for IG API
#   await asyncio.sleep(6)
#   await browser.close()

async def tw_poster(url, u, p, filename):
  browser = await launch(headless=True)
  page = await browser.newPage()
  await stealth(page)
  # chrome goto tw, login
  await page.goto(url)
  await waitForSelector('input[autocomplete="username"]')
  await page.type('input[autocomplete="username"]', u)
  element = await page.querySelectorAll('div[role="button"]')[2]
  await page.evaluate('(element) => element.click()', element)
  await waitForSelector('input[autocomplete="current-password"]')
  await page.type('input[autocomplete="current-password"]', p)
  element = await page.querySelectorAll('div[role="button"]')[2]
  await page.evaluate('(element) => element.click()', element)
  await asyncio.sleep(6)
  # post with image
  await page.goto('https://twitter.com/compose/tweet')
  await waitForSelector('div[role="textbox"]')
  await page.type('div[role="textbox"]', 'text')
  basepath = os.getcwd()
  element = await page.querySelector('input[type="file"]')
  element.uploadFile(os.path.join(basepath, filename))
  element = await page.querySelector('div[data-testid="tweetButton"]')
  await page.evaluate('(element) => element.click()', element)
  await asyncio.sleep(6)
  # clean up
  await browser.close()

def main(filename, delay):
  with TinyDB('db.json') as db:
    config = db.table('config')
    for site in config:
      if 'instagram' in site['url']:
        # read tinydb config IG user&pass
        asyncio.get_event_loop().run_until_complete(ig_poster(site['url'], site['user'], site['pass'], filename))
      if 'twitter' in site['url']:
        # read tinydb config twitter user&pass
        asyncio.get_event_loop().run_until_complete(tw_poster(site['url'], site['user'], site['pass'], filename))
      else:
        raise NotImplementedError
