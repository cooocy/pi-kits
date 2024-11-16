import config_loader
import logging
import os

# Make log dir if not exists.
logger_dir = config_loader.logger__.path.rsplit('/', 1)[0]
if not os.path.exists(logger_dir):
    os.makedirs(logger_dir)

# Define common file handler.
common_file_handler = logging.FileHandler(config_loader.logger__.path)
common_file_handler.setLevel(logging.INFO)
common_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Define root logger.
__ROOT_LOGGER = logging.getLogger()
__ROOT_LOGGER.setLevel(logging.INFO)
__ROOT_LOGGER.addHandler(common_file_handler)

# Close some loggers, since it has too many logs.
__SMB_LOGGER = logging.getLogger('SMB.SMBConnection')
__SMB_LOGGER.disabled = True


def get_logger(name: str = None) -> logging.Logger:
    """
    Get singleton logger by name.
    :param name: Empty to get the root logger.
    :return: logger.
    """
    if name is None or len(name) == 0:
        return __ROOT_LOGGER
    __logger = logging.getLogger(name)
    __logger.setLevel(logging.INFO)
    # Cannot bind handler, otherwise it will cause log duplication. I don't know why.
    return __logger
