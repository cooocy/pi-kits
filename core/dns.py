from ping3 import ping
from typing import List


def available(checked_domains: List[str]) -> bool:
    """
    Check if the DNS service is available.
    :param checked_domains: Which domains are used for the check, all must be successful to return success.
    :return: True if the DNS service is available, False otherwise.
    """
    # ping() returns timing(float, success) or False(bool, failed).
    for domain in checked_domains:
        r = ping(domain, timeout=4)
        if isinstance(r, bool):
            return False
    return True
