import datetime
import os
import time


def now():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def now2():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_file_name(file_path):
    return file_path[file_path.rindex('/') + 1:] if file_path.__contains__('/') else file_path


def current_path():
    current_file_path = os.path.abspath(__file__)
    return current_file_path[:current_file_path.rindex('/')]
