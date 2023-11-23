from fastapi import FastAPI
import os
from dotenv import load_dotenv


load_dotenv(".env.local")
URI_PASSWORD = os.getenv("URI_PASSWORD")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

app = FastAPI()
