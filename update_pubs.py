from scholarly import scholarly
import pandas as pd

def publist():
    search_query = scholarly.search_author('Flávio Codeço Coelho')
    while True:
