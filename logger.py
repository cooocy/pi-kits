import config_loader
import logging
import os

logger_dir = config_loader.logger__.path.rsplit('/', 1)[0]
if not os.path.exists(logger_dir):
    os.makedirs(logger_dir)

LOGGER__ = logging.getLogger()
LOGGER__.setLevel(logging.INFO)

file_handler = logging.FileHandler(config_loader.logger__.path)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
LOGGER__.addHandler(file_handler)
