
# app.py
import streamlit as st
from resources_fetcher import fetch_company_data
from research_agent import fetch_company_summary
from use_case_suggestor import generate_use_cases

st.title("Company Research and AI Use Case Generator")

company_name = st.text_input("Enter the company name:")

if st.button("Fetch Information"):
    if company_name:
        with st.spinner("Fetching data..."):
            company_data = fetch_company_data(company_name)
            st.subheader("Company Information")
            st.write(company_data)
            
            with st.spinner("Generating summary..."):
                summary = fetch_company_summary(company_name)
                st.subheader("Company Summary")
                st.write(summary)
                
                with st.spinner("Generating use cases..."):
                    use_cases = generate_use_cases(summary)
                    st.subheader("AI Use Cases")
                    for i, use_case in enumerate(use_cases):
                        st.write(f"Use Case {i + 1 }: { use_case }")
    else:
        st.warning("Please enter a company name.")
