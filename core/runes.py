import l
import os
import shutil
import time

L = l.get_logger('runes')


def mount_runes(device: str, directory: str):
    """
    Mount Runes.
    Errors will be ignored.
    :param device: device
    :param directory: directory
    :return: None
    """
    cmd = f'mount {device} {directory}'
    os.system(cmd)
    # if error, stdout will print errors.


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
