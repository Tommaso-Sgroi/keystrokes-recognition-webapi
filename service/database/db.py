import json

import mysql.connector


def load_config(path):
    config = json.loads(path)
    return config


def connect_db(config):
    cnx = mysql.connector.connect(**config)
    return cnx


class KeystrokeDatabase(object):
    def __init__(self, connection):
        self.cnx = connection

    def __call__(self):
        return self.cnx.cursor()

    def insert_user(self, uid, name=''):
        pass