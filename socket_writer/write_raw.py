from datetime import datetime, timezone
import os
import socket
import json
import sys
import uuid
from uuid import UUID
from datetime import datetime

file_1 = '../files_old/json_data_passed_2_msgs.json_err'
file_2 = '../files_old/json_data_passed_2_msgs_2.json_err'

print("Connecting...")
gs_socket = "/datagsai/socket/gs_socket"
if os.path.exists(gs_socket):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(gs_socket)
    print("Ready.")
    print("Ctrl-C to quit.")
    print("Sending 'DONE' shuts down the server and quits.")
    f = open(file_1)

    client.send(f.read().encode())
    f = open(file_2)

    client.send(f.read().encode())
    client.close()
else:
    print("Couldn't Connect!")
print("Done")
