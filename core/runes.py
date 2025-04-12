import json

import l
import os
import shutil
import subprocess
import time

L = l.get_logger('runes')


def mount_runes(directory: str):
    """
    Mount Runes.
    If there is only one unmounted device, mount it.
    Errors will be ignored.
    :param directory: directory
    :return: None
    """

    stdout = subprocess.run(['lsblk', '--json'], capture_output=True, text=True, check=True).stdout
    block_devices: dict = json.loads(stdout)
    bd = block_devices.get('blockdevices', [])
    not_mounted = [b for b in bd if b['mountpoint'] is None and 'children' not in b]
    if len(not_mounted) == 0:
        L.info('No unmounted devices found.')
        return

    L.info(f'Found unmounted devices, size: {len(not_mounted)}, details: {not_mounted}')
    # if there is only one unmounted device, mount it.
    # {"name":"sdb", "maj:min":"8:16", "rm":false, "size":"3.6T", "ro":false, "type":"disk", "mountpoint":"/root/runes"}
    if len(not_mounted) == 1:
        device = f'/dev/{not_mounted[0]["name"]}'
        os.system(f'mount {device} {directory}')
        L.info(f'Mount Runes Success. Device: {device}, Directory: {directory}')
        # if error, stdout will print errors.
    else:
        L.info('There are multiple unmounted devices. Please mount them manually.')


def is_non_empty(directory: str) -> bool:
    """
    Check if runes is not empty.
    :param directory: runes directory
    :return: True if not empty.
    """
    return os.path.isdir(directory) and len(os.listdir(directory)) > 0


def clean(directory: str):
    """
    Delete all hidden elements(file and dir) in the specified directory.
    :param directory: directory
    :return: None
    """
    L.info('Clean Begin ......')
    if os.path.exists(directory) and os.path.isdir(directory):
        t1 = time.time()
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                if name.startswith('.'):
                    file_path = os.path.join(root, name)
                    try:
                        os.remove(file_path)
                        L.info('Deleted file: %s', file_path)
                    except OSError as e:
                        L.error('Error deleting file: %s, E: %s', file_path, e)

            for name in dirs:
                if name.startswith('.'):
                    dir_path = os.path.join(root, name)
                    try:
                        shutil.rmtree(dir_path)
                        L.info('Deleted dir: %s', dir_path)
                    except OSError as e:
                        L.error('Error deleting dir: %s, E: %s', dir_path, e)
        t2 = time.time()
        L.info('Clean Const: %f', (t2 - t1))
    else:
        L.info('Directory does not exist or is not directory. dir: %s', directory)

    L.info('Clean End.')
