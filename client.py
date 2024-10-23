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
    while send != 'quit':
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b'\r':
                sock.sendall(bytes(send, "utf-8"))
                send = ""
            else:
                send += char.decode("utf-8")
                print(send)
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