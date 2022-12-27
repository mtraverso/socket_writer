import json
import os
import socket
import time

gs_socket = "/Users/matias/gsaidata/socket/gs_socket"

files = ["../json_data_new_schema.json", "../json_data_new_schema_2.json", "../json_data_new_schema_3.json"]
i = 0
while i in range(100):
    if os.path.exists(gs_socket):
        print("Writing ", (i + 1))
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(gs_socket)
        file = files[i % len(files)]

        f = open(file)
        json_data = json.load(f)

        client.send(json.dumps(json_data).encode())
        time.sleep(1)
        client.close()
        i = i + 1

    else:
        print("Couldn't Connect!")

print("Done")
