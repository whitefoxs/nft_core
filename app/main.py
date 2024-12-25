from fastapi import FastAPI

app = FastAPI(title="NFT Core API")

@app.get("/")
def read_root():
    return {"message": "Hello, Bro! The API is alive and well."}
