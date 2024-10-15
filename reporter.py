#!/usr/bin/python
import datetime

import availability_check
import json
import monitor
import os
import requests

from schedule import every, repeat, run_pending


@repeat(every().friday.at('07:00'))
def restart():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("[%s]: Restarting..." % now)
    with open('restart.log', 'a') as f:
        f.write('[%s]: Restarting...\n' % now)
    os.system('reboot')


@repeat(every(60).seconds)
def report():
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


if __name__ == '__main__':
    # schedule.every(30).seconds.do(report)
    while True:
        run_pending()
