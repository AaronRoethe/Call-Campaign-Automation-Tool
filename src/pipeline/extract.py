import pandas as pd

def file(cfg):
    return pd.read_csv(cfg)

def sql(config):
    pass

def api(config):
    pass

options = {
    "file":file,
    "sql":sql,
    "api":api
}

def get(config):
    action = options[config['extract']["type"]]
    return action(config['extract']['location'])
