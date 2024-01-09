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
        return resp

    return commit


class KeystrokeDatabase(object):
    def __init__(self, connection):
        self.cnx = connection

    def __call__(self, **args):
        return self.cnx.cursor(args)

    def close(self):
        self.cnx.close()

    def insert_user(self, uid, name=''):
        name = name if name != '' else 'user' + str(uid)
        cursor = self()
        try:
            cursor.execute('INSERT INTO user (id, name) VALUES (%s, %s)', (uid, name))
            self.cnx.commit()
        finally:
            cursor.close()

    def delete_user(self, userid):
        cursor = self()
        try:
            cursor.execute('DELETE FROM user where userid=%s', (userid,))
        finally:
            cursor.close()

    def insert_keystroke(self, uid, keystrokes):
        keystrokes = json.dumps(keystrokes, indent=-1)
        cursor = self()
        try:
            cursor.execute('INSERT INTO probe (userid, keystroke) VALUES (%s, %s)', (uid, keystrokes))
            self.cnx.commit()
        finally:
            cursor.close()

    def set_cold_start(self, cold_start: bool):
        cursor = self()
        try:
            cursor.execute('UPDATE cold_start SET has_cold_start=%s', (cold_start,))
            self.cnx.commit()
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

    def get_user_probes(self, userid):
        cursor = self()
        try:
            cursor.execute('SELECT keystrokeid, FA, FR, keystroke FROM probe where userid=%s', (userid,))
            probes = cursor.fetchall()
            return probes
        finally:
            cursor.close()

    def get_user_probe(self, userid, keystrokeId):
        cursor = self()
        try:
            cursor.execute('SELECT FA, FR, keystroke FROM probe where userid=%s and keystrokeid=%s', (userid, keystrokeId))
            probes = cursor.fetchall()
            return probes
        finally:
            cursor.close()

    def delete_user_probe(self, userid, keystrokeId):
        cursor = self()
        try:
            cursor.execute('DELETE FROM probe where userid=%s and keystrokeid=%s', (userid, keystrokeId))
        finally:
            cursor.close()

    def update_probe_rate(self, keystrokeId, rate=''):
        """
        Update probe rate
        :param keystrokeId:
        :param rate: FA, FR, GA, GR
        :return:
        """
        if rate not in ['FA', 'FR', 'GA', 'GR']:
            raise TypeError('rate must be FA, FR, GA')

        cursor = self()
        try:
            cursor.execute(f'UPDATE probe SET {rate}={rate}+1 WHERE keystrokeid=%s', (keystrokeId,))
            self.cnx.commit()
        finally:
            cursor.close()


