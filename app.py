from fastapi import FastAPI
from pydantic import BaseModel
from solana.rpc.api import Client
import pandas as pd
from sklearn.cluster import KMeans

# Initialize FastAPI app
app = FastAPI()

# Solana RPC Client
solana_client = Client("https://api.mainnet-beta.solana.com")

# Example wallet activity data
wallet_activity_data = {
    "wallet": [],
    "nft_trades": [],
    "token_holdings": [],
    "transactions": [],
}

# Pydantic model for wallet input
class WalletInput(BaseModel):
    address: str

# Fetch wallet balance
def get_wallet_balance(wallet_address: str):
    try:
        balance = solana_client.get_balance(wallet_address)
        return balance["result"]["value"] / 1e9  # Convert lamports to SOL
    except Exception as e:
        return {"error": str(e)}

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

# API: Analyze wallet activity
@app.get("/wallet/analyze")
async def wallet_analyze():
    result = analyze_wallet(wallet_activity_data)
    return {"analysis": result}

# API: Add wallet activity data (simulated)
@app.post("/wallet/add_activity")
async def add_activity(wallet: WalletInput, nft_trades: int, token_holdings: int, transactions: int):
    wallet_activity_data["wallet"].append(wallet.address)
    wallet_activity_data["nft_trades"].append(nft_trades)
    wallet_activity_data["token_holdings"].append(token_holdings)
    wallet_activity_data["transactions"].append(transactions)
    return {"message": "Activity added successfully."}
