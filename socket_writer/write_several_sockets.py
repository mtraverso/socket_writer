import json
import os
import socket
import time

sockets = os.listdir('/datagsai/socket')

files = ['../' + x for x in os.listdir('..') if x.endswith('.json')]

images = ['/datagsai/images/' + x for x in os.listdir('/datagsai/images/')]


import uuid
from datetime import datetime, timezone
from random import random

i = 0
clients = []
for socket_no in range(len(sockets)):
    gs_socket = '/datagsai/socket/{}'.format(sockets[int(socket_no)])
    if os.path.exists(gs_socket):
        try:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(gs_socket)
            clients.append(client)
        except ConnectionRefusedError:
            #sockets.remove(sockets[socket_no])
            print("Couldn't connect to socket " + gs_socket)
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
    json_data['belt_part'] = ["F" if i % 2 == 0 else "B"]
    clients[i%2].send(json.dumps(json_data).encode())

    time.sleep(max(1, int(random() * 10)))
    i = i + 1

for client in clients:
    client.close()

print("Done")
