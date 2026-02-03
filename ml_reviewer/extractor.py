import json
import requests
import re


def clean_and_repair_json(text: str):
    """
    Attempts to parse JSON from LLM output, handling common errors
    like markdown blocks, single quotes, or Python-style None.
    """

    if "```" in text:
        match = re.search(r"```(?:json)?(.*?)```", text, re.DOTALL)
        if match:
            text = match.group(1)

    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        text = match.group(1)

    text = re.sub(r'\bNone\b', 'null', text)
    text = re.sub(r'\bTrue\b', 'true', text)
    text = re.sub(r'\bFalse\b', 'false', text)
    text = re.sub(r',\s*\}', '}', text)
    text = re.sub(r',\s*\]', ']', text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:

        try: 
            fixed_text = text.replace("'", '"')
            return json.loads(fixed_text)
        except:
            print(f"Parser failed.")
            return{}
        
    




def extract_ml_facts(source_code: str):
    snippet = source_code[:8000]

    prompt = f"""
    You are a strict parser. Read this Python code and extract these details into a valid JSON object:
    - model_architecture (str or null)
    - optimizer (str or null)
    - learning_rate (float or null)
    - epochs (int or null)

    Code:
    {snippet}

    Return ONLY the JSON. Do not explain.
    """


    try: 
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,  
                "format": "json"  
            },
            timeout=120 
        )

        response.raise_for_status()
        raw_text = response.json()['response']

        json_text = clean_and_repair_json(raw_text)
        facts = json_text
        return facts
    

    except requests.exceptions.ConnectionError:
        print("Error: Connection error. Is Ollama running(run 'ollama serve')")
        return{
        }
    except json.JSONDecodeError:
        print(f"Error: Model failed to generate valid JSON.\nRaw output: {raw_text[:100]}...")
        return {}
    except Exception as e:
        print(f"Error: Unexpected error: {e}")
        return {}
