from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from .classes import *
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
    id = keystroke_database.insert_new_user(nickname.username)
    return {"id": id}


@app.get("/user/phrases/")
def get_user_phrases(request: Request):
    # Assume you retrieve phrases for the specified user from the database
    XId = request.headers.get('X-Id')

    user_phrases = keystroke_database.get_user_probes(int(XId))

    return [v[:-1] for v in user_phrases]


@app.get("/phrases/")
def get_all_phrases():
    class Wrapper(object):
        def __init__(self, user, probe):
            self.user = user
            self.probe = probe

    # Assume you retrieve all phrases from the database
    probes_user = keystroke_database.get_probes_with_user()
    values = []
    for probe in probes_user:
        values.append(Wrapper(User(probe[0], probe[1]), Probe(*probe[2:])))
    pass

    return values


@app.put("/phrases/claim/{keystrokeid}")
def claim_phrase(keystrokeid: int, keystrokes: list,
                 XId: int = Header(..., description="App user id readable version ('semantic version' format)")):
    # Assume you process the claim and return a result
    claim_result = {"passed": True, "likelyhood": 0.95}

    return claim_result
