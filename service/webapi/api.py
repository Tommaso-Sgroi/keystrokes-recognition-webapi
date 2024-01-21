import http.client
import json

from fastapi import FastAPI, HTTPException, Request
from .classes import *
from .utility import load_db, load_model_config, add_padding
from fastapi.middleware.cors import CORSMiddleware
from service.keystroke_recognition.model import load_model, KeystrokeRecognitionModel
from os import sep as separator
import numpy as np

config_path = f".{separator}config.json"
keystroke_database = load_db(path=config_path)
keystroke_model = KeystrokeRecognitionModel(config_path)
print(keystroke_model.summary())
PADDING = 70


def set_config_path(_config_path):
    global config_path
    config_path = _config_path


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for returning all responses as JSON
@app.middleware("http")
async def set_response_content_type(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Type"] = "application/json"
    return response


@app.get('/users/')
async def get_users(_: Request):
    id_name_list = keystroke_database.get_all_users()
    users = [User(_id, name) for _id, name in id_name_list]
    return users


@app.post("/user/")
async def create_user(r: Request):
    data = await r.body()
    data = json.loads(data)
    userid = keystroke_database.insert_new_user(data['nickname'])
    for keystroke in data['keystrokes']:
        # can be optimized using a single query
        keystroke = add_padding(keystroke, PADDING)
        keystroke_database.insert_keystroke(userid, keystroke)

    return userid


@app.post("/users/{userid}/claim/")
async def claim_phrase(userid: int, r: Request):
    data = await r.body()
    keystroke = json.loads(data)

    for i in range(len(keystroke)):
        keystroke[i] = add_padding(keystroke[i], PADDING)

    keystroke = keystroke[-1]

    # check user existence
    if not keystroke_database.user_exists(userid):
        raise HTTPException(status_code=404, detail="user does not exist")

    # make prediction
    print(userid, keystroke)
    claiming_probes = keystroke_database.get_user_probes(userid)

    # passed, likelihood = passed.tolist(), likelihood.tolist()
    predictions = []
    try:
        for probe in claiming_probes:
            probe = add_padding(probe, PADDING)
            _, likelihood = keystroke_model.predict(keystroke, probe)
            predictions.append(float(np.sum(likelihood)))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=http.client.BAD_REQUEST)

    # likelihood = sum(predictions) / len(predictions)
    likelihood = max(predictions)
    passed = bool(likelihood >= keystroke_model.threshold)
    # add padding or truncate

    claim_result = PredictionResponse(likelihood=likelihood, prediction=passed)
    # claim_result = list(claim_result.items())
    return claim_result
 