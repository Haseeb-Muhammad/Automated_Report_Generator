import streamlit as st
import requests

def generate_report(subject):
    webhook_url = "https://haseeb356.app.n8n.cloud/webhook/bf1e9569-527d-413c-b8e4-cb78f3d64218"
    payload = {
    "topic": subject
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Raise error if not 2xx
        print("Webhook triggered successfully!")
        response = response.json()
        print("Response:", response)  # If your n8n returns data
        return response.get("output", "No report content returned.")
    except requests.exceptions.RequestException as e:
        print("Error calling webhook:", e)

# Set page config
st.set_page_config(page_title="Report Generator", layout="centered")

# Page title
st.title("📝 Report Generator")

# ChatGPT-like interface
st.markdown("Enter a topic below and click **Generate Report**:")

# User input
topic = st.text_input("Topic", placeholder="E.g., Artificial Intelligence")

# Generate button (no backend logic added)
if st.button("Generate Report"):
    if topic:
        st.success(f"Generating report on: **{topic}**")
        report = generate_report(topic)
        st.info(report)
    else:
        st.warning("Please enter a topic.")
        
    if st.button("Send Report"):
        pass
