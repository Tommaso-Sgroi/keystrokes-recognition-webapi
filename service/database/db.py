import json
import mysql.connector


def connect_db(config):
    cnx = mysql.connector.connect(**config)
    return cnx

def load_config(path):
    import json
    with open(path, 'r') as file:
        config = json.load(file, parse_constant=True)
    return config

def _add_commit(transaction):
    def commit(self, *a, **b):
        resp = transaction(self, *a, **b)
        self.cnx.commit()
        return resp

    return commit


class KeystrokeDatabase(object):
    def __init__(self, connection):
        self.cnx = connection

    def __call__(self, **args):
        return self.cnx.cursor(args)

    def close(self):
        self.cnx.close()

    @_add_commit
    def insert_user(self, uid, name=''):
        name = name if name != '' else 'user' + str(uid)
        cursor = self()
        try:
            cursor.execute('INSERT INTO user (id, name) VALUES (%s, %s)', (uid, name))
        finally:
            cursor.close()

    @_add_commit
    def insert_keystroke(self, uid, keystrokes):
        keystrokes = json.dumps(keystrokes, indent=-1)
        cursor = self()
        try:
            cursor.execute('INSERT INTO probe (userid, keystroke) VALUES (%s, %s)', (uid, keystrokes))
        finally:
            cursor.close()

    @_add_commit
    def set_cold_start(self, cold_start: bool):
        cursor = self()
        try:
            cursor.execute('UPDATE cold_start SET has_cold_start=%s', (cold_start,))
        finally:
            cursor.close()

    def is_cold_start(self):
        cursor = self()
        try:
            cursor.execute('SELECT * FROM cold_start LIMIT 1')
            myresult = cursor.fetchone()
        finally:
            cursor.close()
        myresult = bool(*myresult)
        return myresult


