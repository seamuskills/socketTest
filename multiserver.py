import socket
import sys
import selectors
import types
import msvcrt

sel = selectors.DefaultSelector()

host, port = sys.argv[1:3]
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, int(port)))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


def accept_wrapper(sock):
    sock.setblocking(False)
    conn, addr = sock.accept()
    print(f"New connection from {(conn, addr)}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    sock.setblocking(False)
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closed connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

try:
    while True:
        events = sel.select(timeout=0.5)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
        if msvcrt.kbhit(): #select makes ctrl+c not work for some reason, so this is a good workaround
            if msvcrt.getch() == b'q':
                raise KeyboardInterrupt
except KeyboardInterrupt:
    print("exiting...")
finally:
    sel.close()