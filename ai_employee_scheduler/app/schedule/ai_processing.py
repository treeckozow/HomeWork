import openai
import os

def createNewUser(user_text: str) -> dict:
    openai.api_key = os.getenv("CHATGPT_API_KEY") # "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"
    prompt = f"""
    convert the following employee information into structured data:
    user info: "{user_text}

    return a structured json dict format with:
    {
        "name": "user name",
        "email": "user email",
        "role": "user role",
        "group": "user group",
        "job": "user job"
    }
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    structured_data = response.choices[0].message.content

    return eval(structured_data)  # Convert string JSON to dictionary

def process_constraint(constraint_text: str) -> dict:
    """ 
    Uses OpenAI's ChatGPT API to convert free-text constraints into structured data.
    """
    openai.api_key = os.getenv("CHATGPT_API_KEY") # "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"

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
