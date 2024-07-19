# ENABLE CGROUPS
Per <https://github.com/k3s-io/k3s/issues/2067>, add `cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory` to the end of /boot/firmware/cmdline.txt
