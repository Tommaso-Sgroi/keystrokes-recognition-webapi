def load_db(path='./config.json'):
    from ..database.db import connect_db, load_config, KeystrokeDatabase

    config = load_config(path)
    connection = connect_db(config)

    return KeystrokeDatabase(connection)


def load_config(path='./config.json'):
    from json import load as load_config_json
    with open(path, 'r') as file:
        config = load_config_json(file, parse_constant=True)['API']
        return config

def load_model_config(path='./config.json'):
    from json import load as load_config_json
    with open(path, 'r') as file:
        config = load_config_json(file, parse_constant=True)['model']
        return config
