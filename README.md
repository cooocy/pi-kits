# pi-kits

[English](README.md) | [中文](README.zh.md)

`pi-kits` is a collection of tools for maintaining the availability of Raspberry Pi or any Linux machine.

## Features and Goals

- Check DNS available
- Check Samba available
- Scheduled restart
- Scheduled machine indicator report
- Hidden files clean

## Installation and Running

### Step 1: Install Python 3.X and Pip3

N/A

### Step 2: Install requirements

```shell
pip3 install -r requirements
```

### Step 3: Configurations

Modify the configigurations in `config.yaml`.

### Step 4: Create and start system service

1. Modify the service file `service/pi-host-self-keeping.service` with `TODO`.

2. Copy the modified service file to the directory `/etc/systemd/system/` in your host machine.

3. Execute the following commands in sequence on the host machine.

```shell
systemctl daemon-reload
systemctl enable pi-host-self-keeping.service
systemctl status pi-host-self-keeping.service
systemctl restart pi-host-self-keeping.service
```