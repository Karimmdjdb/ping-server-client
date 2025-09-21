from sys import argv, exit, maxsize
from signal import signal, SIGINT
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from mytime import get_timestamp_ms
from time import sleep

server_ip, server_port = "127.0.0.1", 10001
message = "PING"
pack_trans, pack_recv, bench_start, bench_end = 0, 0, 0, 0
soc:socket = None


def show_stats() :
    print(f"\n--- {server_ip} ping statistics ---")
    bench_end = get_timestamp_ms(True)
    print(f"{pack_trans} packets transmitted, {pack_recv} packets recieved, {100-(pack_recv/pack_trans*100):.0f}% packet loss, time {bench_end-bench_start}ms")

def safe_exit(signal, frame) :
    soc.close()
    show_stats()
    exit(0)

signal(SIGINT, safe_exit)

def main(args) :
    global soc, pack_trans, pack_recv, bench_start, bench_end

    limit = int(args[0]) if len(args) == 1 else maxsize
    # create UDP socket
    soc = socket(AF_INET, SOCK_DGRAM)
    # allows address fast reuse
    soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    soc.settimeout(2)

    print(f"PING {server_ip}:{server_port} {len(message.encode('utf-8'))} bytes of data.")

    bench_start = get_timestamp_ms(True)

    count = 1

    while count <= limit :
        # save the time and send a request to the server and
        t_start = get_timestamp_ms()
        soc.sendto(message.encode('utf-8'), (server_ip, server_port))
        pack_trans += 1

        # wait for server answer
        try :
            res, _ = soc.recvfrom(2048)
            t_end = get_timestamp_ms()
            pack_recv += 1
            # print the result
            print(f"{len(res)} bytes from {server_ip} : icmp_seq={count} time={t_end-t_start:.3f} ms")
            # sleep 1 second
            sleep(1)
        except TimeoutError as e :
            pass
        finally :
            bench_end = get_timestamp_ms(True)



        count += 1


    soc.close()

    show_stats()

if __name__ == "__main__" :
    main(argv[1:])