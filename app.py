import streamlit as st

from dotenv import load_dotenv, find_dotenv

from src.create_embeddings import *
from src.load_index import *
from src.response import * 

load_dotenv(find_dotenv())

@st.cache_resource
def run():
    backend_path = 'data/backend_html'
    frontend_path = 'data/frontend_html'

    pages = load_data(backend_path) + load_data(frontend_path)

    text = []
    sources = dict()
    for page in pages:

        words, source = scrape(page)
        text += words
        sources.update(source)

    index = create_index()
    embed(text, index)

    return index, sources

st.write('Now loading your embeddings...')
st.write('This may take a minute...')
index, sources = run()

question = st.text_input(label = 'type your question here!', value='What is Django?')
st.write('You are asking: ' + question)

if st.button('Click to query our database!'):
    answer, sources = get_answer(question, index, sources)
    st.write(answer)

    if answer != "I don't know.":
        st.write(sources)


