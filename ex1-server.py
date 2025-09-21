from sys import argv
from signal import signal, SIGINT
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from random import random

server_port = 10001
message = "PONG"

soc:socket = None

def safe_exit(signal, frame) :
    soc.close()
    print("\nServer exited successfully.")
    exit(0)

signal(SIGINT, safe_exit)

def main(args) :
    global soc
    # create UDP socket
    soc = socket(AF_INET, SOCK_DGRAM)
    # allows address fast reuse
    soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # bind socket
    soc.bind(('', server_port))

    print(f"server listening on port {server_port}")
    # server loop
    while True :
        _, client_address = soc.recvfrom(2048)
        if random()*100 < 50 :
            continue
        soc.sendto(message.encode('utf-8'), client_address)


if __name__ == "__main__" :
    main(argv[1:])