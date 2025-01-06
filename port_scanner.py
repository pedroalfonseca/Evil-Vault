#!/usr/bin/env python3

from re import compile
from nmap import PortScanner


# Regex patterns
IP_ADDR_PAT = compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
PORT_RANGE_PAT = compile("([0-9]+)-([0-9]+)")

# Default port range values
PORT_MIN = 0
PORT_MAX = 65535


while True:
    ip_addr = input("IP address to scan: ").strip()
    if IP_ADDR_PAT.search(ip_addr):
        break

    print(f"\033[31mERROR\033[0m: Please enter a valid IPv4 address.")

while True:
    port_range = input("Port range: ").strip()
    if not port_range:
        break

    port_range_valid = PORT_RANGE_PAT.search(port_range)
    if port_range_valid:
        PORT_MIN = int(port_range_valid.group(1))
        PORT_MAX = int(port_range_valid.group(2))
        break

    print(f"\033[31mERROR\033[0m: Please enter a valid port range in the format <min>-<max>. Example: 10-60")

scanner = PortScanner()

for port in range(PORT_MIN, PORT_MAX + 1):
    try:
        result = scanner.scan(ip_addr, str(port))
        port_status = (result["scan"][ip_addr]["tcp"][port]["state"])
        print(f"Port {port} is {port_status}.")
    except Exception as e:
        print(f"Failed to scan port {port}: {e}")
