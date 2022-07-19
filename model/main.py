from enum import Enum
from tinydb import TinyDB, Query
from . import nltk_sent
from . import deep_sent

class Engine(Enum):
    NLTK=1
    HUGGINGFACE=2

POWER_LIST = ['John Gore',
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


def main(engine=Engine.NLTK):
    assert isinstance(engine, Engine)

    with TinyDB('db.json') as db:
        pc_db = db.table('pcs')
        at_db = db.table('articles')
        ds_db = db.table('qips')
        User = Query()
        
        ds = {}
        for at in at_db:
            data = []
            for article in at['texts']:
                if at['pc'] in article or len([n for n in at['pc'] if n in article]):
                    data.append(article)
            if engine == Engine.NLTK:
                supportiveness, _, _ = nltk_sent.sentiment_analysis(data)
            elif engine == Engine.HUGGINGFACE:
                supportiveness, _, _ = deep_sent.sentiment_analysis(data)
            activeness = 100 * float(len(data)) / float(len(at['texts']))
            powerfulness = 50
            if at['name'] in POWER_LIST:
                powerfulness = 70
            if at['pc'] not in ds:
              ds[at['pc']] = {'q': at['pc'], 'i': [], 'p': [], 's': []}
            ds[at['pc']]['i'].append(powerfulness)
            ds[at['pc']]['p'].append(supportiveness)
            ds[at['pc']]['s'].append(activeness)

        for q, d in ds.items():
            ds_db.upsert(d, User.q == q)
