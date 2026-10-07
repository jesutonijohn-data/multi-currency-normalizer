import pandas as pd
import streamlit as st

st.title("💱 Multi-Currency Normalizer")
st.write("Upload a messy financial CSV file to clean and normalize amounts to USD.")

# 1. File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df)

    # 2. Define exchange rates
    exchange_rates = {
        'USD': 1.0,
        'EUR': 1.08,
        'GBP': 1.25,
        'NGN': 0.00067
    }

    # 3. Apply your cleaning function
    df['clean_amount'] = df['raw_amount'].str.replace(r'[A-Za-z$€£,]', '', regex=True)
    df['clean_amount'] = pd.to_numeric(df['clean_amount'])
    df['exchange_rate'] = df['currency_code'].map(exchange_rates).fillna(1.0)
    df['amount_in_usd'] = df['clean_amount'] * df['exchange_rate']

    st.subheader("Normalized Output")
    st.dataframe(df)

    # 4. Download button for the user
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name='normalized_financial_data.csv',
        mime='text/csv',
    )