import os
import socket, msvcrt, sys


if len(sys.argv) == 1:
    ip = input("Connect to ip:")
else:
    ip = sys.argv[1]
port = 8080

send = ""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect_ex((ip, port))
    sock.setblocking(False)
    try:
        print(f'[connected to {sock.getpeername()}]')
    except OSError:
        print("could not connect to the server.")
        sys.exit()
    while send != 'quit':
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b'\r':
                sock.sendall(bytes(send, "utf-8"))
                send = ""
            elif char == b'\x08':
                send = send[:len(send) - 1]
            else:
                send += char.decode("utf-8")
        print(f'\r> {send}', end='', flush=True)
        try:
            data = sock.recv(1024)
            if data == b'':
                raise ConnectionAbortedError
        except ConnectionAbortedError:
            print("Couldn't connect to server, maybe server session stopped?")
            break
        except BlockingIOError:
            data = None
        if data is not None:
            print(f"data: {data}")