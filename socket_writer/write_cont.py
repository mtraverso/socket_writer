import json
import os
import socket
import time

gs_socket = "/Users/matias/gsaidata/socket/gs_socket"

files = ['../'+x for x in os.listdir('..') if x.endswith('.json')]



import uuid
from datetime import datetime, timezone
from random import random
i = 0
client = []
if os.path.exists(gs_socket):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(gs_socket)
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
    json_data['acq_time'] = int(datetime.now(tz=timezone.utc).timestamp()*1000)
    print(json_data['event_id'])

    client.send(json.dumps(json_data).encode())
    time.sleep(max(1, int(random()*10)))
    i = i + 1
client.close()




print("Done")
