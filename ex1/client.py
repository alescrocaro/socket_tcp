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

while True:
  sendData = False
  buffer = input("$ ")
  if buffer != "" and not buffer.isspace():
    command = buffer.split()

    if command[0] == "EXIT":
      print("Closing connection")
      break

    if command[0] == "CONNECT":
      if len(command) == 2:
        try:
          (username, password) = command[1].split(",")
          if(username != "" and not username.isspace() and password != "" and not password.isspace()):
            print('TESTE')
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

    elif command[0] == "PWD":
      if len(command) == 1:
        sendData = True

    # Can not start with "/"
    # Can only change one dir by each command
    elif command[0] == "CHDIR":
      if len(command) == 2:
        path = command[1].split("/")
        formattedPath = list(filter(bool, path))

        buffer = command[0] + ' ' + formattedPath[0]

        sendData = True

    elif command[0] == "GETFILES" or command[0] == "GETDIRS":
      if  len(command) == 1:
        sendData = True

    else:
      sendData = False

    if sendData:
      if command[0] == 'CONNECT':
        if isAuthenticated:
          print("Already connected")

        else:
          clientSocket.sendall(buffer.encode())
          data = clientSocket.recv(1024)
          print(f'SERVER RESPONSE: {data.decode()}')
          if data.decode() == 'SUCCESS':
            isAuthenticated = True

      else:
        if isAuthenticated:
          clientSocket.sendall(buffer.encode())

          data = clientSocket.recv(1024)

          print(f'SERVER RESPONSE: {data.decode()}')

        else:
          print("You must be authenticated!")

