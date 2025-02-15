import os

from dependency_injector import providers


def read_config():
    if 'ENV' in os.environ:
        env = os.environ['ENV']
    else:
        env = 'development'

    config_file = f'config.{env}.ini'
    config_file_path = os.path.join(os.path.dirname(__file__), config_file)

    return providers.Configuration(ini_files=[config_file_path])

