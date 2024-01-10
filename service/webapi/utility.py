def load_db(path='./config.json'):
    from service.database.db import connect_db, load_config, KeystrokeDatabase

    config = load_config(path)
    connection = connect_db(config)

    return KeystrokeDatabase(connection)
