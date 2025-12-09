# Setup of Prometheus on Raspberry Pi Zero W

## OS Setup

1. Setup `/etc/ssh/sshd_config` cyphers to lighter weight but still secure cyphers. 
  ```
  Ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes256-ctr
  KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
  MACs hmac-sha2-256,hmac-sha2-512
  ```

## Prometheus Setup

It does it all for you!

1. `sudo apt install prometheus prometheus-alertmanager  -y`
2. Copy `prometheus.yaml`

## Json_exporter

1. Download `json_exporter` from <https://github.com/prometheus-community/json_exporter/releases>
2. Copy `json_exporter` to `/usr/bin/json_exporter`
3. Copy `json_exporter.yaml` to `/etc/json_exporter/json_exporter.yaml`
4. Copy `json_exporter.service` to `/etc/systemd/system/json_exporter.service`
5. `systemctl daemon-reload` to reload systemd services
6. `systemctl enable json_exporter.service` to enable the service
7. `systemctl start json_exporter.service` to start the service
8. `journalctl -fu json_exporter` check logs for errors

## Grafana

See: [https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/](https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/)

!!! Ensure Grafana is enabled and started !!!