import os
from dotenv import load_dotenv

load_dotenv()

# Feel free to change "localhost" to an IP or domain if needed
DB_USER = os.getenv("DB_USER", "zhenfenghuang")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Fung24031978")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "nft_core_db")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
