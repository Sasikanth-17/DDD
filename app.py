
# # app.py
# import streamlit as st
# from resources_fetcher import fetch_company_data
# from research_agent import fetch_company_summary
# from use_case_suggestor import generate_use_cases

# st.title("Company Research and AI Use Case Generator")

# company_name = st.text_input("Enter the company name:")

# if st.button("Fetch Information"):
#     if company_name:
#         with st.spinner("Fetching data..."):
#             company_data = fetch_company_data(company_name)
#             st.subheader("Company Information")
#             st.write(company_data)
            
#             with st.spinner("Generating summary..."):
#                 summary = fetch_company_summary(company_name)
#                 st.subheader("Company Summary")
#                 st.write(summary)
                
#                 with st.spinner("Generating use cases..."):
#                     use_cases = generate_use_cases(summary)
#                     st.subheader("AI Use Cases")
#                     for i, use_case in enumerate(use_cases):
#                         st.write(f"Use Case {i + 1 }: { use_case }")
#     else:
#         st.warning("Please enter a company name.")


import requests
from bs4 import BeautifulSoup
import streamlit as st
from transformers import pipeline
import random

# Function to fetch company information from DuckDuckGo
def fetch_company_info(company_name):
    search_url = f"https://duckduckgo.com/html/?q={company_name}+company+info"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract links (or other relevant data)
    links = soup.find_all('a', class_='result__a')
    
    # For simplicity, we return the first link (you can expand this logic to extract more data)
    return links[0]['href'] if links else "No information found"

# Research summarizer using Hugging Face summarization model (T5 or BART)
def summarize_research(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Function to suggest AI/Gen AI use cases based on industry
def suggest_use_cases(industry):
    use_cases = {
        "Healthcare": ["AI for patient diagnosis", "AI for predicting disease outbreaks", "AI-powered medical image analysis"],
        "Finance": ["AI for fraud detection", "AI for personalized financial advice", "AI-powered risk analysis"],
        "Retail": ["AI for personalized recommendations", "AI for inventory management", "AI-powered customer service chatbots"],
        "Manufacturing": ["AI for predictive maintenance", "AI for quality control", "AI-powered supply chain optimization"],
        "Automotive": ["AI for autonomous vehicles", "AI for predictive maintenance", "AI-powered traffic optimization"]
    }
    
    # Return use cases based on the industry (default to a general set if no specific match found)
    return use_cases.get(industry, ["AI for process automation", "AI for data analysis"])

# Streamlit App
def main():
    st.title("AI/Gen AI for Companies")

    # Input company name
    company_name = st.text_input("Enter the company name:")
    
    if company_name:
        # Step 1: Fetch company info (sector, research summary, etc.)
        st.subheader("Company Info")
        company_info = fetch_company_info(company_name)
        st.write(f"Company Information: {company_info}")

        # Step 2: Summarize research about the company
        # For demonstration, we use a mock text about the company. Replace with actual scraping content.
        mock_research_text = """
        Tesla is an electric vehicle and clean energy company that designs, manufactures, and sells electric vehicles, battery energy storage, and solar energy products. Tesla aims to accelerate the world's transition to sustainable energy.
        """
        research_summary = summarize_research(mock_research_text)
        st.subheader("Research Summary")
        st.write(research_summary)
        
        # Step 3: Suggest AI/Gen AI use cases
        # Based on a simple sector (for now, we use a random selection)
        industries = ["Healthcare", "Finance", "Retail", "Manufacturing", "Automotive"]
        industry = random.choice(industries)  # Random industry for demo purposes
        st.subheader(f"Suggested Use Cases for {industry} Industry")
        use_cases = suggest_use_cases(industry)
        for case in use_cases:
            st.write(f"- {case}")

if __name__ == "__main__":
    main()

