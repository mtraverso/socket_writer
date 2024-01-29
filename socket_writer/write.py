import random
from datetime import datetime, timezone
import os
import socket
import json
import sys
import uuid
from uuid import UUID
from datetime import datetime

from socket_writer.utils import list_files_by_extension, set_image

print("Connecting...")
sockets = os.listdir('/datagsai/socket')

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

images = list_files_by_extension('/datagsai/images', '.png')
images.extend(list_files_by_extension('/datagsai/images', '.jpg'))

dirs = ["passed"]
files = []
for dir in dirs:
    for f in list_files_by_extension('../files/'+dir+"/", ".json"):
        files.append("../files/"+dir+"/"+f)
print(files)

belts = ['F', 'B']

client = random.choice(clients)
print("Ready.")
print("Ctrl-C to quit.")
print("Sending 'DONE' shuts down the server and quits.")
file = random.choice(files)
f = open(file)
json_data = json.load(f)
json_data['event_id'] = str(uuid.uuid4())
json_data['event_timestamp'] = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
json_data['images']['image_list'][0]['file_image_url'] = random.choice(images)
#json_data['acq_time'] = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
print(json_data)
set_image(json_data, images)
json_data['acq_time'] = int(datetime.now().timestamp()*1000)
json_data['belt_part'] = random.choice(belts)
client.send(json.dumps(json_data).encode())
client.close()

print("Done")
