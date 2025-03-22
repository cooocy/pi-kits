import json
import l
import requests

L = l.get_logger('h3c')
sent_flag = False


def __login(h3c_config: dict):
    url = h3c_config['server'] + '/api/login/auth'
    request_body = {'username': h3c_config['username'], 'password': h3c_config['password']}
    try:
        response = requests.post(url=url, data=json.dumps(request_body))
        if response.status_code == 200:
            response_body = json.loads(response.text)
            if response_body['code'] == 0:
                session = response_body['data']['session']
                L.info(f'H3C Login Success. session: {session}')
                return session
        L.info('H3C Login Failed.')
        return None
    except Exception as e:
        L.error('H3C Login Error. E: %s', e)
        return None


def scan_online_devices(h3c_config: dict):
    session = __login(h3c_config)
    if session is None or session == '':
        L.error('H3C Login Failed, no need to scan.')
        return []

    url = h3c_config['server'] + '/api/esps'
    headers = {'Pragma': 'no-cache', 'Connection': 'keep-alive', 'authentication': session}
    request_body = [{'object': 'esps.sta', 'method': 'getlist', 'id': 1, 'param': {'list': []}}]
    try:
        response = requests.post(url=url, data=json.dumps(request_body), headers=headers)
        if response.status_code == 200:
            response_body = json.loads(response.text)
            if len(response_body) == 1 and response_body[0]['result']['code'] == 0:
                devices = response_body[0]['result']['data']['list']
                online_devices = [item for item in devices if item["isOnline"] == "true"]
                return online_devices
            if type(response_body) == dict and response_body['code'] == 12:
                L.error('H3C Scan Online Devices Error. Login Timeout.')
                # Login timeout. Send Message.
                pass
        return []
    except Exception as e:
        L.error('H3C Scan Online Devices Error. E: %s', e)
        return []
