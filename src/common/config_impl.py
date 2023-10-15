import os
import yaml
import mysql.connector
from mysql.connector import Error


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            root_dir = os.path.abspath(os.path.dirname(__file__))
            config_path = os.path.join(root_dir, 'config.yaml')
            with open(config_path, 'r') as file:
                cls._instance.data = yaml.safe_load(file)
        return cls._instance

    def get(self, key, default=None):
        return self.data.get(key, default)

    def get_nested(self, key_path, default=None):
        keys = key_path.split('.')
        value = self.data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
