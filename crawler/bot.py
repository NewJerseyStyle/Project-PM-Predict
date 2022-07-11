import time
import random
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
from tinydb import TinyDB, Query

async def download_all_mps():
    db = TinyDB('db.json')
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
        mp_data = {'name': name}
        if 'twitter' in contact_url:
            mp_data['twitter'] = contact_url
        db.insert(mp_data)
        time.sleep(random.randint(3, 9))
    await browser.close()


async def download_all_candidates():
    db = TinyDB('db.json')
    browser = await launch(headless=True)
    page = await browser.newPage()
    await stealth(page)
    # await page.screenshot({'path': 'example.png'})
    await browser.close()

def main():
    asyncio.get_event_loop().run_until_complete(download_all_mps())

if __name__ == '__main__':
    main()
# C:\Users\David\AppData\Local\pyppeteer\pyppeteer\local-chromium\588429
