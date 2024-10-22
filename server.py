import socket

ip = "127.0.0.1"
port = 8080


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((ip, port))
    sock.listen()
    print("Server ready to listen")
    conn, addr = sock.accept()
    with conn:
        print(f"Connected to {addr}")
        while True:
            dat = conn.recv(1024)
            if not dat:
                break
            else:
                print(f"data recieved: {dat}")
            conn.sendall(dat)