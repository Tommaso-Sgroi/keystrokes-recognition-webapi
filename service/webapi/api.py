from typing import Union

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from ..database import KeystrokeDatabase
from .utility import load_db
from fastapi.middleware.cors import CORSMiddleware

keystroke_database = load_db()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_db = {}


class Data(BaseModel):
    username: str


@app.post("/user/")
def create_user(nickname: Data):
    # Assume you generate a unique user ID and store it in the database
    user_id = len(fake_db) + 1
    fake_db[user_id] = {"id": user_id, "username": nickname}

    return {"id": user_id}


@app.get("/user/phrases/")
def get_user_phrases(
        XId: int = Header(..., description="App user id readable version ('semantic version' format)")):
    # Assume you retrieve phrases for the specified user from the database
    user_phrases = [
        {"keystrokeID": 1, "FA": 2, "FR": 1, "GA": 10, "GR": 5, "phrase": "the lazy brown fox"},
        {"keystrokeID": 2, "FA": 0, "FR": 0, "GA": 15, "GR": 3, "phrase": "do something"},
    ]

    return user_phrases


@app.get("/phrases/")
def get_all_phrases():
    # Assume you retrieve all phrases from the database
    all_phrases = [
        {"keystrokeID": 1, "FA": 2, "FR": 1, "GA": 10, "GR": 5, "phrase": "the lazy brown fox"},
        {"keystrokeID": 2, "FA": 0, "FR": 0, "GA": 15, "GR": 3, "phrase": "do something"},
        {"keystrokeID": 3, "FA": 1, "FR": 5, "GA": 8, "GR": 2, "phrase": "not my phrase"},
    ]

    return all_phrases


@app.put("/phrases/claim/{keystrokeid}")
def claim_phrase(keystrokeid: int, keystrokes: list,
                 XId: int = Header(..., description="App user id readable version ('semantic version' format)")):
    # Assume you process the claim and return a result
    claim_result = {"passed": True, "likelyhood": 0.95}

    return claim_result
