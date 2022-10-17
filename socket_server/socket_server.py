import os
import socket

if os.path.exists("/Users/matias/gsaidata/socket/gs_socket"):
    os.remove("/Users/matias/gsaidata/socket/gs_socket")

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/Users/matias/gsaidata/socket/gs_socket")
while True:
    server.listen(1)
    conn, addr = server.accept()
    datagram = conn.recv(16636)
    print(datagram)
