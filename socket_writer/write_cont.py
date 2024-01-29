import json
import os
import socket
import time

gs_socket = "/datagsai/socket/gs_socket"

files = ['../'+x for x in os.listdir('..') if x.endswith('.json')]

import uuid
from datetime import datetime
from uuid import UUID

import uuid
from datetime import datetime, timezone
from random import random, randint
i = 0
client = []

image_list = ['/datagsai/images/image_0_0_c216ae3a-d587-4bd7-9366-98324aaba325', '/datagsai/images/image_7_0_8f47def8-c8da-4fd9-8814-7ab79d696c26', '/datagsai/images/image_7_0_8f47def8-c8da-4fd9-8814-7ab79d696c25', '/datagsai/images/image_7_0_8f47def8-c8da-4fd9-8814-7ab79d696c27', '/datagsai/images/SS_FM0000000000_32F_b2.out.png', '/datagsai/images/SS_FM0000000001_32F_b2.out.png', '/datagsai/images/SS_FM0000000023_32F_b2.out.png', '/datagsai/images/test_image_1.jpg', '/datagsai/images/test_image_2.jpg']
begin = datetime.now()
if os.path.exists(gs_socket):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(gs_socket)
else:
    print("Couldn't Connect!")
while i in range(1400):
    if os.path.exists(gs_socket):
        print("Writing ", (i + 1))
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(gs_socket)
        file = files[i % len(files)]

        f = open(file)
        json_data = json.load(f)
        json_data['event_timestamp'] = str(datetime.now())
        json_data['acq_time'] = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
        json_data['event_id'] = str(uuid.uuid4())
        print(json_data['event_id'] + " "+file)
        json_data['images']['image_list'][0]['file_image_url'] = image_list[randint(0, len(image_list)-1)]

        client.send(json.dumps(json_data).encode())
        time.sleep(0.25)
        client.close()
        i = i + 1

    else:
        print("Couldn't Connect!")
finish = datetime.now()

difference = finish-begin
total_seconds = difference.total_seconds()

print("Running for "+ str(total_seconds)+" secs")

print("Done")
