# Setup of Prometheus on Raspberry Pi Zero W

## OS Setup

1. Setup `/etc/ssh/sshd_config` cyphers to lighter weight but still secure cyphers. 
  ```
  Ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes256-ctr
  KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
  MACs hmac-sha2-256,hmac-sha2-512
  ```

## Prometheus Setup

1. Setup `prometheus` user
  * `useradd -m -d /home/prometheus -s /usr/sbin/nologin prometheus`
2. Download `prometheus` and `alertmanager` from <https://prometheus.io/download/>
3. Extract to `/home/prometheus/prometheus`
4. Copy `office_data.yaml`, and `alertmanager.yml` and `prometheus.service` to `/home/prometheus`
5. Copy `prometheus.service` to `/etc/systemd/system/prometheus.service`
5. `sudo chown -R prometheus:prometheus /home/prometheus` to ensure the `prometheus` user owns its home directory
6. 