# pi-kits

[English](README.md) | [中文](README.zh.md)

`pi-kits` 是用于维护 `Raspberry Pi` 或任何 Linux 机器可用性的工具集合。

## 功能和目标

- 检查 DNS 可用性
- 检查 Samba 可用性
- 定时重启
- 计划重启
- 定时机器指标上报
- 隐藏文件清理

## 安装和运行

### 步骤 1: 安装 Python 3.X 和 Pip3

N/A

### 步骤 2: 安装依赖

```shell
pip3 install -r requirements
```

### 步骤 3: 配置

修改配置文件 `config.yaml`。

### Step 4: 创建并启动系统服务

1. 修改服务文件 `pi-host-self-keeping.service` 中的 `TODO`。

2. 拷贝修改后的服务文件至宿主机的 `/etc/systemd/system/` 目录。

3. 在宿主机上顺序执行下面的命令。

```shell
systemctl daemon-reload
systemctl enable pi-host-self-keeping.service
systemctl status pi-host-self-keeping.service
systemctl restart pi-host-self-keeping.service
```