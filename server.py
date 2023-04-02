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

def service_connection(key, mask):
  sock = key.fileobj
  data = key.data
  if mask & selectors.EVENT_READ:
    recv_data = sock.recv(1024)  # Should be ready to read
    if recv_data:
      # data.outb += recv_data
      print(f"Received {recv_data!r} from connection {data.connid}")
      data.recv_total += len(recv_data)
    if not recv_data or data.recv_total == data.msg_total:
      print(f"Closing connection to {data.addr} aaa {data.connid}")
      selector.unregister(sock)
      sock.close()
  if mask & selectors.EVENT_WRITE:
    if not data.outb:
      data.outb = data.messages.pop(0)

    if data.outb:
      print(f"Echoing {data.outb!r} to {data.addr} aaaa to connection {data.connid}")
      sent = sock.send(data.outb)  # Should be ready to write
      data.outb = data.outb[sent:]

try:
  while True:
    events = selector.select(timeout=None)
    for key, mask in events:
      if key.data is None:
        accept_wrapper(key.fileobj)
      else:
        service_connection(key, mask)
except KeyboardInterrupt:
  print("Caught keyboard interrupt, exiting")
finally:
  selector.close()










""" with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
  serverSocket.bind((HOST, PORT))
  serverSocket.listen()
  clientSocket, clientAddress = serverSocket.accept()

  with clientSocket: # automatically closes socket at the end of block
    print(f"Connected by {clientAddress}")
    while True:
      data = clientSocket.recv(1024) # read data sent by client
      
      clientSocket.sendall(data) # echo data back to client

      if data == b"STOP":
        break
    # end while
  # end with
# end with """
  