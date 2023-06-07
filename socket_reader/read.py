import socket

gs_socket = "/Users/matias/gsaidata/socket/gs_socket"

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
    s.connect(gs_socket)
    data = s.recv(8192)

print(f"Received {data!r}")