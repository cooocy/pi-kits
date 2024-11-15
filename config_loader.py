import kits
import yaml
from typing import List


class Samba:
    def __init__(self, username: str, password: str, server_ip: str, port: int):
        self.username = username
        self.password = password
        self.server_ip = server_ip
        self.port = port


class DNS:
    def __init__(self, checked_domains: List[str]):
        self.checked_domains = checked_domains


class Runes:
    def __init__(self, device: str, directory: str):
        self.device = device
        self.directory = directory


def __load_config():
    current_path = kits.current_path()
    f = open(current_path + '/config.yaml')
    y = yaml.safe_load(f)
    f.close()
    return y


__configurations = __load_config()
# todo __
runes_cleaner = __configurations['log']['runes-cleaner']
restart = __configurations['log']['restart']

report_url__ = __configurations['report_url']
dns__ = DNS(__configurations['dns']['checked_domains'])
samba__ = Samba(__configurations['samba']['username'], str(__configurations['samba']['password']),
                __configurations['samba']['server_ip'], __configurations['samba']['port'])
runes__ = Runes(__configurations['runes']['device'], __configurations['runes']['directory'])
