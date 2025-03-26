from config.loader import load_yaml_configurations

app_configurations = load_yaml_configurations('config/app_private.yaml')
logger_configurations = app_configurations['logger']
reporter_configurations = app_configurations['reporter']
dns_configurations = app_configurations['dns']
samba_configurations = app_configurations['samba']
runes_configurations = app_configurations['runes']
lan_scanner_configurations = app_configurations['lan_scanner']
h3c_configurations = app_configurations['h3c']

__all__ = ['app_configurations', 'logger_configurations', 'reporter_configurations', 'dns_configurations',
           'samba_configurations', 'runes_configurations', 'lan_scanner_configurations', 'h3c_configurations']
