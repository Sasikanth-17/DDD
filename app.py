import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load the model and tokenizer
@st.cache_resource
def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"  # Automatically map to available GPU/CPU
    )
    return tokenizer, model

# Load Falcon or Mistral model (open source)
MODEL_NAME = "tiiuae/falcon-7b-instruct"  # Change to "mistralai/Mistral-7B" if preferred
tokenizer, model = load_model(MODEL_NAME)

# Define Streamlit app
st.title("Company Insights and AI Use Cases")

st.sidebar.header("Input Parameters")
company_name = st.sidebar.text_input("Enter Company Name", value="Tesla")
button = st.sidebar.button("Get Insights")

if button:
    with st.spinner(f"Generating insights for {company_name}..."):
        # Prompt templates for the tasks
        prompts = {
            "sector": f"What sector does the company {company_name} operate in?",
            "summary": f"Provide a detailed summary of the company {company_name}, including its products and focus areas.",
            "use_cases": f"What AI or GenAI use cases could improve the operations or products of the company {company_name}?",
            "resources": f"Suggest publicly available datasets or tools from Kaggle, GitHub, or Hugging Face that can help implement the AI use cases for {company_name}.",
        }

        # Generate responses for each task
        responses = {}
        for task, prompt in prompts.items():
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(
                **inputs,
                max_length=200,  # Adjust as needed
                num_return_sequences=1,
                do_sample=True,
                top_p=0.95,
                temperature=0.7,
            )
            responses[task] = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Display results
        st.subheader(f"Insights for {company_name}")
        st.write("### 1. Sector")
        st.write(responses["sector"])
        st.write("### 2. Company Summary")
        st.write(responses["summary"])
        st.write("### 3. AI/GenAI Use Cases")
        st.write(responses["use_cases"])
        st.write("### 4. Relevant Resources")
        st.write(responses["resources"])

st.sidebar.markdown("Developed with ❤️ using Falcon/Mistral")

# Disclaimer
st.markdown(
    """
    **Note**: This app uses an open-source LLM for text generation. The insights are AI-generated and may need verification.
    """
)
