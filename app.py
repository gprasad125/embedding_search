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
    for page in pages:

        text += scrape(page)

    index = create_index()
    embed(text, index)

    return index

st.write('Now loading your embeddings...')
st.write('This may take a minute...')
index = run()

question = st.text_input(label = 'type your question here!', value='what is Django?')
st.write('You are asking: ' + question)

if st.button('Click to query our database!'):
    answer = get_answer(question, index)
    st.write(answer)


