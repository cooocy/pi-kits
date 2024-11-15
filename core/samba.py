from smb.SMBConnection import SMBConnection


def available(username: str, password: str, server_ip: str, port: int) -> bool:
    """
    Check if the Samba service is available.
    Whether service is available based on shares length > 0.
    :param username: username
    :param password: password
    :param server_ip: server ip
    :param port: server port
    :return: True if the Samba service is available, False otherwise.
    """
    conn = SMBConnection(username, password, '', '', domain='', use_ntlm_v2=True, is_direct_tcp=True)
    conn.connect(server_ip, port)
    shares = conn.listShares()
    for share in shares:
        print(share.name)
    conn.close()
    return len(shares) > 0
