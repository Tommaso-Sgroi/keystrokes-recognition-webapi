from os import sep as separator


def load_db(path='./config.json'):
    from service.database.db import load_config, connect_db

    config = load_config(path)
    connection = connect_db(config)

    return connection


def populate_database(file=f'data{separator}ks.zip'):
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
        pass

if __name__ == '__main__':
    cnx = load_db()
