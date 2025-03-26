#!/usr/bin/python
import json
import l
import os
import requests

from config import dns_configurations, reporter_configurations, runes_configurations, samba_configurations, \
    h3c_configurations
from core import dns, machine_monitor, runes, samba, h3c
from schedule import every, repeat, run_pending

L = l.get_logger('self_keeping')
post_headers = {'Content-Type': 'application/json', reporter_configurations['header']: reporter_configurations['token']}


# Weekly restart at 07:00 to avoid serious failures.
@repeat(every().friday.at('07:00'))
def restart():
    try:
        body = {'note': 'Scheduled Restart'}
        requests.post(url=reporter_configurations['base_url'] + reporter_configurations['boot_record_report_uri'],
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
        restart_plan_response = requests.post(
            url=reporter_configurations['base_url'] + reporter_configurations['boot_plan_pick_uri'],
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
                requests.post(
                    url=reporter_configurations['base_url'] + reporter_configurations['boot_record_report_uri'],
                    data=json.dumps(body),
                    headers=post_headers)
                L.info('Report Restart Record Success. Body: %s', body)
                L.info('Planned Restarting...')
                os.system('reboot')

    except Exception as e:
        L.error('Planned Restarting Error. E: %s', e)


# Every 60 seconds, report the states of the host machine.
@repeat(every(60).seconds)
def report_self_status():
    def ext_available():
        __mounted = False
        __samba_available = False
        __dns_available = False
        try:
            __mounted = runes.is_non_empty(runes_configurations['directory'])
        except Exception as e:
            L.error('Mounted Available Error. E: %s', e)
            __mounted = False
        try:
            __samba_available = samba.available(samba_configurations['username'], samba_configurations['password'],
                                                samba_configurations['server_ip'],
                                                samba_configurations['port'])
        except Exception as e:
            L.error('Samba Available Error. E: %s', e)
            __samba_available = False
        try:
            __dns_available = dns.available(dns_configurations['checked_domains'])
        except Exception as e:
            L.error('DNS Available Error. E: %s', e)
            __dns_available = False
        return __mounted, __samba_available, __dns_available

    try:
        state = machine_monitor.monitor(interval=1, directory=runes_configurations['directory'])
        cpu_rate = state.cpu_percent
        cpu_temperature = state.cpu_temp
        memory_used = state.mem_total - state.mem_free
        memory_total = state.mem_total
        disk_used = state.disk_total - state.disk_free
        disk_total = state.disk_total
        mounted, samba_available, dns_available = ext_available()

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
        requests.post(url=reporter_configurations['base_url'] + reporter_configurations['status_report_uri'],
                      data=json.dumps(body),
                      headers=post_headers)
        L.info('Status Report Success. Body: %s', body)
    except Exception as e:
        L.error('Status Report Error. E: %s', e)


# Every 100 seconds, report the states of LAN Online Devices.
@repeat(every(100).seconds)
def report_online_devices():
    try:
        devices = h3c.scan_online_devices(h3c_config=h3c_configurations)
        online_devices = []
        for device in devices:
            d = {'name': device['hostname'], 'mac': device['mac'], 'ip': device['ip']}
            online_devices.append(d)
        body = {'onlineDevices': online_devices}
        requests.post(url=reporter_configurations['base_url'] + reporter_configurations['lan_status_report_uri'],
                      data=json.dumps(body),
                      headers=post_headers)
        L.info('Online Devices Report Success. Body: %s', body)
    except Exception as e:
        L.error('Online Devices Report Error. E: %s', e)


if __name__ == '__main__':
    L.info('Self Keeping Started.')
    runes.mount_runes(runes_configurations['device'], runes_configurations['directory'])
    L.info('Mount Runes End. The result is unknown.')
    while True:
        run_pending()
