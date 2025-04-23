import openai
import os

def process_constraint(constraint_text: str) -> dict:
    """ 
    Uses OpenAI's ChatGPT API to convert free-text constraints into structured data.
    """

    prompt = f"""
    Convert the following employee work constraint into a structured format:
    Constraint: "{constraint_text}"
    
    Return a structured JSON format with:
    - available_days (list)
    - unavailable_days (list)
    - preferred_shifts (Morning, Afternoon, Night)
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    structured_data = response.choices[0].message.content

    return eval(structured_data)  # Convert string JSON to dictionary
