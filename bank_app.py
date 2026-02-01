import streamlit as st
import pandas as pd
import numpy as np

# ML
from sklearn.linear_model import LogisticRegression

# Speech
import speech_recognition as sr

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Bank Account Management", layout="centered")

st.title("🏦 Bank Account Management System")
st.caption("ML Fraud Detection + Speech Based Application Form")

# -------------------- SPEECH FUNCTION --------------------
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return "Speech not recognized"

# -------------------- SIDEBAR --------------------
menu = st.sidebar.selectbox(
    "Select Option",
    ["Account Application", "Transaction", "Admin – Fraud Detection"]
)

# -------------------- ACCOUNT APPLICATION --------------------
if menu == "Account Application":
    st.subheader("📝 Bank Account Application Form")

    if st.button("🎤 Fill Name Using Voice"):
        name = speech_to_text()
        st.session_state["name"] = name

    name = st.text_input("Full Name", st.session_state.get("name", ""))

    if st.button("🎤 Fill Mobile Using Voice"):
        mobile = speech_to_text()
        st.session_state["mobile"] = mobile

    mobile = st.text_input("Mobile Number", st.session_state.get("mobile", ""))

    if st.button("🎤 Fill Address Using Voice"):
        address = speech_to_text()
        st.session_state["address"] = address

    address = st.text_area("Address", st.session_state.get("address", ""))

    account_type = st.selectbox("Account Type", ["Savings", "Current"])
    deposit = st.number_input("Initial Deposit Amount", min_value=500)

    if st.button("Submit Application"):
        st.success("✅ Account Application Submitted Successfully!")
        st.write("### Application Details")
        st.write("Name:", name)
        st.write("Mobile:", mobile)
        st.write("Address:", address)
        st.write("Account Type:", account_type)
        st.write("Deposit Amount:", deposit)

# -------------------- TRANSACTION PAGE --------------------
elif menu == "Transaction":
    st.subheader("💸 Make a Transaction")

    amount = st.number_input("Transaction Amount", min_value=1)
    transaction_time = st.slider("Transaction Time (Hour)", 0, 23, 12)
    location = st.selectbox("Transaction Location", ["Home City", "Other City", "International"])
    frequency = st.slider("Transactions Today", 1, 20, 1)

    if st.button("Submit Transaction"):
        st.success("💰 Transaction Submitted")
        st.write("Amount:", amount)
        st.write("Time:", transaction_time)
        st.write("Location:", location)
        st.write("Frequency:", frequency)

# -------------------- FRAUD DETECTION (ADMIN) --------------------
elif menu == "Admin – Fraud Detection":
    st.subheader("🚨 Fraud Detection Dashboard")

    # Dummy training data
    X = np.array([
        [100, 10, 0, 1],
        [5000, 2, 2, 10],
        [200, 14, 0, 2],
        [10000, 1, 2, 15],
        [300, 11, 1, 1]
    ])

    y = np.array([0, 1, 0, 1, 0])  # 0 = Normal, 1 = Fraud

    model = LogisticRegression()
    model.fit(X, y)

    st.write("### Test a Transaction")

    amt = st.number_input("Amount", min_value=1)
    time = st.slider("Hour", 0, 23, 12)
    loc = st.selectbox("Location Code", ["0 - Home", "1 - Other City", "2 - International"])
    freq = st.slider("Transaction Frequency", 1, 20, 1)

    loc_code = int(loc[0])

    if st.button("Check Fraud"):
        input_data = np.array([[amt, time, loc_code, freq]])
        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.error("🚨 FRAUD DETECTED! Transaction Blocked")
        else:
            st.success("✅ Transaction is SAFE")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("AI Powered Banking System | Streamlit + ML + Speech Recognition")
