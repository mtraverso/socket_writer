import json
import os
import socket
import sys
import uuid
from datetime import datetime, timezone

if len(sys.argv) == 1:
    file = '../json_data.json'
else:
    file = sys.argv[1]

print("Connecting...")
if len(sys.argv) != 2:
    print("Error on params passed")
    sys.exit(1)
lane = sys.argv[1]
if lane == "1":
    gs_socket = "/Users/matias/gsaidata/socket/gs_socket_1"
elif lane == "2":
    gs_socket = "/Users/matias/gsaidata/socket/gs_socket_2"
else:
    print("No socket selected or invalid socket")
    sys.exit()

if os.path.exists(gs_socket):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(gs_socket)
    print("Ready.")
    print("Ctrl-C to quit.")
    print("Sending 'DONE' shuts down the server and quits.")
    f = open(file)
    json_data = json.load(f)
    json_data['event_id'] = str(uuid.uuid4())
    json_data['event_timestamp'] = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
    #json_data['acq_time'] = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    print(json_data)

    client.sendall(json.dumps(json_data).encode())
    client.close()
else:
    print("Couldn't Connect!")
print("Done")
