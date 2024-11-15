#!/usr/bin/python

import json

import config_loader
import logger
import os
import requests

from core import monitor, availability_check
from schedule import every, repeat, run_pending

from core.runes_cleaner import clean


# 每周五 07:00 重启, 避免严重故障.
@repeat(every().friday.at('07:00'))
def restart():
    try:
        logger.log(config_loader.restart, 'Restarting...')
        os.system('reboot')
    except Exception as e:
        print(e)


# 每 60s 报告宿主机状态.
@repeat(every(60).seconds)
def report():
    try:
        state = monitor.monitor(interval=1)
        cpu_rate = state.cpu_percent
        cpu_temperature = state.cpu_temp
        memory_used = state.mem_total - state.mem_free
        memory_total = state.mem_total
        disk_used = state.disk_total - state.disk_free
        disk_total = state.disk_total

        mount = os.system('ls /root/runes') == 0
        smb = availability_check.check_samba()
        dns = availability_check.check_dns()
        body = {"cpuRate": cpu_rate, "cpuTemperature": cpu_temperature, "memoryUsed": memory_used,
                "memoryTotal": memory_total, "diskUsed": disk_used, "diskTotal": disk_total, "mount": mount, "smb": smb,
                "dns": dns}

        requests.post("https://wormhole.dcyy.cc/melina/ca/report", data=json.dumps(body),
                      headers={'Content-Type': 'application/json'})

    except Exception as e:
        print(e)


def mount_disks():
    os.system('mount /dev/sda /root/runes')


if __name__ == '__main__':
    mount_disks()
    # schedule.every(30).seconds.do(report)
    while True:
        run_pending()
