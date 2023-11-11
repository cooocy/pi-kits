#!/usr/bin/python
import psutil
import sys
from datetime import datetime


class State:
    def __init__(self, cpu_count, cpu_percent, cpu_temp,
                 mem_total, mem_free, mem_percent,
                 disk_total, disk_free, disk_percent,
                 net_send_p_second, net_recv_p_second):
        self.cpu_count = cpu_count
        self.cpu_percent = cpu_percent
        self.cpu_temp = cpu_temp

        self.mem_total = mem_total
        self.mem_free = mem_free
        self.mem_percent = mem_percent

        self.disk_total = disk_total
        self.disk_free = disk_free
        self.disk_percent = disk_percent

        self.net_sent = net_send_p_second
        self.net_recv = net_recv_p_second

    def __str__(self) -> str:
        return 'State(cpu_count: %s, cpu_percent: %s, cpu_temp: %s, mem_total: %s, mem_free: %s, mem_percent: %s, disk_total: %s, ' \
               'disk_free: %s, disk_percent: %s, net_sent: %s, net_recv: %s)' % (
            self.cpu_count, self.cpu_percent, self.cpu_temp, self.mem_total, self.mem_free, self.mem_percent,
            self.disk_total,
            self.disk_free, self.disk_percent, self.net_sent, self.net_recv)


class PrettyState:
    __1K = 1024
    __1M = 1024 * 1024
    __1G = 1024 * 1024 * 1024

    def __init__(self, cpu_count, cpu_percent, cpu_temp,
                 mem_total, mem_free, mem_percent,
                 disk_total, disk_free, disk_percent,
                 net_send_p_second, net_recv_p_second):
        self.cpu_count = cpu_count
        self.cpu_percent = '%.2f%s' % (cpu_percent, '%')
        self.cpu_temp = '%.0f%s' % (cpu_temp, '℃')

        self.mem_total = '%.2fMB' % (mem_total / PrettyState.__1M)
        self.mem_free = '%.2fMB' % (mem_free / PrettyState.__1M)
        self.mem_percent = '%.2f%s' % (mem_percent, '%')

        self.disk_total = '%.2fGB' % (disk_total / PrettyState.__1G)
        self.disk_free = '%.2fGB' % (disk_free / PrettyState.__1G)
        self.disk_percent = '%.2f%s' % (disk_percent, '%')

        if net_send_p_second > 10 * PrettyState.__1G:
            self.net_sent = '%.2fGB/s' % (net_send_p_second / PrettyState.__1G)
        elif net_send_p_second > 10 * PrettyState.__1M:
            self.net_sent = '%.2fMB/s' % (net_send_p_second / PrettyState.__1M)
        elif net_send_p_second > 10 * PrettyState.__1K:
            self.net_sent = '%.2fKB/s' % (net_send_p_second / PrettyState.__1K)
        else:
            self.net_sent = '%.2fB/s' % net_send_p_second
        if net_recv_p_second > 10 * PrettyState.__1G:
            self.net_recv = '%.2fGB/s' % (net_recv_p_second / PrettyState.__1G)
        elif net_recv_p_second > 10 * PrettyState.__1M:
            self.net_recv = '%.2fMB/s' % (net_recv_p_second / PrettyState.__1M)
        elif net_recv_p_second > 10 * PrettyState.__1K:
            self.net_recv = '%.2fKB/s' % (net_recv_p_second / PrettyState.__1K)
        else:
            self.net_recv = '%.2fB/s' % net_recv_p_second

    def __str__(self):
        return 'PrettyState(cpu_count: %s, cpu_percent: %s, cpu_temp: %s, mem_total: %s, mem_free: %s, mem_percent: %s, disk_total: %s, ' \
               'disk_free: %s, disk_percent: %s, net_sent: %s, net_recv: %s)' % (
            self.cpu_count, self.cpu_percent, self.cpu_temp, self.mem_total, self.mem_free, self.mem_percent,
            self.disk_total,
            self.disk_free, self.disk_percent, self.net_sent, self.net_recv)


def monitor(interval, is_pretty=False):
    """
    Monitor the CPU, Mem, Disk, Network every {interval} second.
    call e.g.
    while True:
      print(monitor(1))
    :param interval: seconds
    :param is_pretty: pretty format
    :return: system utilization of cpu, mem, disk and net sent/recv speed.
      e.g. State(cpu_count: 8, cpu_percent: 15.51%, mem_total: 32768.00MB,
                 mem_free: 10772.00MB, mem_percent: 67.10%,
                 disk_total: 460.43GB, disk_free: 226.64GB, disk_percent: 50.78%,
                 net_sent: 14.37KB/s, net_recv: 6259.00B/s)
    """

    before = datetime.now()
    sent_before = psutil.net_io_counters().bytes_sent
    recv_before = psutil.net_io_counters().bytes_recv

    # CPU
    cpu_count = psutil.cpu_count()
    cpu_percent = sum(psutil.cpu_percent(interval=interval, percpu=True))
    cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current

    # Memory
    memory = psutil.virtual_memory()
    mem_total = memory.total
    mem_free = memory.available
    mem_percent = memory.percent

    # Disk
    disk = psutil.disk_usage('/root/runes')
    disk_total = disk.total
    disk_free = disk.free
    disk_percent = 100 * (disk_total - disk_free) / disk_total

    # Network
    net_sent = psutil.net_io_counters().bytes_sent - sent_before
    net_recv = psutil.net_io_counters().bytes_recv - recv_before
    now = datetime.now()
    seconds = (now - before).seconds

    if is_pretty:
        return PrettyState(cpu_count, cpu_percent, cpu_temp, mem_total, mem_free, mem_percent, disk_total, disk_free,
                           disk_percent, net_sent / seconds, net_recv / seconds)
    else:
        return State(cpu_count, cpu_percent, cpu_temp, mem_total, mem_free, mem_percent, disk_total, disk_free,
                     disk_percent, net_sent / seconds, net_recv / seconds)


if __name__ == '__main__':
    internal = int(sys.argv[1])
    is_pretty = int(sys.argv[2]) == 1
    if is_pretty is None:
        is_pretty = False
    while True:
        print(monitor(internal, is_pretty))

