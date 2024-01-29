import json
import os
import socket
import time

from socket_writer.utils import list_files_by_extension, set_image

sockets = os.listdir('/datagsai/socket')


#dirs = os.listdir('../files')
dirs = ["passed"]
files = []
for dir in dirs:
    for f in list_files_by_extension('../files/'+dir+"/", ".json"):
        files.append("../files/"+dir+"/"+f)
print(files)


#files = ["../json_data_new_schema_one_fm.json", "../json_data_new_schema_two_fm_same_type.json", "../json_data_new_schema_only_ai.json", "../json_data_new_schema.json", "../json_data_passed.json"]

import uuid
from datetime import datetime
import random
i = 0
clients = []
for socket_no in range(len(sockets)):
    gs_socket = '/Users/matias/gsaidata/socket/{}'.format(sockets[int(socket_no)])

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

belts = ['L', 'R']

try:
    begin = datetime.now()
    while i in range(25000):
        client = random.choice(clients)
        print("Writing ", (i + 1))
        file = random.choice(files)
        print(file)
        f = open(file)
        json_data = json.load(f)
        json_data['event_timestamp'] = str(datetime.now())

        json_data['acq_time'] = int(datetime.now().timestamp()*1000)
        json_data['event_id'] = str(uuid.uuid4())
        json_data['belt_part'] = random.choice(belts)
        set_image(json_data, images)

        client.send(json.dumps(json_data).encode())
        #time.sleep(0.019)
        #time.sleep(0.03)
        i = i + 1

    end = datetime.now()
    print("Ran for "+str((end-begin).total_seconds())+ " seconds")
finally:
    for client in clients:
        client.close()
print("Done")
