#!/bin/sh
echo "Content-Type: text/html"
echo ""

LEASE_FILE="/var/lib/misc/dnsmasq.leases"

cat <<'HTML'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="30">
  <title>DHCP Leases</title>
  <style>
    body { font-family: sans-serif; padding: 1rem; }
    h2 { margin-top: 0; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 0.4rem 0.8rem; text-align: left; }
    th { background: #f0f0f0; }
    tr:nth-child(even) { background: #fafafa; }
  </style>
</head>
<body>
<h2>Active DHCP Leases</h2>
HTML

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
