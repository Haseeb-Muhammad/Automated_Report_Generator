import streamlit as st
import requests
import os
import requests
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_ID")

api = Api(AIRTABLE_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)
records = table.all()
# print(f"{table=}")

def add_email_to_airtable(email):
    print(f"Adding email: {email}")
    print(f"Token: {AIRTABLE_TOKEN}")
    print(f"Base: {BASE_ID}, Table: {TABLE_NAME}")
    table.create({"Email": email})

# Initialize email list in session state
if "emails" not in st.session_state:
    st.session_state.emails = []

st.set_page_config(page_title="Email Manager", layout="centered")
st.title("📧 Email List Manager")

# Add new email
with st.form("email_form", clear_on_submit=True):
    new_email = st.text_input("Add new email", placeholder="example@email.com")
    submitted = st.form_submit_button("Add")
    if submitted and new_email:
        if new_email not in st.session_state.emails:
            success = add_email_to_airtable(new_email)
            st.session_state.emails.append(new_email)
            st.success(f"Added to Airtable: {new_email}")
        else:
            st.warning("This email is already in the list.")

# Display current emails
st.subheader("Current Session Email List")
if st.session_state.emails:
    for email in st.session_state.emails:
        col1, col2 = st.columns([0.85, 0.15])
        col1.write(email)
        if col2.button("❌", key=email):
            st.session_state.emails.remove(email)
            st.experimental_rerun()
else:
    st.info("No emails in the list yet.")

