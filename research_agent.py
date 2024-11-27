# research_agent.py
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import pipeline

nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def fetch_company_summary(company_name):
    url = f"https://www.google.com/search?q={company_name}+about"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    about_text = ""
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        about_text += g.text + " "
    
    summary = summarize_text(about_text)
    return summary
