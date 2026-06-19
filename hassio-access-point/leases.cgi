#!/bin/sh
echo "Content-Type: text/html"
echo ""

LEASE_FILE="/var/lib/misc/dnsmasq.leases"
INTERFACE=$(jq -r '.interface // "wlan0"' /data/options.json 2>/dev/null || echo "wlan0")

cat <<'HTML'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="30">
  <title>Access Point</title>
  <style>
    body { font-family: sans-serif; padding: 1rem; }
    h2 { margin-top: 1.5rem; }
    h2:first-child { margin-top: 0; }
    table { border-collapse: collapse; width: 100%; margin-bottom: 1rem; }
    th, td { border: 1px solid #ccc; padding: 0.4rem 0.8rem; text-align: left; }
    th { background: #f0f0f0; }
    tr:nth-child(even) { background: #fafafa; }
    .unknown { color: #aaa; }
  </style>
</head>
<body>
HTML

# --- Connected Clients ---
echo "<h2>Connected Clients</h2>"

CONNECTED=$(hostapd_cli -i "$INTERFACE" list_sta 2>/dev/null)

if [ -z "$CONNECTED" ]; then
    echo "<p>No clients connected.</p>"
else
    echo "<table>"
    echo "<tr><th>MAC Address</th><th>IP Address</th><th>Hostname</th></tr>"
    echo "$CONNECTED" | while IFS= read -r mac; do
        [ -z "$mac" ] && continue
        ip="-"
        hostname="-"
        ip_class="unknown"
        host_class="unknown"
        if [ -f "$LEASE_FILE" ]; then
            lease=$(grep -i " $mac " "$LEASE_FILE" | head -1)
            if [ -n "$lease" ]; then
                ip=$(echo "$lease" | awk '{print $3}')
                hostname=$(echo "$lease" | awk '{print $4}')
                ip_class=""
                host_class=""
            fi
        fi
        printf '<tr><td>%s</td><td class="%s">%s</td><td class="%s">%s</td></tr>\n' \
            "$mac" "$ip_class" "$ip" "$host_class" "$hostname"
    done
    echo "</table>"
fi

# --- DHCP Leases ---
echo "<h2>DHCP Leases</h2>"

if [ ! -f "$LEASE_FILE" ] || [ ! -s "$LEASE_FILE" ]; then
    echo "<p>No active leases found.</p>"
else
    echo "<table>"
    echo "<tr><th>IP Address</th><th>MAC Address</th><th>Hostname</th><th>Expires</th></tr>"
    while IFS=' ' read -r expiry mac ip hostname _; do
        if [ "$expiry" = "0" ]; then
            exp_str="static"
        else
            exp_str=$(awk -v ts="$expiry" 'BEGIN { print strftime("%Y-%m-%d %H:%M:%S", ts+0) }')
        fi
        printf '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' \
            "$ip" "$mac" "$hostname" "$exp_str"
    done < "$LEASE_FILE"
    echo "</table>"
fi

echo "</body></html>"
