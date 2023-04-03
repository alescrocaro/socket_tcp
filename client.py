import sys
import socket
import selectors
import types
import hashlib

HOST = "127.0.0.1" # localhost
PORT = 4444 # port used by server
# PORT = 7777 # port used by server


# socket.AF_INET = internet address family for ipv4
# socket.SOCK_STREAM = socket type for TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
  clientSocket.connect((HOST, PORT))
  # message = sys.argv[1]
  message = ''
  while message != "EXIT":
    sendData = False
    message = input("$ ")
    if message != "" and not message.isspace():
      if message.startswith("CONNECT"):
        command = message.split(" ")
        if command[0] == "CONNECT":
          print(f'len(command) {len(command)}')
          if len(command) == 2:
            try:
              (username, password) = command[1].split(",")
              if(username != "" and not username.isspace() and password != "" and not password.isspace()):
                print(username, password)
                hashObject = hashlib.sha512() # create SHA512 hash obj
                hashObject.update(password.encode()) # encode string to bytes and update hash obj with result
                hexDig = hashObject.hexdigest() # get hash as hexadecimal string

                print(f"Hash SHA-512 de '{password}': {hexDig}")

                message = command[0] + ' ' + username + ',' + hexDig # update message with the encrypted password

                sendData = True

            except:
              print("INPUT ERROR")
              sendData = False

      else: 
        sendData = True

      if sendData:
        print("ENVIOU PRO SERVER")
        clientSocket.sendall(message.encode())
        
        data = clientSocket.recv(1024)
    
        print(f'SERVER RESPONSE: {data.decode()}')
  # end while
# end with
