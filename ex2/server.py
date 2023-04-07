###########################################################################
# Description: This code is used to manage a connection with the client   #
#              using tcp sockets and threads. It process the commands     #
#              ADDFILE, DELETE, GETFILESLIST and GETFILE, make the needed #
#              processes send a response to the client                    #
#                                                                         #
# Authors: Alexandre Aparecido Scrocaro Junior, Pedro Klayn               #
#                                                                         #
# Dates: github.com/alescrocaro/socket_tcp                                #
#                                                                         #
###########################################################################


import socket
import threading
import os
import logging

# config logger
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
  
REQ = 1
RES = 2
SUCCESS = 1
ERROR = 2
ADDFILE_ID = 1
DELETE_ID = 2
GETFILESLIST_ID = 3
GETFILE_ID = 4
EXIT_ID = 5

# wait for client request and calls the requested functionality, if there is 
# some error, closes connection with client
# client_socket = client socket used to send response
# client_address = client address used to know who made the request
def handle_connection(client_socket, client_address):
  while True:
    try:
      print('Reading client request')
      data = client_socket.recv(1024)
      message_type = data[0:1]
      command_id = data[1:2]
      file_name_size = data[2:3]
      file_name_size = int.from_bytes(file_name_size, 'big')
      last_pos_of_name = (3 + file_name_size)
      file_name = data[3:last_pos_of_name]

      if not data:
        logging.error("No data")
        print("No data")
        break

      if message_type == REQ.to_bytes(1, 'big'):
        file_name = file_name.decode('utf8')
        if command_id == ADDFILE_ID.to_bytes(1, 'big'):
          print('COMMAND: ADDFILE')
          handle_ADDFILE(client_socket, file_name, client_address)
        elif command_id == DELETE_ID.to_bytes(1, 'big'):
          print('COMMAND: DELETE')
          handle_DELETE(client_socket, file_name, client_address)
        
        elif command_id == GETFILE_ID.to_bytes(1, 'big'):
          print('COMMAND: GETFILE')
          handle_GETFILE(client_socket, file_name, client_address)
        
        elif command_id == GETFILESLIST_ID.to_bytes(1, 'big'):
          print('COMMAND: GETFILESLIST')
          handle_GETFILESLIST(client_socket, client_address)

      else:
        logging.error(f"Something went wrong...")
        print('Something went wrong...')
        continue

    except Exception as e:
      logging.error(f"Error while handling connection: {e}")
      print(f"Error while handling connection: {e}")
      break

  print("Closing connection")
  client_socket.close()

# upload a file in files_server, if it doesnt exists already and return a response
# to the client
# client_socket = socket used to send the message to the client
# file_name = relative path of the file name the client is tryng to add to the server
# client_address = client address used to know who made the request
def handle_ADDFILE(client_socket, file_name, client_address):
  response =  RES.to_bytes(1, 'big')
  response +=  ADDFILE_ID.to_bytes(1, 'big')
  name = file_name.split('/')[-1]
  files_path = './files_server/'
  file_path = os.path.join(files_path, name)

  if os.path.exists(file_path):
    response += ERROR.to_bytes(1, 'big')
    client_socket.send(response)
    print(f"File {name} already exists")
    logging.error(f"File {name} already exists")

  else:
    file_size = os.path.getsize(file_name)
    try: 
      with open(file_name, 'rb') as file:
        data = file.read()

      with open(file_path, "wb") as file:
        file.write(data)

    except:
      print('Error trying to write file')
      logging.error('Error trying to write file')
      response += ERROR.to_bytes(1, 'big')
      client_socket.send(response)

    response += SUCCESS.to_bytes(1, 'big')
    response += file_size.to_bytes(4, 'big')
    response += data
    client_socket.send(response)
    print(f"File '{name}' added by {client_address}")
    logging.info(f"File '{name}' added by {client_address}")

# deletes the file the client wants if it exists (the client cant send the file_name with a 
# '/' in first position) and return response to the client
# client_socket = socket used to send the message to the client
# file_name = relative path of the file
# client_address = client address used to know who made the request
def handle_DELETE(client_socket, file_name, client_address):
  response =  RES.to_bytes(1, 'big')
  response +=  DELETE_ID.to_bytes(1, 'big')
  file_path = file_name
  if (not file_path.startswith('./')):
    file_path = './' + file_path

  print (file_path)
  if not os.path.exists(file_path):
    response += ERROR.to_bytes(1, 'big')
    client_socket.send(response)
    print(f"File {file_name} does not exists")
    logging.error(f"File {file_name} does not exists")

  else:
    try:
      os.remove(file_path)
      logging.info(f"File '{file_name}' deleted by {client_address}")
      print(f"File '{file_name}' deleted by {client_address}")
      response += SUCCESS.to_bytes(1, 'big')
      client_socket.send(response)
    except:
      response += ERROR.to_bytes(1, 'big')
      client_socket.send(response)
      logging.error(f"Error tryng to delete file '{file_name}' by {client_address}")


# download the requested file -> copy a file that exists in files_server to 
# files_client and return a response to the client
# client_socket = socket used to send the message to the client
# file_name = file name that exists in files_server folder
# client_address = client address used to know who made the request
def handle_GETFILE(client_socket, file_name, client_address):
  response =  RES.to_bytes(1, 'big')
  response += GETFILE_ID.to_bytes(1, 'big')
  file_path = './files_server/' + file_name
  if not os.path.exists(file_path):
    response += ERROR.to_bytes(1, 'big')
    client_socket.send(response)
    print(f"File {file_name} does not exists")
    logging.error(f"File {file_name} does not exists")

  else:
    try: 
      print('before open file')
      with open(file_path, 'rb') as file:
        data = file.read()
      print('after open file')

      file_size = os.path.getsize(file_path)
      print('file_size')
      print(file_size)

      response += SUCCESS.to_bytes(1, 'big')
      response += file_size.to_bytes(4, 'big')
      response += data
      client_socket.send(response)
      logging.info(f"File {file_name} sent to client: {client_address}")

    except:
      response += ERROR.to_bytes(1, 'big')
      client_socket.send(response)
      logging.error(f"Error tryng to send {file_name}")
      print(f"Error tryng to send {file_name}")

# get all the files in files_server dir and return to the client
# client_socket = socket used to send the message to the client
# client_address = client address used to know who made the request
def handle_GETFILESLIST(client_socket, client_address):
  response = RES.to_bytes(1, 'big')
  response += GETFILESLIST_ID.to_bytes(1, 'big')

  try:
    file_list = os.listdir('./files_server')
    response += SUCCESS.to_bytes(1, 'big')
    for file_name in file_list:
      response += len(file_name).to_bytes(2, 'big')
      response += bytes(file_name, 'utf-8')

    logging.info(f"Sending files list to {client_address}")
    print(f"Sending files list to {client_address}")
    print("response SUCCESS get file list")
    print(response)
    client_socket.send(response)

  except:
    response += ERROR.to_bytes(1, 'big')
    client_socket.send(response)
    logging.error(f"Error tryng to get files list for {client_address}")
    print(f"Error tryng to get files list for {client_address}")



HOST = "127.0.0.1"
PORT = 4444
PORT = 7770
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
logging.info(f"Listening on {HOST}:{PORT}")
print(f"Listening on {HOST}:{PORT}")
while True:
  client_connection, client_address = server_socket.accept()
  logging.info(f"Accepted connection from {client_address}")
  print(f"Accepted connection from {client_address}")
  client_thread = threading.Thread(target=handle_connection, args=(client_connection, client_address))
  client_thread.start()
