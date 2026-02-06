import pandas as pd 
import json
import requests
import urllib.error


def get_dataset_profile(csv_path: str):

    try:
        dataset = pd.read_csv(csv_path)
    except Exception as e:
        return{"error": f"Could not read CSV: {str(e)}"}
    
    profile = {
        "rows": len(dataset),
        "columns": list(dataset.columns),
        "issues": []
    }

    missing = dataset.isnull.sum()
    for col, count in missing.items():
        if count > 0 :
            percentage = (count / len(dataset)) * 100
            profile["issues"].append({
                "column": col,
                "problem": "missing_values",
                "count": int(count),
                "severity": "high" if percentage > 20 else "medium"
            })

    dupes = dataset.duplicated().sum()
    if dupes > 0:
        profile["issues"].append({
            "problem": "duplicate_rows",
            "count": int(dupes),
            "severity": "low"
        })

    for col in dataset.select_dtypes(include=['object']):
        unique_count =dataset[col].nunique()
        if unique_count > 50 and unique_count < len(dataset):
             profile["issues"].append({
                "column": col,
                "problem": "high_cardinality",
                "unique_values": unique_count,
                "severity": "info"
            })

    return profile

def get_cleaning_advice(profile: dict):
    if not profile.get("issues"):
        return "Clean dataset. Keep training!"
    
    prompt = f"""
    You are a Senior Data Engineer. 
    Here is a profile of a dirty dataset. Provide a numbered checklist of Python cleaning steps (Pandas) to fix these specific issues.
    
    Dataset Profile:
    {json.dumps(profile, indent=2)}

    Rules:
    - Be brief and technical.
    - Suggest specific methods (e.g., "Use df.drop_duplicates()").
    - Do not write a preamble. Just the steps.
    """

    data = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/generate", 
            data=json.dumps(data).encode("utf-8"), 
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            result =json.loads(response.read().decode("utf-8"))
            return result['response']
    except Exception as e:
        return f"Model is not avaliable right now! {e}"
    