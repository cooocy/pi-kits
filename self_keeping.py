#!/usr/bin/python
import json
import l
import os
import requests

from config_loader import dns__, reporter__, runes__, samba__
from core import dns, machine_monitor, runes, samba
from schedule import every, repeat, run_pending

L = l.get_logger('self_keeping')
post_headers = {'Content-Type': 'application/json'}


# Weekly restart at 07:00 to avoid serious failures.
@repeat(every().friday.at('07:00'))
def restart():
    try:
        body = {'note': 'Scheduled Restart'}
        requests.post(url=reporter__.base_url + reporter__.boot_record_report_uri,
                      data=json.dumps(body),
                      headers=post_headers)
        L.info('Scheduled Restarting ...')
        os.system('reboot')
    except Exception as e:
        L.error('Scheduled Restarting Error. E: %s', e)


# Every 43 seconds, pick the restart plan and do restart.
@repeat(every(43).seconds)
def planned_restart():
    try:
        restart_plan_response = requests.post(url=reporter__.base_url + reporter__.boot_plan_pick_uri,
                                              data=json.dumps({}),
                                              headers=post_headers)
        if restart_plan_response.status_code == 200:
            restart_plan_response_body = restart_plan_response.json()
            if restart_plan_response_body['data'] is None:
                L.info('Pick Restart Plan End. No Restart Plan.')
            else:
                plan = restart_plan_response_body['data']
                L.info('Pick Restart Plan Success. %s', plan)
                body = {'note': plan['note']}
                requests.post(url=reporter__.base_url + reporter__.boot_record_report_uri,
                              data=json.dumps(body),
                              headers=post_headers)
                L.info('Report Restart Record Success. Body: %s', body)
                L.info('Planned Restarting...')
                os.system('reboot')

    except Exception as e:
        L.error('Planned Restarting Error. E: %s', e)


# Every 60 seconds, report the states of the host machine.
@repeat(every(60).seconds)
def report_status():
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
        body = {
            "cpuRate": cpu_rate,
            "cpuTemperature": cpu_temperature,
            "memoryUsed": memory_used,
            "memoryTotal": memory_total,
            "diskUsed": disk_used,
            "diskTotal": disk_total,
            "mount": mounted,
            "smb": samba_available,
            "dns": dns_available
        }
        requests.post(url=reporter__.base_url + reporter__.status_report_uri,
                      data=json.dumps(body),
                      headers=post_headers)
        L.info('Status Report Success. Body: %s', body)
    except Exception as e:
        L.error('Status Report Error. E: %s', e)


if __name__ == '__main__':
    L.info('Self Keeping Started.')
    runes.mount_runes(runes__.device, runes__.directory)
    L.info('Mount Runes End. The result is unknown.')
    while True:
        run_pending()
