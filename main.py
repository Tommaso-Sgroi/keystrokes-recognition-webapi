from os import sep as separator

from service.database.db import KeystrokeDatabase


def load_db(path='./config.json'):
    from service.database.db import connect_db, load_config

    config = load_config(path)
    connection = connect_db(config)

    return KeystrokeDatabase(connection)


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
        ks.insert_keystroke(uid, keystrokes)  # insert keystroke in DB
        pass


if __name__ == '__main__':
    ksdb = load_db()
    try:
        if ksdb.is_cold_start():
            populate_database(ksdb)
            ksdb.set_cold_start(False)
    finally:
        ksdb.close()

