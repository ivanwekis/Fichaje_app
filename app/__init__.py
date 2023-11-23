from fastapi import FastAPI
import os 
from dotenv import load_dotenv

load_dotenv(".env.local")
URI = os.getenv("URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

app = FastAPI()
