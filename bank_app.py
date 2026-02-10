import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import re

st.title("🏦 Bank Challan Filling System (Voice + Fraud Detection)")
st.write("Voice enabled online Streamlit app with fraud detection")

# ---------------- VOICE INPUT (BROWSER) ----------------
components.html(
"""
<button onclick="startDictation()">🎙️ Start Voice Input</button>
<p id="output"></p>

<script>
function startDictation() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function(e) {
            document.getElementById('output').innerHTML = e.results[0][0].transcript;
        };
    } else {
        alert("Speech recognition not supported");
    }
}
</script>
""",
height=150,
)

st.info("👆 Speak → copy the text → paste into fields below")

# ---------------- FORM INPUT ----------------
name = st.text_input("Name")
account = st.text_input("Account Number")
bank = st.text_input("Bank Name")
branch = st.text_input("Branch")
amount = st.number_input("Amount", min_value=0)
purpose = st.text_input("Purpose of Payment")

# ---------------- FRAUD DETECTION FUNCTION ----------------
def detect_fraud(name, account, bank, amount, purpose):
    fraud_reasons = []

    if not account.isdigit() or not (10 <= len(account) <= 16):
        fraud_reasons.append("Invalid account number")

    if amount > 100000:
        fraud_reasons.append("Amount exceeds safe limit")

    if re.search(r"\d", name):
        fraud_reasons.append("Name contains numbers")

    if len(bank) < 3:
        fraud_reasons.append("Invalid bank name")

    suspicious_words = ["illegal", "fake", "scam", "hack"]
    if any(word in purpose.lower() for word in suspicious_words):
        fraud_reasons.append("Suspicious payment purpose")

    if fraud_reasons:
        return "⚠️ Suspicious", fraud_reasons
    else:
        return "✅ Safe", []

# ---------------- SUBMIT ----------------
if st.button("Submit Challan"):
    status, reasons = detect_fraud(name, account, bank, amount, purpose)

    data = {
        "Name": name,
        "Account Number": account,
        "Bank Name": bank,
        "Branch": branch,
        "Amount": amount,
        "Purpose": purpose,
        "Transaction Status": status
    }

    df = pd.DataFrame([data])

    st.subheader("📄 Challan Details")
    st.dataframe(df)

    if status == "⚠️ Suspicious":
        st.error("🚨 Fraud Alert Detected!")
        for r in reasons:
            st.write("•", r)
    else:
        st.success("✅ Transaction is Safe")

    st.download_button(
        "⬇️ Download Challan CSV",
        df.to_csv(index=False).encode(),
        "bank_challan.csv",
        "text/csv"
    )
