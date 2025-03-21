from dataclasses import dataclass
from scapy.all import ARP, Ether, srp


@dataclass
class Device:
    ip: str
    mac: str
    name: str


def scan_online_devices(ip_range, known_devices):
    """
    Scan online devices on the local network using scapy,
    and get the device's IP, MAC address, and device name.
    :param ip_range: Scanned IP range, e.g. 192.168.1.1/24
    :param known_devices: List of known devices, e.g. [{'name': '', 'mac': ''}, {}]
    :return: Return the IP, MAC address, and device name of active devices.
    """
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []
    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc
        hostname = __get_hostname(mac, known_devices)
        devices.append(Device(ip=ip, mac=mac, name=hostname))

    return devices


def __get_hostname(mac, known_devices):
    """
    Get the host name of the device through the MAC address.
    :param mac: The MAC address of the target device.
    :param known_devices: List of known devices, e.g. [{'name': '', 'mac': ''}, {}]
    :return: The host name of the device, if it cannot be resolved, returns "Unknown".
    """
    mac_2_device = {item['mac']: item for item in known_devices if 'mac' in item}
    return mac_2_device.get(mac, 'Unknown')
