import sys
import socket
import selectors
import time
import types
import json

# used to manage I/O operations on more than one socket
selector = selectors.DefaultSelector()

HOST = "127.0.0.1" # localhost
PORT = 4444
# PORT = 7777

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
  socket, clientAddress = sock.accept()  # Should be ready to read
  print(f"Accepted connection from {clientAddress}")
  socket.setblocking(False)
  data = types.SimpleNamespace(addr=clientAddress, inb=b"", outb=b"")
  events = selectors.EVENT_READ | selectors.EVENT_WRITE
  selector.register(socket, events, data=data)


def service_connection(key, mask):
  serverSocket = key.fileobj
  data = key.data

  if mask & selectors.EVENT_READ:
    print('LEITURAAAAAAAAAAAAA')
    print()
    recv_data = serverSocket.recv(1024)  # Should be ready to read

    if recv_data:
      data.outb += recv_data
      print(f'data {data}')
      print(f'recv_data {recv_data}')
      print()

      if recv_data == b"EXIT":
        print(f"Closing connection to {data.addr}")
        print()
        selector.unregister(serverSocket)
        serverSocket.close()
        return

      command = recv_data.split(b" ")
      print(command)

      if command[0] == b"CONNECT":
        try:
          (username, password) = command[1].split(b",")

          decodedUsername = username.decode("utf-8")
          decodedPassword = password.decode("utf-8")

          with open('users.json') as file:
            users = json.load(file)['users']

          for user in users:
            print(user)
            if user['username'] == decodedUsername and user['password'] == decodedPassword:
              print('User authenticated.')
              data.outb = b"SUCCESS"
              break

          else:  # this else points to 'for' loop
            print('Invalid username or password.')
            data.outb = b"ERROR"
            # Should be ready to write
            sent = serverSocket.send(data.outb)
            data.outb = data.outb[sent:]

          print(users)

          print(decodedUsername, decodedPassword)
          print()

        except:
          data.outb = b"ERROR"
          sent = serverSocket.send(data.outb) # Should be ready to write
          data.outb = data.outb[sent:]

    else:
      print(data)
      print(f"Closing connection to {data.addr}")
      print()
      selector.unregister(serverSocket)
      serverSocket.close()

  if mask & selectors.EVENT_WRITE:
    print('ESCRITAAAAAAAAAAAAAA')
    if data.outb:
      print(f"Echoing {data.outb!r} to {data.addr}")
      print()
      sent = serverSocket.send(data.outb)  # Should be ready to write
      data.outb = data.outb[sent:]


try:
  while True:
    # blocks until there are sockets ready for I/O (like listen)
    events = selector.select(timeout=None)
    print('events')
    print()
    for key, mask in events:
      print('ENTROU FOR')
      print()
      if key.data is None:
        print(' accept_wrapper')
        print()
        time.sleep(1)
        accept_wrapper(key.fileobj)

      else:
        print(f'service_connection')
        print()
        time.sleep(1)
        # mask = event mask of the operations that are ready.
        # key = SelectorKey namedtuple. We will use just fileObj (socket) and data (data sent from client)
        service_connection(key, mask)

except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")

finally:
    selector.close()
