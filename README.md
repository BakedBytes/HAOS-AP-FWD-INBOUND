# Hassio-Access-Point (Personal Fork)

> ⚠️ **This is a personal fork for private use only.** It is not intended for general use or support. Please refer to the [original repository](https://github.com/ex-ml/Hassio-Access-Point) for the official version.

## About

This is a fork of [ex-ml/Hassio-Access-Point](https://github.com/ex-ml/Hassio-Access-Point), a Home Assistant OS add-on that turns your device into a WiFi access point using `hostapd`.

## Changes in this fork

### Inbound routing fix (`run.sh`)

The original add-on only allows outbound traffic from WLAN clients to the internet (`ESTABLISHED,RELATED` only for inbound). This means it is **not possible to reach WLAN clients from the LAN side**.

This fork adds a missing `iptables` rule that allows new incoming connections from the LAN interface into the WLAN network:

```bash
iptables-nft -A FORWARD -i $DEFAULT_ROUTE_INTERFACE -o $INTERFACE -d $NETWORK_CIDR -j ACCEPT
```

The network address (`$NETWORK_CIDR`) is automatically calculated from the configured `address` and `netmask` options — no hardcoded values.

This rule is also properly removed when `client_internet_access` is disabled.

## Original Repository

All credits go to the original authors. Please visit the original project for documentation, configuration options and support:

👉 https://github.com/ex-ml/Hassio-Access-Point
