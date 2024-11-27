# resources_fetcher.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_company_info(company_name):
    url = f"https://www.google.com/search?q={company_name}+sector"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    sector = None
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        if 'sector' in g.text.lower():
            sector = g.text
            break
    
    return sector

def fetch_company_data(company_name):
    sector = fetch_company_info(company_name)
    return {
        "company_name": company_name,
        "sector": sector
    }
