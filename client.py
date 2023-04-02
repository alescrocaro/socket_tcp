import sys
import socket
import selectors
import types

HOST = "127.0.0.1" # localhost
PORT = 10667 # port used by server


# socket.AF_INET = internet address family for ipv4
# socket.SOCK_STREAM = socket type for TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
  clientSocket.connect((HOST, PORT))
  message = sys.argv[1]
  print(message)
  while message != "EXIT":
    message = input("$ ")
    # message = message[2:]
    print(message)
    clientSocket.sendall(message.encode())
    data = clientSocket.recv(1024)
# end with

print(f"Received {data!r}")
