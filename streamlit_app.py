import streamlit as st
import requests

# API URLs
BASE_URL = "http://127.0.0.1:8000/wallet"  # Make sure your FastAPI server is running

# Streamlit App
st.title("Solana Wallet Profiler")

# Wallet connection
wallet_address = st.text_input("Enter Solana Wallet Address:")

if wallet_address:
    # Fetch wallet balance
    if st.button("Get Wallet Balance"):
        try:
            response = requests.post(f"{BASE_URL}/balance", json={"address": wallet_address})
            balance = response.json().get("balance")
            if balance is not None:
                st.success(f"Balance: {balance} SOL")
            else:
                st.error("Error fetching balance.")
        except Exception as e:
            st.error(f"Error: {e}")

    # Wallet Analysis
    if st.button("Analyze Wallet"):
        try:
            response = requests.get(f"{BASE_URL}/analyze")
            analysis = response.json().get("analysis")
            if analysis:
                for entry in analysis:
                    st.write(f"Wallet: {entry['wallet']}, Cluster: {entry['cluster']}")
            else:
                st.error("No analysis data available.")
        except Exception as e:
            st.error(f"Error: {e}")

    # Add wallet activity
    with st.form(key="add_activity_form"):
        nft_trades = st.number_input("NFT Trades", min_value=0, value=0)
        token_holdings = st.number_input("Token Holdings", min_value=0, value=0)
        transactions = st.number_input("Transactions", min_value=0, value=0)
        submit_button = st.form_submit_button(label="Submit Activity")

        if submit_button:
            try:
                response = requests.post(f"{BASE_URL}/add_activity", json={
                    "address": wallet_address,
                    "nft_trades": nft_trades,
                    "token_holdings": token_holdings,
                    "transactions": transactions,
                })
                message = response.json().get("message")
                if message:
                    st.success(message)
                else:
                    st.error("Error adding activity.")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.warning("Please enter a wallet address to proceed.")
