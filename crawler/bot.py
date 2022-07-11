import time
import random
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
from tinydb import TinyDB, Query

async def download_all_mps():
    db = TinyDB('db.json')
    mp_db = db.table('mps')
    if len(mp_db):
        return
    browser = await launch(headless=True)
    page = await browser.newPage()
    await stealth(page)
    await page.goto('https://members.parliament.uk/members/commons')
    continue_flag = True
    mp_link_list = []
    while continue_flag
        try:
            await page.waitForXPath('//*[@id="main-content"]/div/article/div/div/div[2]/div/div[2]/div/ul/li[7]/a')
        except:
            continue_flag = False

        await page.waitForSelector('.card-member')
        mp_list = await page.querySelectorAll('.card-member')
        for element in mp_list:
            href = await page.evaluate('(element) => element.href', element)
            mp_link_list.append(href)

        time.sleep(random.randint(4, 6))

    for url in mp_link_list:
        await page.goto(url)
        mp_name_selector = '#main-content > div.hero-banner.hero-banner-brand > div > div > div.col-md-8.col-no-spacing > h1'
        await page.waitForSelector(mp_name_selector)
        name = await page.querySelectorEval(mp_name_selector, '(element) => element.textContent')
        await page.waitForSelector('.card-contact-info')
        contact = await page.querySelector('.card-contact-info')
        contact_url = await page.evaluate('(element) => element.href', contact)
        mp_data = {'name': name, 'twitter': None}
        if 'twitter' in contact_url:
            mp_data['twitter'] = contact_url
        mp_db.insert(mp_data)
        time.sleep(random.randint(3, 9))
    await browser.close()


async def download_all_candidates():
    db = TinyDB('db.json')
    pc_db = db.table('pcs')
    if len(pc_db):
        return
    browser = await launch(headless=True)
    page = await browser.newPage()
    await stealth(page)
    await page.goto('https://www.oddschecker.com/politics/british-politics/next-prime-minister')
    await page.waitForSelector('.selTxt')
    pc_list = await page.querySelectorAll('.selTxt')
    for element in pc_list:
        name = await page.evaluate('(element) => element.href', element)
        pc_db.insert({'name': name, 'names': list(name.split()) })
    time.sleep(1)
    await browser.close()


def get_all_powers():
    power_list = ['John Gore',
                 'Peter Hargreaves',
                 'Lubov Chernukhin',
                 'Ann Rosemary Said',
                 'Lakshmi',
                 'Usha Mittal',
                 'Aquind.Ltd',
                 'Unite',
                 'Len McCluskey',
                 'Ecotricity',
                 'Harold Immanuel',
                 'Christopher Harborne',
                 'Jeremy Hosking',
                 'AML Global',
                 'Sherriff Group',
                 'Noel Hayden',
                 'Davide Serra',
                 'Julian Dunkerton']
    return power_list


async def ask_google(pname):
    db = TinyDB('db.json')
    pc_db = db.table('pcs')
    for pc in pc_db:
        browser = await launch(headless=True)
        page = await browser.newPage()
        await stealth(page)
        await page.goto('https://www.google.com/')
        # google pname + pc.name; grap all result of first 2 page
        # store data to db
        pc_db.insert({'name': name, 'names': list(name.split()) })
    # await page.screenshot({'path': 'example.png'})
    time.sleep(1)
    await browser.close()


def do_search():
    db = TinyDB('db.json')
    mp_db = db.table('mps')
    for mp in mp_db:
        asyncio.get_event_loop().run_until_complete(ask_google(mp.name))
    for name in get_all_powers():
        asyncio.get_event_loop().run_until_complete(ask_google(name))


def main():
    asyncio.get_event_loop().run_until_complete(download_all_mps())
    asyncio.get_event_loop().run_until_complete(download_all_candidates())

if __name__ == '__main__':
    main()
# C:\Users\David\AppData\Local\pyppeteer\pyppeteer\local-chromium\588429
