#!/usr/bin/env python3

import json
import zmq

from dozenos.utils.commit import wait_for_commit_lock
from dozenos.defaults import dozenos_configd_socket_path

context = zmq.Context()

request = {
    'type': 'node',
    'last': True,
    'data': '/usr/libexec/dozenos/conf_mode/protocols_static.py',
}
request = json.dumps(request)

print("Waiting for commit lock...")
wait_for_commit_lock()

print("Connecting to dozenos-configd server...")
socket = context.socket(zmq.REQ)
socket.connect(dozenos_configd_socket_path)

print(f"Sending request {request}...")
socket.send_string(request)

message = socket.recv()
print(f"Received reply {request} [ {message} ]")

print("All done")
