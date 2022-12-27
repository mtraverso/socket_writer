import os
import socket
import json
import sys

if len(sys.argv) == 1:
    file = '../json_data.json'
else:
    file = sys.argv[1]

print("Connecting...")
if os.path.exists("/Users/matias/gsaidata/socket/gs_socket"):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/Users/matias/gsaidata/socket/gs_socket")
    print("Ready.")
    print("Ctrl-C to quit.")
    print("Sending 'DONE' shuts down the server and quits.")
    f = open(file)
    json_data = json.load(f)
    print(json_data)

    client.send(json.dumps(json_data).encode())
    client.close()
else:
    print("Couldn't Connect!")
print("Done")
