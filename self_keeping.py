#!/usr/bin/python
import json
import os
import requests

from config_loader import dns__, report_url__, runes__, samba__
from core import dns, machine_monitor, runes, samba
from schedule import every, repeat, run_pending

from logger import LOGGER__


# Weekly restart at 07:00 to avoid serious failures.
@repeat(every().friday.at('07:00'))
def restart():
    try:
        LOGGER__.info('Machine Restarting ...')
        os.system('reboot')
    except Exception as e:
        print(e)


# Every 60 seconds, report the states of the host machine.
@repeat(every(60).seconds)
def report():
    try:
        state = machine_monitor.monitor(interval=1, directory=runes__.directory)
        cpu_rate = state.cpu_percent
        cpu_temperature = state.cpu_temp
        memory_used = state.mem_total - state.mem_free
        memory_total = state.mem_total
        disk_used = state.disk_total - state.disk_free
        disk_total = state.disk_total

        mounted = runes.is_non_empty(runes__.directory)
        samba_available = samba.available(samba__.username, samba__.password, samba__.server_ip, samba__.port)
        dns_available = dns.available(dns__.checked_domains)
        body = {"cpuRate": cpu_rate, "cpuTemperature": cpu_temperature, "memoryUsed": memory_used,
                "memoryTotal": memory_total, "diskUsed": disk_used, "diskTotal": disk_total, "mount": mounted,
                "smb": samba_available,
                "dns": dns_available}
        requests.post(report_url__, data=json.dumps(body), headers={'Content-Type': 'application/json'})
        LOGGER__.info('Report Success. ', body)
    except Exception as e:
        LOGGER__.error('Report Error. ', e)


if __name__ == '__main__':
    LOGGER__.info('Self Keeping Started.')
    runes.mount_runes(runes__.device, runes__.directory)
    LOGGER__.info('Mount Runes End. The result is unknown.')
    while True:
        run_pending()
