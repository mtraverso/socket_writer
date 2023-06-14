from datetime import datetime, timezone
import os
import socket
import json
import sys
import uuid
from uuid import UUID
from datetime import datetime

if len(sys.argv) == 1:
    file = '../json_data.json'
else:
    file = sys.argv[1]

print("Connecting...")
gs_socket = "/Users/matias/gsaidata/socket/gs_socket"
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
    json_data['acq_time'] = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    print(json_data)
    json_data['acq_time'] = int(datetime.now().timestamp()*1000)
    client.send(json.dumps(json_data).encode())
    client.close()
else:
    print("Couldn't Connect!")
print("Done")
