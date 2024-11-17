import React, { useState } from "react";
import { Connection, PublicKey } from "@solana/web3.js";
import axios from "axios";

const App = () => {
  const [walletAddress, setWalletAddress] = useState("");
  const [balance, setBalance] = useState(null);
  const [analysis, setAnalysis] = useState([]);
  const [newActivity, setNewActivity] = useState({
    nftTrades: 0,
    tokenHoldings: 0,
    transactions: 0,
  });

  const connection = new Connection("https://api.mainnet-beta.solana.com");

  // Handle wallet connection
  const handleWalletConnect = async () => {
    const provider = window.solflare; // Requires Solflare Wallet Extension
    if (!provider) {
      alert("Solflare Wallet is not installed.");
      return;
    }

    try {
      await provider.connect();
      setWalletAddress(provider.publicKey.toString());
    } catch (err) {
      console.error("Error connecting wallet:", err);
    }
  };

  // Fetch wallet balance
  const fetchBalance = async () => {
    try {
      const publicKey = new PublicKey(walletAddress);
      const balance = await connection.getBalance(publicKey);
      setBalance(balance / 1e9); // Convert lamports to SOL
    } catch (err) {
      console.error("Error fetching balance:", err);
    }
  };

  // Fetch wallet analysis from backend
  const fetchAnalysis = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/wallet/analyze");
      setAnalysis(response.data.analysis);
    } catch (err) {
      console.error("Error fetching analysis:", err);
    }
  };

  // Add new wallet activity
  const addActivity = async () => {
    try {
      await axios.post("http://127.0.0.1:8000/wallet/add_activity", {
        address: walletAddress,
        nft_trades: newActivity.nftTrades,
        token_holdings: newActivity.tokenHoldings,
        transactions: newActivity.transactions,
      });
      alert("Activity added successfully!");
    } catch (err) {
      console.error("Error adding activity:", err);
    }
  };

  return (
    <div>
      <h1>Solana Wallet Profiler</h1>
      {!walletAddress ? (
        <button onClick={handleWalletConnect}>Connect Wallet</button>
      ) : (
        <div>
          <p>Wallet Address: {walletAddress}</p>
          <button onClick={fetchBalance}>Get Balance</button>
          {balance !== null && <p>Balance: {balance} SOL</p>}

          <h2>Analyze Wallet</h2>
          <button onClick={fetchAnalysis}>Fetch Analysis</button>
          {analysis.length > 0 && (
            <div>
              {analysis.map((entry, index) => (
                <div key={index}>
                  <p>Wallet: {entry.wallet}</p>
                  <p>Cluster: {entry.cluster}</p>
                </div>
              ))}
            </div>
          )}

          <h2>Add Activity</h2>
          <input
            type="number"
            placeholder="NFT Trades"
            value={newActivity.nftTrades}
            onChange={(e) =>
              setNewActivity({ ...newActivity, nftTrades: e.target.value })
            }
          />
          <input
            type="number"
            placeholder="Token Holdings"
            value={newActivity.tokenHoldings}
            onChange={(e) =>
              setNewActivity({ ...newActivity, tokenHoldings: e.target.value })
            }
          />
          <input
            type="number"
            placeholder="Transactions"
            value={newActivity.transactions}
            onChange={(e) =>
              setNewActivity({ ...newActivity, transactions: e.target.value })
            }
          />
          <button onClick={addActivity}>Submit Activity</button>
        </div>
      )}
    </div>
  );
};

export default App;
