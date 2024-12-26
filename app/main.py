# app/main.py

from fastapi import FastAPI
from app.routers import auth, kyc, transaction, blockchain

app = FastAPI(title="NFT Core API")

app.include_router(auth.router)
app.include_router(kyc.router)
app.include_router(transaction.router)
app.include_router(blockchain.router)  # Now your /blockchain endpoints are live!


@app.get("/")
def root():
    return {"message": "Hello, Bro! Welcome to NFT Core API."}
