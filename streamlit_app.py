import streamlit as st
import json
import requests
from typing import Optional
from langflow.load import upload_file

# Load secrets from Streamlit
BASE_API_URL = st.secrets["BASE_API_URL"]
LANGFLOW_ID = st.secrets["LANGFLOW_ID"]
FLOW_ID = st.secrets["FLOW_ID"]
APPLICATION_TOKEN = st.secrets["APPLICATION_TOKEN"]
ENDPOINT = st.secrets.get("ENDPOINT", "")

TWEAKS = {
  "ChatInput-CzPR1": {},
  "ChatOutput-oaH16": {},
  "ParseData-t0jSM": {},
  "File-8KMAg": {},
  "Prompt-kGaqK": {},
  "GoogleGenerativeAIModel-iJgow": {}
}

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("Langflow Chatbot")
    st.write("Ask me anything!")

    message = st.text_input("Your message:")
    endpoint = ENDPOINT or FLOW_ID

    if st.button("Send"):
        response = run_flow(
            message=message,
            endpoint=endpoint,
            tweaks=TWEAKS,
            application_token=APPLICATION_TOKEN
        )
        st.json(response)

if __name__ == "__main__":
    main()
