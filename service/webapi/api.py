import json

from fastapi import FastAPI, HTTPException, Request
from .classes import *
from .utility import load_db, load_model_config
from fastapi.middleware.cors import CORSMiddleware
from service.keystroke_recognition.model import load_model, KeystrokeRecognitionModel
from os import sep as separator

config_path = f".{separator}config.json"
keystroke_database = load_db(path=config_path)
keystroke_model = load_model(None)  # KeystrokeRecognitionModel(config_path)


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
        keystroke_database.insert_keystroke(userid, keystroke)

    return userid


@app.post("/users/{userid}/claim/")
async def claim_phrase(userid: int, r: Request):
    data = await r.body()
    keystroke = json.loads(data)

    # check user existence
    if not keystroke_database.user_exists(userid):
        raise HTTPException(status_code=404, detail="user does not exist")

    # make prediction
    print(userid, keystroke)
    claiming_probes = keystroke_database.get_user_probes(userid)

    # predictions = []
    # for probe in claiming_probes:
    #     probe = json.loads(probe)
    #     prediction = keystroke_model.predict(keystroke, probe)
    #     predictions.append(prediction[0])

    # likelihood = sum(predictions) / len(predictions)
    # passed = likelihood > keystroke_model.threshold
    # return prediction

    passed, likelihood = keystroke_model.predict(keystroke, probe_data=claiming_probes.pop())
    claim_result = {"passed": passed, "likelihood": likelihood}

    return claim_result
