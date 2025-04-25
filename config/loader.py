import os

import requests
import toml
import yaml
from enum import Enum


class Formats(Enum):
    YAML = "yaml"
    TOML = "toml"


def load_toml_configurations(config_path):
    with open(config_path, 'r') as file:
        config = toml.loads(file.read())
    return config


def load_yaml_configurations(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def load_online_configurations(full_name: str, configuration_format: Formats) -> dict:
    """
    Load configurations from a specified online source.

    :param full_name: The full name of the configuration file, may have a Placeholder like ':tail'
    :param configuration_format: The format of the configuration file (YAML or TOML).
    :return: A dictionary containing the loaded configurations.
    """

    configurations_url = os.environ.get('BOOKSTORE_URL')
    configurations_token = os.environ.get('BOOKSTORE_TOKEN')
    configuration_tail = os.environ.get('CONFIGURATION_TAIL')
    if configurations_url is None or len(configurations_url) == 0 or configurations_token is None or len(
            configurations_token) == 0:
        raise ValueError("Environment variables CONFIGURATIONS_URL and CONFIGURATIONS_TOKEN must be set.")
    if full_name is None or len(full_name) == 0:
        raise ValueError("full_name must be provided.")

    full_name = full_name.replace(':tail', configuration_tail)
    url = f"{configurations_url}/{full_name}"
    response = requests.get(url=url, headers={'Authorization': f'token {configurations_token}'})
    if response.status_code != 200:
        return {}
    response_body = response.text
    if response_body is None or len(response_body) == 0:
        return {}

    if configuration_format == Formats.YAML:
        return yaml.safe_load(response_body)
    else:
        return toml.loads(response_body)
