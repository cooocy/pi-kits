import kits
import yaml
from dataclasses import dataclass
from typing import List


@dataclass
class Logger:
    path: str
    max_bytes: int
    backup_count: int


class DNS:
    def __init__(self, checked_domains: List[str]):
        self.checked_domains = checked_domains


class Samba:
    def __init__(self, username: str, password: str, server_ip: str, port: int):
        self.username = username
        self.password = password
        self.server_ip = server_ip
        self.port = port


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

logger__ = Logger(__configurations['logger']['path'], __configurations['logger']['max_bytes'],
                  __configurations['logger']['backup_count'])
report_url__ = __configurations['report_url']
dns__ = DNS(__configurations['dns']['checked_domains'])
samba__ = Samba(__configurations['samba']['username'], str(__configurations['samba']['password']),
                __configurations['samba']['server_ip'], __configurations['samba']['port'])
runes__ = Runes(__configurations['runes']['device'], __configurations['runes']['directory'])
