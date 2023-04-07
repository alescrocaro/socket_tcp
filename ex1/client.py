import socket
import hashlib


HOST = "127.0.0.1" # localhost
# PORT = 8888 # port used by server
PORT = 4444 # port used by server
# PORT = 7777 # port used by server

# socket.AF_INET = internet address family for ipv4
# socket.SOCK_STREAM = socket type for TCP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))
isAuthenticated = False
buffer = ''

# loop to keep sending messages to server
while True:
  sendData = False # used to manage when the client will send a message to the server
  buffer = input("$ ")
  if buffer != "" and not buffer.isspace(): # only manage input if client is sending something
    command = buffer.split()

    if command[0] == "EXIT":
      print("Closing connection")
      break

    # manage CONNECT command
    if command[0] == "CONNECT":
      if len(command) == 2: # check if the input is in the correct format
        try:
          (username, password) = command[1].split(",")
          if(username != "" and not username.isspace() and password != "" and not password.isspace()):
            hashObject = hashlib.sha512() # create SHA512 hash obj
            hashObject.update(password.encode()) # encode string to bytes and update hash obj with result
            encryptedPassword = hashObject.hexdigest() # get hash as hexadecimal string

            buffer = command[0] + ' ' + username + ',' + encryptedPassword # update message with the encrypted password

            sendData = True
          else:
            print('INPUT ERROR')
            continue

        except:
          print("INPUT ERROR")
          continue

    # manage PWD command
    elif command[0] == "PWD":
      if len(command) == 1: # check if the input is in the correct format
        sendData = True

    # manage CHDIR command
    # Can only change one dir by each command
    elif command[0] == "CHDIR":
      if len(command) == 2: # check if the input is in the correct format
        path = command[1].split("/")
        formattedPath = list(filter(bool, path)) # remove '' elements

        buffer = command[0] + ' ' + formattedPath[0]

        sendData = True

    # manage GETFILES and GETDIRS commands
    elif command[0] == "GETFILES" or command[0] == "GETDIRS":
      if  len(command) == 1: # check if the input is in the correct format
        sendData = True

    else:
      sendData = False

    # manage data sending to server
    if sendData:
      if command[0] == 'CONNECT': # set client authentication
        if isAuthenticated:
          print("Already connected")

        else:
          clientSocket.sendall(buffer.encode())
          data = clientSocket.recv(1024)
          print(f'SERVER RESPONSE: {data.decode()}')
          if data.decode() == 'SUCCESS':
            isAuthenticated = True

      else: # only send other commands to server if client is authenticated
        if isAuthenticated:
          clientSocket.sendall(buffer.encode())

          data = clientSocket.recv(1024)

          print(f'SERVER RESPONSE: {data.decode()}')

        else:
          print("You must be authenticated!")

