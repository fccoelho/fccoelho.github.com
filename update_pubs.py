"""Monthly update of the publications list on the personal website.

Fetches the publication list from OpenAlex (open scholarly graph API),
merges it with the local cache (pubs.pkl), and regenerates:
  - refs.bib   (BibTeX file, written via pybtex)
  - pubs.md    (plain formatted list, repo root)
  - content/page/publications.md     (EN page, frontmatter preserved)
  - content/page/publications.pt.md  (PT page, frontmatter preserved)

Notes
-----
Originally this script scraped Google Scholar via the `scholarly` package,
which broke due to Scholar's bot blocking. OpenAlex is now the source of
truth. Works from all known OpenAlex author profiles for Flávio are merged
(dedupe by fuzzy title match) so profile fragmentation does not lose works.
"""
import os
import pickle
import re
from difflib import SequenceMatcher

import pybtex
import requests
from pybtex.database import BibliographyData, Entry

CACHE = 'pubs.pkl'
CONTENT_PAGES = [
    ('content/page/publications.md', '## Publication list'),
    ('content/page/publications.pt.md', '## Lista de Publicações'),
]
OPENALEX = 'https://api.openalex.org/works'
MAILTO = 'fccoelho@gmail.com'
# All OpenAlex author profiles for Flávio Codeço Coelho (main + fragmented).
# Do NOT add the Zenodo-only profiles (AlertaDengue software releases).
AUTHOR_IDS = [
    'A5006736248',  # main: ENSP/Fiocruz + FGV, ORCID 0000-0003-3868-4391
    'A5102747530',  # fragmented: FGV
]
EXCLUDED_TYPES = {'erratum', 'paratext', 'editorial', 'software', 'dataset'}
EXCLUDED_VENUES = ('zenodo',)
# Works wrongly attributed to Flávio by OpenAlex authorship disambiguation.
FALSE_POSITIVE_TITLES = {
    'towed array geometry estimation during ship’s maneuvering',
    # Confirmed by Flávio (21/09/2026) as misattributed by OpenAlex
    'stereological estimation of mean nuclear volume as prognostic factor in canine subcutaneous mast cell tumours',
    # OpenAlex duplicate of the JMIR 2023 EpigraphHub paper (without subtitle)
    'a platform for data-centric, continuous epidemiological analyses',
    # Version-variants of papers already on the list (journal versions kept):
    'srag por covid-19 no brasil: descrição e comparação de características demográficas e comorbidades com srag por influenza e com a população geral',
    'assessing the potential impact of covid-19 in brazil: mobility, morbidity and the burden on the health care system',
    'machine-learning forecasting for dengue epidemics - comparing lstm, random forest and lasso regression',
}


def norm_title(title):
    return ' '.join(title.lower().split())


def similar(t1, t2, threshold=0.90):
    return SequenceMatcher(None, t1, t2).ratio() >= threshold


