# OS Configuration

This is the configuration for a Raspberry Pi, tested on a 3b+.

## ENABLE CGROUPS
Per <https://github.com/k3s-io/k3s/issues/2067>, add `cgroup_memory=1 cgroup_enable=memory` to the end of /boot/firmware/cmdline.txt

## Enable office-data-collector
```
sudo systemctl enable office-data-collector.service
```
