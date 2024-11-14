import logger
import os
import shutil
import time

from config_loader import runes_cleaner


def clean(dir: str):
    """
    删除执行目录下所有隐藏的文件/文件夹.
    :param dir: 一个非空目录
    :return: None
    """
    logger.log(runes_cleaner, 'Clean Begin ......')
    if os.path.exists(dir) and os.path.isdir(dir):
        t1 = time.time()
        for root, dirs, files in os.walk(dir, topdown=False):
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
        logger.log(runes_cleaner, 'Directory does not exist or is not directory. dir:', dir)
    logger.log(runes_cleaner, 'Clean End.')
