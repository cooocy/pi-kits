import logger
import os
import shutil
import time

from config_loader import runes_cleaner


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
    logger.log(runes_cleaner, 'Clean Begin ......')
    if os.path.exists(directory) and os.path.isdir(directory):
        t1 = time.time()
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                if name.startswith('.'):
                    file_path = os.path.join(root, name)
                    try:
                        os.remove(file_path)
                        logger.log(runes_cleaner, 'Deleted file:', file_path)
                    except OSError as e:
                        logger.log(runes_cleaner, 'Error deleting file: %s, e: %s' % (file_path, e))

            # 删除隐藏文件夹
            for name in dirs:
                if name.startswith('.'):
                    dir_path = os.path.join(root, name)
                    try:
                        shutil.rmtree(dir_path)
                        logger.log(runes_cleaner, 'Deleted dir:', dir_path)
                    except OSError as e:
                        logger.log(runes_cleaner, 'Error deleting dir: %s, e: %s' % (dir_path, e))
        t2 = time.time()
        logger.log(runes_cleaner, 'Clean Const: %f' % (t2 - t1))
    else:
        logger.log(runes_cleaner, 'Directory does not exist or is not directory. dir:', directory)
    logger.log(runes_cleaner, 'Clean End.')
