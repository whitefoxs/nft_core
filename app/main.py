# app/main.py

from fastapi import FastAPI
from app.routers import auth, kyc

app = FastAPI(title="NFT Core API")

# Include routers
app.include_router(auth.router)
app.include_router(kyc.router)

@app.get("/")
def root():
    return {"message": "Hello, Bro! Welcome to NFT Core API."}
