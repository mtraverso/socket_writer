import json
import os
import socket
import time

gs_socket = "/datagsai/socket/gs_socket"

files = ["../json_data_new_schema_one_fm.json", "../json_data_new_schema_two_fm_same_type.json", "../json_data_new_schema_only_ai.json", "../json_data_new_schema.json"]
import uuid
from datetime import datetime
from uuid import UUID

i = 0
while i in range(100):
    if os.path.exists(gs_socket):
        print("Writing ", (i + 1))
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(gs_socket)
        file = files[i % len(files)]

        f = open(file)
        json_data = json.load(f)
        json_data['event_timestamp'] = datetime.now()
        json_data['event_id'] = str(uuid.uuid4())

        client.send(json.dumps(json_data).encode())
        time.sleep(1)
        client.close()
        i = i + 1

    else:
        print("Couldn't Connect!")

print("Done")
