import json
import urllib.request
import urllib.error
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

    data = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,  
        "format": "json"  
    }

    try: 
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps(data).encode("utf-8"),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            raw_text = result['response']
            return clean_and_repair_json(raw_text)

    except urllib.error.URLError:
        print("Error: Connection error. Is Ollama running? (run 'ollama serve')")
        return {}
    except Exception as e:
        print(f"Error: Unexpected error: {e}")
        return {}