def fetch_openalex_works():
    """Return all OpenAlex works authored by any of AUTHOR_IDS."""
    works = {}
    cursor = '*'
    while cursor:
        resp = requests.get(
            OPENALEX,
            params={
                'filter': f"author.id:{'|'.join(AUTHOR_IDS)}",
                'per-page': 200,
                'cursor': cursor,
                'sort': 'publication_date:desc',
                'mailto': MAILTO,
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        for w in data.get('results', []):
            works[w['id']] = w
        cursor = data.get('meta', {}).get('next_cursor')
    return list(works.values())


def work_to_bib(work):
    """Map an OpenAlex work record to the bib-dict schema used by refs.bib."""
    biblio = work.get('biblio') or {}
    source = ((work.get('primary_location') or {}).get('source') or {})
    venue = source.get('display_name') or ''
    authors = [
        a['author']['display_name'].strip()
        for a in work.get('authorships', [])
        if a.get('author', {}).get('display_name', '').strip()
    ]
    if not authors:
        authors = ['Flávio Codeço Coelho']
    if len(authors) == 1:
        author_str = authors[0]
    else:
        author_str = ' and '.join(authors)

    first, last = biblio.get('first_page'), biblio.get('last_page')
    pages = f'{first}--{last}' if first and last and first != last else (first or '')

    return {
        'title': work.get('display_name', ''),
        'author': author_str,
        'pub_year': work.get('publication_year'),
        'journal': venue,
        'volume': biblio.get('volume') or '',
        'number': biblio.get('issue') or '',
        'pages': pages,
    }


def load_cache():
    if os.path.exists(CACHE):
        try:
            with open(CACHE, 'rb') as f:
                cached = pickle.load(f)
            if isinstance(cached, list) and cached:
                return cached
        except Exception as e:
            print(f'warning: could not load {CACHE}: {e}')
    return []


def fetch_publications():
    """Return (pubs, new_pubs): merged list sorted by year desc, and the newly added ones."""
    cache = load_cache()
    cached_titles = [norm_title(p.get('bib', {}).get('title', '')) for p in cache]
    pubs = list(cache)
    new_pubs = []

    for work in fetch_openalex_works():
        if work.get('type') in EXCLUDED_TYPES:
            continue
        source = ((work.get('primary_location') or {}).get('source') or {})
        if (source.get('display_name') or '').strip().lower().startswith(EXCLUDED_VENUES):
            continue
        bib = work_to_bib(work)
        if not bib['title'] or not bib['journal']:
            continue
        title = norm_title(bib['title'])
        if title in FALSE_POSITIVE_TITLES:
            continue
        if any(similar(title, t) for t in cached_titles):
            continue
        cached_titles.append(title)
        pubs.append({'bib': bib, 'id': work.get('id')})
        new_pubs.append(pubs[-1])
        print(f'new: {bib["title"]} ({bib["pub_year"]})')

    def year_key(p):
        try:
            return int(p.get('bib', {}).get('pub_year', 0))
        except (TypeError, ValueError):
            return 0

    pubs.sort(key=year_key, reverse=True)
    with open(CACHE, 'wb') as f:
        pickle.dump(pubs, f)
    return pubs, new_pubs


def sanitize_name(name):
    """Make a person name parseable by pybtex (at most one comma)."""
    name = name.strip().rstrip(',').strip()
    if name.count(',') > 1:
        parts = [p.strip() for p in name.split(',') if p.strip()]
        name = f'{parts[0]}, {" ".join(parts[1:])}'
    return name


def author_names(raw):
    """Split an author string into pybtex-parseable person names.

    Handles both the legacy display style "A, B, C, and D" and the BibTeX
    style "A and B and C" used by work_to_bib.
    """
    raw = raw.strip()
    if ', and ' in raw or (raw.count(' and ') == 1 and ',' in raw):
        parts = re.split(r',\s*and\s+|,\s*', raw)
    else:
        parts = raw.split(' and ')
    return [sanitize_name(p) for p in parts if p.strip()]


def save_bib(pubs):
    """Write refs.bib from publication dicts (journal-bearing entries only)."""
    def year_of(b):
        try:
            return int(b.get('pub_year', 0))
        except (TypeError, ValueError):
            return 0

    refs = [p['bib'] for p in pubs if p.get('bib', {}).get('pub_year')]
    refs.sort(key=year_of, reverse=True)

    bibdata = BibliographyData()
    for i, ref in enumerate(refs):
        if 'journal' not in ref or not ref['journal']:
            continue
        fields = {'author': ' and '.join(author_names(ref.get('author', '')))}
        for key in ('title', 'journal', 'volume', 'number', 'pages'):
            if ref.get(key):
                fields[key] = str(ref[key])
        fields['year'] = str(ref['pub_year'])
        bibdata.add_entry(f'ref{i}', Entry('article', fields=fields))
    bibdata.to_file('refs.bib')


def gen_ref_list():
    # Lenient mode: log name-parsing problems instead of crashing the update.
    pybtex.errors.set_strict_mode(False)
    md = pybtex.format_from_file('refs.bib', style='unsrt', output_backend='markdown')
    # Match the site's established "1. " ordered-list numbering.
    md = re.sub(r'\[(\d+)\]', r'\1. ', md)
    with open('pubs.md', 'w') as pubfile:
        pubfile.write(md)
    return md


def update_pages(pub_md):
    """Splice the formatted list into the Hugo pages, preserving frontmatter."""
    body = pub_md.strip() + '\n'
    for path, heading in CONTENT_PAGES:
        with open(path) as f:
            text = f.read()
        idx = text.find(heading)
        if idx == -1:
            print(f'warning: heading "{heading}" not found in {path}; skipped')
            continue
        cut = idx + len(heading)
        with open(path, 'w') as f:
            f.write(text[:cut] + '\n\n' + body)


if __name__ == '__main__':
    pubs, new_pubs = fetch_publications()
    save_bib(pubs)
    md = gen_ref_list()
    update_pages(md)
    print(f'Total publications: {len(pubs)} | new since last update: {len(new_pubs)}')
