import requests
from app.config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, MODEL_NAME

def send_to_azure_openai(messages, model=MODEL_NAME):
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{model}/chat/completions?api-version=2024-05-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    body = {"messages": messages}
    resp = requests.post(url, headers=headers, json=body, verify=False)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]
