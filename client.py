import socket

HOST = "127.0.0.1" # localhost
PORT = 10666 # port used by server
""" 
# socket.AF_INET = internet address family for ipv4
# socket.SOCK_STREAM = socket type for TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
  clientSocket.connect((HOST, PORT))
  clientSocket.sendall(b"STOP")
  data = clientSocket.recv(1024)
# end with

print(f"Received {data!r}")

 """

# multiconn-client.py

import sys
import selectors
import types
import sys
import socket
import selectors
import types


# used to manage I/O operations on more than one socket
selector = selectors.DefaultSelector()

HOST = "127.0.0.1" # localhost
PORT = 10666
# socket.AF_INET = internet address family for ipv4
# socket.SOCK_STREAM = socket type for TCP
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen()
print(f"Listening on {(HOST, PORT)}")
# set socket to non blocking mode
serverSocket.setblocking(False)
# register the socket to be monitorated
selector.register(serverSocket, selectors.EVENT_READ, data=None)

def accept_wrapper(sock):
  conn, addr = sock.accept()  # Should be ready to read
  print(f"Accepted connection from {addr}")
  conn.setblocking(False)
  data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
  events = selectors.EVENT_READ | selectors.EVENT_WRITE
  selector.register(conn, events, data=data)

try:
  while True:
    events = selector.select(timeout=None)
    for key, mask in events:
      if key.data is None:
        accept_wrapper(key.fileobj)
      else:
        start_connections(key, mask)
except KeyboardInterrupt:
  print("Caught keyboard interrupt, exiting")
finally:
  selector.close()
sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]

def start_connections(host, port, num_conns):
  server_addr = (host, port)
  for i in range(0, num_conns):
    connid = i + 1
    print(f"Starting connection {connid} to {server_addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
      connid=connid,
      msg_total=sum(len(m) for m in messages),
      recv_total=0,
      messages=messages.copy(),
      outb=b"",
    )
    sel.register(sock, events, data=data)

# ...