import kits
import yaml


def __load_config():
    current_path = kits.current_path()
    f = open(current_path + '/config.yaml')
    y = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return y


configurations = __load_config()
runes_cleaner = configurations['log']['runes-cleaner']
restart = configurations['log']['restart']
