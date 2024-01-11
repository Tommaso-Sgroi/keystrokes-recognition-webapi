import json
from os import sep as separator

from service.database.db import KeystrokeDatabase
from service.webapi.api import app
from service.webapi.utility import load_db
from service.webapi.utility import load_config
import uvicorn

app = app


def populate_database(ks: KeystrokeDatabase, file=f'data{separator}ks.zip'):
    import zipfile, json
    from pathlib import Path

    def read_from_zip():
        """Read dataset from zip file"""
        uds = []
        with zipfile.ZipFile(file, mode='r') as zip_ref:
            for name in zip_ref.namelist():
                n = zip_ref.read(name)
                phrases = json.loads(n)
                uds.append((Path(name).stem, phrases))
        return uds

    id_keystrokes = read_from_zip()
    for uid, keystrokes in id_keystrokes:
        ks.insert_user(uid, '')  # insert user in DB
        for keystroke in keystrokes:
            ks.insert_keystroke(uid, keystroke)  # insert keystroke in DB
        pass


if __name__ == '__main__':
    ksdb = load_db()
    try:
        if ksdb.is_cold_start():
            populate_database(ksdb)
            ksdb.set_cold_start(False)

        probes = ksdb.update_probe_rate(1, 'FA')
        print(probes)
    finally:
        ksdb.close()
    uvicorn.run("main:app", **load_config('./config.json'))
