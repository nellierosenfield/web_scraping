from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import requests

st.selectbox('Choose a topic', ['love', 'humor', 'life', 'books'])
