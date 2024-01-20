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


def add_padding(data, padding=70):
    if len(data) >= padding:
        # truncate
        return data[:padding]
    data.extend([[0, 0, 0, 0]] * (padding - len(data)))
    return data

