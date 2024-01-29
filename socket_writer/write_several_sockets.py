import json
import os
import socket
import time

gs_socket_1 = "/datagsai/socket/gs_socket_1"
gs_socket_2 = "/datagsai/socket/gs_socket_2"

files = ['../' + x for x in os.listdir('..') if x.endswith('.json')]

images = ['/datagsai/images/' + x for x in os.listdir('/datagsai/images/')]


import uuid
from datetime import datetime, timezone
from random import random

i = 0
client_1 = []
client_2 = []
if os.path.exists(gs_socket_1):
    client_1 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_1.connect(gs_socket_1)
else:
    print("Couldn't Connect!")

if os.path.exists(gs_socket_2):
    client_2 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_2.connect(gs_socket_2)
else:
    print("Couldn't Connect!")

while i in range(100):
    print("Writing ", (i + 1))

    file = files[i % len(files)]
    print(file)

    f = open(file)
    json_data = json.load(f)
    json_data['event_timestamp'] = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
    json_data['event_id'] = str(uuid.uuid4())
    json_data['acq_time'] = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    json_data['images']['image_list'][0]['file_image_url'] = random.choice(images)
    print(json_data['event_id'])
    if i%2 == 0:
        json_data['belt_part'] = 'L'
        client_1.send(json.dumps(json_data).encode())
    else:
        json_data['belt_part'] = 'R'
        client_2.send(json.dumps(json_data).encode())

    time.sleep(max(1, int(random() * 10)))
    i = i + 1
client_1.close()
client_2.close()

print("Done")
