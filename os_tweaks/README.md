# OS Configuration

## ENABLE CGROUPS
Per <https://github.com/k3s-io/k3s/issues/2067>, add `cgroup_memory=1 cgroup_enable=memory` to the end of /boot/firmware/cmdline.txt

## Install K3s

See <https://k3s.io> fpr more

Quickstart: 

```
curl -sfL https://get.k3s.io | sh - 
# Check for Ready node, takes ~30 seconds 
sudo k3s kubectl get node 
```

## Build Container

1. Run <os_tweaks\setup_build_node.sh> to install Docker
1. Run <src\build_container.sh> to build the container
1. Import the container into K3s
    1. <https://cwienczek.com/2020/06/import-images-to-k3s-without-docker-registry/>
1. Install the manifest in <k8s_manifest>