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
AIRTABLE_ENDPOINT = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}"
}

api = Api(AIRTABLE_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)
records = table.all()
local_emails=[]

emails = []

for record in records:
    emails.append(record["fields"]["Email"])

def delete_records(email):
    record_ids = []
    for record in records:
        if record["fields"]["Email"] == email:
            record_ids.append(record["id"])
        print(record["fields"]["Email"])
    for record_id in record_ids:
        url = f"{AIRTABLE_ENDPOINT}/{record_id}"
        response = requests.delete(url, headers=HEADERS)
        if response.status_code == 200:
            print(f"✅ Deleted record ID: {record_id}")
        else:
            print(f"❌ Failed to delete record ID: {record_id}, Error: {response.text}")
def add_email_to_airtable(email):
    if email not in emails:
        table.create({"Email": email})
    else:
        print("already present")
        pass

st.set_page_config(page_title="Email Manager", layout="centered")
st.title("📧 Email List Manager")

with st.form("email_form", clear_on_submit=True):
    new_email = st.text_input("Add new email")
    submitted = st.form_submit_button("Add")
    if submitted and new_email:
        # print(f"{st.session_emails=}")
        if new_email not in emails:
            success = add_email_to_airtable(new_email)
            emails.append(new_email)
            st.success(f"Added to Airtable: {new_email}")
        else:
            st.warning("This email is already in the list.")

st.subheader("Current Session Email List")
count=0
if emails:
    print(f"{emails=}")
    for email in emails:
        col1, col2 = st.columns([0.85, 0.15])
        col1.write(email)
        count +=1
        if col2.button("❌", key=count):
            emails.remove(email)
            delete_records(email)
            st.rerun()
else:
    st.info("No emails in the list yet.")

