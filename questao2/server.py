import sys
import socket
import selectors
import time
import types
import json
import os

def accept_wrapper(sock):
  socket, clientAddress = sock.accept()  # Should be ready to read
  print(f"Accepted connection from {clientAddress}")
  socket.setblocking(False)
  data = types.SimpleNamespace(addr=clientAddress, inb=b"", outb=b"")
  events = selectors.EVENT_READ | selectors.EVENT_WRITE
  selector.register(socket, events, data=data)


def service_connection(key, mask):
  currentPath = os.getcwd()
  serverSocket = key.fileobj
  data = key.data

  if mask & selectors.EVENT_READ:
    recv_data = serverSocket.recv(1024)  # Should be ready to read

    if recv_data:
      data.outb += recv_data

      if recv_data == b"EXIT":
        print(f"Closing connection to {data.addr}")
        selector.unregister(serverSocket)
        serverSocket.close()
        return

      command = recv_data.split(b" ")

      if command[0] == b"CONNECT":
        try:
          (username, password) = command[1].split(b",")

          decodedUsername = username.decode("utf-8")
          decodedPassword = password.decode("utf-8")

          with open('users.json') as file:
            users = json.load(file)['users']

          for user in users:
            if user['username'] == decodedUsername and user['password'] == decodedPassword:
              data.outb = b"SUCCESS"
              break

          else:  # this else points to 'for' loop
            data.outb = b"ERROR"
            sent = serverSocket.send(data.outb) # Should be ready to write
            data.outb = data.outb[sent:]

        except:
          data.outb = b"ERROR"
          sent = serverSocket.send(data.outb) # Should be ready to write
          data.outb = data.outb[sent:]

      elif command[0] == b"PWD":
        try:
          print(f"path {currentPath}")
          data.outb = currentPath.encode()

        except:
          data.outb = b"ERROR"
          sent = serverSocket.send(data.outb) # Should be ready to write
          data.outb = data.outb[sent:]


      elif command[0] == b"CHDIR":
        try:
          os.chdir(command[1])
          currentPath = os.path.abspath(os.getcwd())
          data.outb = b"SUCCESS"

        except:
          data.outb = b"ERROR"
          sent = serverSocket.send(data.outb) # Should be ready to write
          data.outb = data.outb[sent:]

      elif command[0] == b"GETFILES":
        try:
          files = os.listdir(currentPath)
          data.outb = (str(len(files)) + '\n').encode()
          # sent = serverSocket.send(data.outb)
          # data.outb = b""
          for file in files:
            data.outb += (file + "\n").encode()
          sent = serverSocket.send(data.outb)
          data.outb = b""

        except:
          data.outb = b"ERROR"
          sent = serverSocket.send(data.outb)
          data.outb = data.outb[sent:]

      elif command[0] == b"GETDIRS":
        try:
          dirs_only = [file for file in os.listdir() if os.path.isdir(file)]
          data.outb = (str(len(dirs_only)) + '\n').encode()
          # sent = serverSocket.send(data.outb)
          # data.outb = b""
          for dir in dirs_only:
            data.outb += (dir + "\n").encode()
          sent = serverSocket.send(data.outb)
          data.outb = b""

        except:
          data.outb = b"ERROR"
          sent = serverSocket.send(data.outb)
          data.outb = data.outb[sent:]

    else:
      print(f"Closing connection to {data.addr}")
      selector.unregister(serverSocket)
      serverSocket.close()

  if mask & selectors.EVENT_WRITE:
    if data.outb:
      print(f"Echoing {data.outb!r} to {data.addr}")
      sent = serverSocket.send(data.outb)  # Should be ready to write
      data.outb = data.outb[sent:]

#####
#####
#####

# used to manage I/O operations on more than one socket
selector = selectors.DefaultSelector()

HOST = "127.0.0.1" # localhost
PORT = 4444
# PORT = 7778

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


try:
  while True:
    # blocks until there are sockets ready for I/O (like listen)
    events = selector.select(timeout=None)
    for key, mask in events:
      if key.data is None:
        # key.fileobj = socket
        accept_wrapper(key.fileobj)

      else:
        # mask = event mask of the operations that are ready.
        # key = SelectorKey namedtuple. We will use just fileObj (socket) and data (data sent from client)
        service_connection(key, mask)
      
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")

finally:
    selector.close()
