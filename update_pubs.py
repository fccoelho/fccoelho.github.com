from scholarly import scholarly
import pandas as pd
import json
import os
import datetime
from tqdm import tqdm
import pickle
from icecream import ic
import pybtex

def get_author():
    search_query = scholarly.search_author('Flávio Codeço Coelho')
    author = next(search_query)
    return author

def  get_pubs(author):
    pubs = []
    author = scholarly.fill(author)
    # ic(author)
    for pub in tqdm(author['publications']):
        pub = scholarly.fill(pub)
        pubs.append(pub)
    return pubs

def save_bib(refs):
    """
    Save bibfile
    """
    refs_sorted = sorted([r for r in refs if 'pub_year' in r], key=lambda x: x['pub_year'], reverse=True)
    if len(refs) != len(refs_sorted):
        refs_missing = [r for r in refs if r not in refs_sorted]
        print(f"Missing {len(refs_missing)} references in pub list, due to missing pub_year field. Adding them to the end.")
        for ref in refs_missing:
            ref['pub_year'] = "--"
            refs_sorted.append(ref)
    with open('refs.bib', 'w') as bibfile:
        for i, ref in enumerate(tqdm(refs_sorted)):
            if 'abstract' in ref:
                del ref['abstract']
            if ('journal' not in ref):
                continue
            bibfile.write(r"@article{ref"+str(i)+", " + (str(ref)+'|')
                          .replace("'author': '","author = {")
                          .replace("'author': \"","author = {")
                          .replace("'title': '","title = {")
                          .replace("'abstract': '","abstract = {")
                          .replace("'abstract': \"","abstract = {")
                          .replace("'journal': '","journal = {")
                          .replace("'journal': \"","journal = {")
                          .replace("'volume': '","volume = {")
                          .replace("'number': '","number = {")
                          .replace("'pages': '","pages = {")
                          .replace("'publisher': '","publisher = {")
                          .replace("'pub_year': ","pub_year = {")
                          .replace("'conference': '","conference = {")
                          .replace("'citation': '","citation = {")
                          .replace("'citation': \"","citation = {")
                          .replace(", citation",'}, citation')  # to close } after pub_year
                          .replace("pub_year", "year")
                          .replace("',", '},')
                          .replace("'},", '},')
                          .replace("\",",'},')
                          .replace("'}|",'}}')
                          .replace("\"}|",'}}')[1:] + '\n')
def gen_ref_list():
    with open('pubs.md', 'w') as pubfile:
        md = pybtex.format_from_file("refs.bib",
                                     style="unsrt",
                                     # output_encoding="utf-8",
                                     output_backend="markdown")
        pubfile.write(md)



if __name__== "__main__":
    author = get_author()
    if os.path.exists('pubs.pkl'):
        fstat = os.stat('pubs.pkl')
        cdate = datetime.datetime.fromtimestamp(fstat.st_ctime)
        if cdate > datetime.datetime.now() - datetime.timedelta(days=1):
            pubs = pickle.load(open('pubs.pkl', 'rb'))
        else:
            print('Updating publication list')
            pubs = get_pubs(author)
            pickle.dump(pubs, open(f'pubs.pkl', 'wb'))
    else:
        print('Updating publication list')
        pubs = get_pubs(author)
        pickle.dump(pubs, open(f'pubs.pkl', 'wb'))
    save_bib([p['bib'] for p in pubs])
    gen_ref_list()
    dfpubs = pd.DataFrame(pubs)
    # print (dfpubs.iloc[0])
