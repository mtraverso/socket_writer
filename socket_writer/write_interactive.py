import json
import os
import socket
import uuid
from datetime import datetime, timezone

from socket_writer.utils import list_files_by_extension, set_image

sockets = os.listdir('/datagsai/socket')
images = list_files_by_extension('/datagsai/images', '.png')
images.extend(list_files_by_extension('/datagsai/images', '.jpg'))
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

while True:
    if len(clients) > 1:
        socket_no = input("Select socket to use: [0-{}]: ".format(len(sockets)-1))
        if socket_no == 'q':
            break
        if socket_no == '':
            continue
        if int(socket_no) > len(clients)-1:
            continue
    else:
        socket_no = 0

    dirs = os.listdir('../files')
    for i in range(0, len(dirs)):
        print("{}: {}".format(i, dirs[i]))
    dir = input("Select dir to use: [0-{}]: ".format(len(dirs) - 1))
    if dir == 'q':
        break
    if dir == '':
        continue
    files = list_files_by_extension("../files/"+dirs[int(dir)], ".json")
    file_no = 0
    if len(files) > 1:
        for i in range(0, len(files)):
            print("{}: {}".format(i, files[i]))
        file_no = input("Select file to use: [0-{}]: ".format(len(files) - 1))
    print(files[int(file_no)])
    f = open("../files/"+dirs[int(dir)]+"/"+files[int(file_no)])
    json_data = json.load(f)
    json_data['event_id'] = str(uuid.uuid4())
    json_data['event_timestamp'] = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
    set_image(json_data, images)

    json_data['acq_time'] = int(datetime.now().timestamp()*1000)
    if len(clients) > 1:
        if int(socket_no) == 0:
            json_data['belt_part'] = 'L'
        else:
            json_data['belt_part'] = 'R'
    print(json_data)
    clients[int(socket_no)].send(json.dumps(json_data).encode())


