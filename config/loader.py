import yaml


def load_yaml_configurations(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
