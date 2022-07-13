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
        pc_db.insert({'name': name, 'names': list(name.split()) + [name] })
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
    at_db = db.table('articles')
    User = Query()
    for pc in pc_db:
        at_db_list = []
        if at_db.get((User.name == pname) & (User.pc == pc.name)):
            at_db_list = at_db.get(User.name == pname)['texts']
        for name in pc.names:
            browser = await launch(headless=True)
            page = await browser.newPage()
            await stealth(page)
            # google pname + pc.name
            await page.goto('https://www.google.com/')
            await page.waitForXPath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
            element = await page.xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
            await page.evaluate('el => el.value = "{pname} {name}"', element)
            await page.keyboard.press('Enter')
            # grap all result of first 2 page
            for _ in range(2):
                await page.waitForSelector('.g')
                article_list = await page.querySelectorAll('.g')
                for element in article_list:
                    article = await page.evaluate('(element) => element.classList.length > 1 ? "" : element.innerText', element)
                    at_db_list.append(at_db_list)
                element = await page.querySelector('a#pnnext')
                await page.evaluate('(element) => element.click()', element)
            time.sleep(1)
            await browser.close()
        # store data to db
        at_db.upsert({'name': pname, 'pc': pc.name, 'texts': at_db_list}, , (User.name == pname) & (User.pc == pc.name))


def do_search():
    db = TinyDB('db.json')
    mp_db = db.table('mps')
    for mp in mp_db:
        asyncio.get_event_loop().run_until_complete(ask_google(mp.name))
    for name in get_all_powers():
        asyncio.get_event_loop().run_until_complete(ask_google(name))


def main():
    # crawl name list
    asyncio.get_event_loop().run_until_complete(download_all_mps())
    asyncio.get_event_loop().run_until_complete(download_all_candidates())
    # make sure Boris Johnson is on the list
    db = TinyDB('db.json')
    pc_db = db.table('pcs')
    name = 'Boris Johnson'
    pc_db.insert({'name': name, 'names': list(name.split()) + [name] })
    # crawl data
    do_search()

if __name__ == '__main__':
    main()
