
import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("credit_card_fraud_model.pkl")

# App Title
st.title("💳 Credit Card Fraud Detection System")

st.write("Enter transaction details below and click Predict.")

# User Inputs
amount = st.number_input("Transaction Amount", min_value=0.0)

transaction_hour = st.slider(
    "Transaction Hour",
    min_value=0,
    max_value=23,
    value=12
)

foreign_transaction = st.selectbox(
    "Foreign Transaction",
    ["No", "Yes"]
)

location_mismatch = st.selectbox(
    "Location Mismatch",
    ["No", "Yes"]
)

device_trust_score = st.slider(
    "Device Trust Score",
    min_value=0,
    max_value=100,
    value=50
)

velocity_last_24h = st.number_input(
    "Number of Transactions in Last 24 Hours",
    min_value=0
)

cardholder_age = st.number_input(
    "Cardholder Age",
    min_value=18,
    max_value=100,
    value=30
)

st.subheader("Merchant Category")

merchant_category = st.selectbox(
    "Select Merchant Category",
    ["Electronics", "Food", "Grocery", "Travel"]
)

# Prediction Button
if st.button("Predict Fraud"):

    # One-hot encoding for merchant category
    electronics = 1 if merchant_category == "Electronics" else 0
    food = 1 if merchant_category == "Food" else 0
    grocery = 1 if merchant_category == "Grocery" else 0
    travel = 1 if merchant_category == "Travel" else 0

    input_data = pd.DataFrame({
        'amount': [amount],
        'transaction_hour': [transaction_hour],
        'foreign_transaction': [1 if foreign_transaction == "Yes" else 0],
        'location_mismatch': [1 if location_mismatch == "Yes" else 0],
        'device_trust_score': [device_trust_score],
        'velocity_last_24h': [velocity_last_24h],
        'cardholder_age': [cardholder_age],
        'merchant_category_Electronics': [electronics],
        'merchant_category_Food': [food],
        'merchant_category_Grocery': [grocery],
        'merchant_category_Travel': [travel]
    })

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error("🚨 Fraudulent Transaction Detected")
    else:
        st.success("✅ Legitimate Transaction")

    st.subheader("Input Data")
    st.dataframe(input_data)