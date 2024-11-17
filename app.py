from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from solana.rpc.api import Client
import pandas as pd
from sklearn.cluster import KMeans
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Solana RPC Client
solana_client = Client(os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"))

# Example wallet activity data (simulated, should ideally be stored in a database)
wallet_activity_data = {
    "wallet": [],
    "nft_trades": [],
    "token_holdings": [],
    "transactions": [],
}

# Pydantic model for wallet input
class WalletInput(BaseModel):
    address: str

# Pydantic model for activity input
class WalletActivity(BaseModel):
    nft_trades: int
    token_holdings: int
    transactions: int

# Fetch wallet balance
def get_wallet_balance(wallet_address: str):
    try:
        balance = solana_client.get_balance(wallet_address)
        return balance["result"]["value"] / 1e9  # Convert lamports to SOL
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Analysis
def analyze_wallet(wallet_data):
    df = pd.DataFrame(wallet_data)
    model = KMeans(n_clusters=2, random_state=42)
    df["cluster"] = model.fit_predict(
        df[["nft_trades", "token_holdings", "transactions"]]
    )
    return df.to_dict(orient="records")

# API: Get wallet balance
@app.post("/wallet/balance")
async def wallet_balance(wallet: WalletInput):
    balance = get_wallet_balance(wallet.address)
    return {"wallet": wallet.address, "balance": balance}

# Cache for analysis result
analysis_cache = None

# API: Analyze wallet activity
@app.get("/wallet/analyze")
async def wallet_analyze():
    global analysis_cache
    if analysis_cache is None:  # Only recalculate analysis if not cached
        result = analyze_wallet(wallet_activity_data)
        analysis_cache = result
    return {"analysis": analysis_cache}

# API: Add wallet activity data (simulated)
@app.post("/wallet/add_activity")
async def add_activity(wallet: WalletInput, activity: WalletActivity):
    wallet_activity_data["wallet"].append(wallet.address)
    wallet_activity_data["nft_trades"].append(activity.nft_trades)
    wallet_activity_data["token_holdings"].append(activity.token_holdings)
    wallet_activity_data["transactions"].append(activity.transactions)
    # Clear the cache so the new data triggers a re-analysis
    global analysis_cache
    analysis_cache = None
    return {"message": "Activity added successfully."}
