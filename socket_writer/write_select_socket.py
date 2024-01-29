import json
import os
import socket
import sys
import uuid
from datetime import datetime, timezone

import random

if len(sys.argv) == 1:
    file = '../json_data.json'
else:
    file = sys.argv[2]

print("Connecting...")
print(sys.argv)
if len(sys.argv) != 4:
    print("Error on params passed")
    sys.exit(1)
socket_path = sys.argv[1]

images = ["/datagsai/images/"+x for x in os.listdir('/datagsai/images')]

gs_socket = socket_path

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
    image = [x for x in json_data['images']['image_list'] if x['detector'] == 'gsai-xray-v1.2'][0]
    image['file_image_url'] = random.choice(images)
    image['acq_timestamp'] = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
    print(json_data)
    json_data['belt_part'] = sys.argv[3]

    print(json_data)
    client.sendall(json.dumps(json_data).encode())
    client.close()
else:
    print("Couldn't Connect!")
print("Done")
