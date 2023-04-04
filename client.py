import sys
import socket
import selectors
import types
import hashlib

HOST = "127.0.0.1" # localhost
# PORT = 8888 # port used by server
PORT = 4444 # port used by server
# PORT = 7778 # port used by server


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
      command = message.split()
      if message.startswith("CONNECT"):
        if command[0] == "CONNECT":
          if len(command) == 2:
            try:
              (username, password) = command[1].split(",")
              if(username != "" and not username.isspace() and password != "" and not password.isspace()):
                hashObject = hashlib.sha512() # create SHA512 hash obj
                hashObject.update(password.encode()) # encode string to bytes and update hash obj with result
                encryptedPassword = hashObject.hexdigest() # get hash as hexadecimal string

                message = command[0] + ' ' + username + ',' + encryptedPassword # update message with the encrypted password

                sendData = True

            except:
              print("INPUT ERROR")
              sendData = False

      elif message.startswith("PWD"):
        if len(command) == 1 and command[0] == "PWD": 
          sendData = True

      # Can not start with "/"
      # Can only change one dir by each command
      elif message.startswith("CHDIR"):
        if len(command) == 2 and command[0] == "CHDIR":
          path = command[1].split("/")
          formattedPath = list(filter(bool, path))
          
          message = command[0] + ' ' + formattedPath[0]

          sendData = True

      elif message.startswith("GETFILES"):
        if command[0] == "GETFILES" and len(command) == 1:
          sendData = True  

      elif message.startswith("GETDIRS"):
        if command[0] == "GETDIRS" and len(command) == 1:
          sendData = True  

      else: 
        sendData = False

      if sendData:
        clientSocket.sendall(message.encode())
        
        data = clientSocket.recv(1024)
    
        print(f'SERVER RESPONSE: {data.decode()}')
  # end while
# end with
