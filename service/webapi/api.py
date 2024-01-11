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


# Middleware for returning all responses as JSON
@app.middleware("http")
async def set_response_content_type(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Type"] = "application/json"
    return response


@app.post("/user/")
def create_user(r: Request):
    # Assume you generate a unique user ID and store it in the database
    id = keystroke_database.insert_new_user("")
    return {"id": id}

@app.get('/users/')
def get_users():
    pass



@app.post("/users/{userid}/claim/")
def claim_phrase(keystrokeid: int, keystrokes: list,
                 XId: int = Header(..., description="App user id readable version ('semantic version' format)")):
    # Assume you process the claim and return a result
    claim_result = {"passed": True, "likelyhood": 0.95}

    return claim_result
