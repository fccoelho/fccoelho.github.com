from scholarly import scholarly
import pandas as pd

def get_author():
    search_query = scholarly.search_author('Flávio Codeço Coelho')
    author = next(search_query)
    return author

def  get_pubs(author):
    pubs = []
    author = scholarly.fill(author)
    for pub in author['publications']:
        # pub = scholarly.fill(pub)
        pubs.append(pub)
    return pubs

if __name__== "__main__":
    author = get_author()
    dfpubs = pd.DataFrame(get_pubs(author))
    print (dfpubs)
    # pubs = pd.DataFrame(author.publications)
    # pubs.to_csv('publications.csv', index=False)