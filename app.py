import openagi
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Falcon or Mistral model
@st.cache_resource
def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"  # Automatically map to available GPU/CPU
    )
    return tokenizer, model

# Use OpenAGI to define the agents
class ResearchAgent(openagi.Agent):
    def __init__(self, model_name="tiiuae/falcon-7b-instruct"):
        super().__init__(name="Research Agent")
        self.tokenizer, self.model = load_model(model_name)
        
    def execute(self, company_name):
        prompt = f"What sector does the company {company_name} operate in?"
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_length=200,
            num_return_sequences=1,
            do_sample=True,
            top_p=0.95,
            temperature=0.7,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


class UseCaseAgent(openagi.Agent):
    def __init__(self, model_name="tiiuae/falcon-7b-instruct"):
        super().__init__(name="Use Case Agent")
        self.tokenizer, self.model = load_model(model_name)
        
    def execute(self, company_name):
        prompt = f"What AI or GenAI use cases could improve the operations or products of the company {company_name}?"
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_length=200,
            num_return_sequences=1,
            do_sample=True,
            top_p=0.95,
            temperature=0.7,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


class ResourceAgent(openagi.Agent):
    def __init__(self, model_name="tiiuae/falcon-7b-instruct"):
        super().__init__(name="Resource Agent")
        self.tokenizer, self.model = load_model(model_name)
        
    def execute(self, company_name):
        prompt = f"Suggest publicly available datasets or tools from Kaggle, GitHub, or Hugging Face that can help implement the AI use cases for {company_name}."
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_length=200,
            num_return_sequences=1,
            do_sample=True,
            top_p=0.95,
            temperature=0.7,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


# Instantiate agents
research_agent = ResearchAgent()
usecase_agent = UseCaseAgent()
resource_agent = ResourceAgent()

# Streamlit UI
st.title("Company Insights and AI Use Cases")

st.sidebar.header("Input Parameters")
company_name = st.sidebar.text_input("Enter Company Name", value="Tesla")
button = st.sidebar.button("Get Insights")

if button:
    with st.spinner(f"Generating insights for {company_name}..."):
        # Get insights from agents
        sector_response = research_agent.execute(company_name)
        use_cases_response = usecase_agent.execute(company_name)
        resources_response = resource_agent.execute(company_name)

        # Display results
        st.subheader(f"Insights for {company_name}")
        st.write("### 1. Sector")
        st.write(sector_response)
        st.write("### 2. AI/GenAI Use Cases")
        st.write(use_cases_response)
        st.write("### 3. Relevant Resources")
        st.write(resources_response)

st.sidebar.markdown("Developed with ❤️ using Falcon/Mistral and OpenAGI")

# Disclaimer
st.markdown(
    """
    **Note**: This app uses an open-source LLM for text generation. The insights are AI-generated and may need verification.
    """
)
