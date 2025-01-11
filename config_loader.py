import kits
import yaml
from dataclasses import dataclass
from typing import List


@dataclass
class Logger:
    path: str
    max_bytes: int
    backup_count: int


@dataclass
class Reporter:
    base_url: str
    status_report_uri: str
    boot_plan_pick_uri: str
    boot_record_report_uri: str


@dataclass
class DNS:
    checked_domains: List[str]


@dataclass
class Samba:
    username: str
    password: str
    server_ip: str
    port: int


@dataclass
class Runes:
    device: str
    directory: str


def __load_config():
    current_path = kits.current_path()
    f = open(current_path + '/config.yaml')
    y = yaml.safe_load(f)
    f.close()
    return y


__configurations = __load_config()

logger__ = Logger(__configurations['logger']['path'],
                  __configurations['logger']['max_bytes'],
                  __configurations['logger']['backup_count'])
reporter__ = Reporter(__configurations['reporter']['base_url'],
                      __configurations['reporter']['status_report_uri'],
                      __configurations['reporter']['boot_plan_pick_uri'],
                      __configurations['reporter']['boot_record_report_uri'])

dns__ = DNS(__configurations['dns']['checked_domains'])
samba__ = Samba(__configurations['samba']['username'], str(__configurations['samba']['password']),
                __configurations['samba']['server_ip'], __configurations['samba']['port'])
runes__ = Runes(__configurations['runes']['device'], __configurations['runes']['directory'])
