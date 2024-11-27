from transformers import pipeline
def generate_use_cases(summary):
    generator = pipeline("text-generation")
    prompt = f"Generate AI use cases for a company that {summary}"
    use_cases = generator(prompt, max_length=200, num_return_sequences=3)
    return [uc['generated_text'] for uc in use_cases]
