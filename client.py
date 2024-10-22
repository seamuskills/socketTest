import socket, msvcrt

ip = "127.0.0.1"
port = 8080

send = None

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect_ex((ip, port))
    sock.setblocking(False)
    while send != b'q':
        if msvcrt.kbhit():
            send = msvcrt.getch()
            sock.sendall(send)
        try:
            data = sock.recv(1024)
        except ConnectionAbortedError:
            print("Couldn't connect to server, maybe server session stopped?")
            break
        except BlockingIOError:
            data = None
        if data is not None:
            print(f"data: {data}")