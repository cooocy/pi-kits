#! /usr/bin/python
import os
import sys

from ping3 import ping
from smb.SMBConnection import SMBConnection


def mount_runes():
    # x = os.system('ls /root/runes')
    if True:
        f = os.system('mount /dev/sda /root/runes')
        print('mount /dev/sda /root/runes: %s' % f)
        if f != 0:
            sys.exit(1)


def restart_dns():
    f = os.system("echo '' >> /etc/resolv.dnsmasq")
    print('modify resolv.dnsmasq: %s' % f)
    if f != 0:
        sys.exit(1)
    f = os.system('systemctl restart dnsmasq')
    print('systemctl restart dnsmasq: %s' % f)
    if f != 0:
        sys.exit(1)


def check_samba() -> bool:
    username = 'root'
    password = '940103'
    server_ip = '192.168.124.2'
    try:
        conn = SMBConnection(username, password, '', '', domain='', use_ntlm_v2=True,
                             is_direct_tcp=True)
        conn.connect(server_ip, 445)
        shares = conn.listShares()
        for share in shares:
            print(share.name)
        conn.close()
        return len(shares) > 0
    except:
        return False


def check_dns() -> bool:
    r1 = ping('route.home.lan')
    print('ping route.home.lan %s' % r1)
    r2 = ping('m.home.lan')
    print('ping m.home.lan %s' % r2)
    r3 = ping('www.baidu.com')
    print('ping www.baidu.com %s' % r3)
    os.system('curl www.baidu.com')
    return isinstance(r1, float) and isinstance(r2, float) and isinstance(r3, float)


if __name__ == '__main__':
    print('-------------------- Mount Runes')
    mount_runes()
    print('\n')
    
    print('-------------------- Restart DNS')
    restart_dns()
    print('\n')

    print('-------------------- Check Samba')
    print(check_samba())
    print('\n')

    print('-------------------- Check DNS')
    print(check_dns())
