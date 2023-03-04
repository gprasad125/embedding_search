import os
import pinecone
import pandas as pd
import openai

from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from dotenv import find_dotenv, load_dotenv

def load_data(fp):

    files = os.listdir(fp)
    pages = [(fp + '/' + file) for file in files if '.html' in file]

    return pages

def scrape(page):
    with open(page) as s:
        soup = BeautifulSoup(s, 'html.parser')

    paragraphs = soup.find_all('p')
            
    ps = [p.text for p in paragraphs]
    marker = page.index('_html/') + 6
    sources = {p.text: page[marker:] for p in paragraphs}
    return ps, sources

def embed(text, index):

    count = 0
    batch_size = 32

    for i in tqdm(range(0, len(text), batch_size)):
        
        # set end position of batch
        i_end = min(i+batch_size, len(text))
        
        # get batch of lines and IDs
        lines_batch = text[i: i+batch_size]
        ids_batch = [str(n) for n in range(i, i_end)]
        
        # create embeddings
        res = openai.Embedding.create(input=lines_batch, engine='text-embedding-ada-002')
        embeds = [record['embedding'] for record in res['data']]
        
        # prep metadata and upsert batch
        meta = [{'text': line} for line in lines_batch]
        to_upsert = zip(ids_batch, embeds, meta)
        
        # upsert to Pinecone
        index.upsert(vectors=list(to_upsert))