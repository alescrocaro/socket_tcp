###########################################################################
# Description: This code is used to make a connection to the server using #
#              tcp sockets. It process the commands ADDFILE, DELETE,      #
#              GETFILESLIST and GETFILE by command line and send to the   #
#              server, defined by the variables HOST and PORT.            #
#                                                                         #
# Authors: Alexandre Aparecido Scrocaro Junior, Pedro Klayn               #
#                                                                         #
# Dates: github.com/alescrocaro/socket_tcp                                #
#                                                                         #
###########################################################################

import socket
import os

REQ = 1
RES = 2
SUCCESS = 1
ERROR = 2
ADDFILE_ID = 1
DELETE_ID = 2
GETFILESLIST_ID = 3
GETFILE_ID = 4
EXIT_ID = 5

commands = ['ADDFILE', 'DELETE', 'GETFILESLIST', 'GETFILE']

# check the text command and returns its id 
# command = command the client inputs ('ADDFILE', 'DELETE', 'GETFILESLIST', 
# 'GETFILE', 'EXIT')
# return = command id
def get_command_id_by_name(command):
  match command:
    case 'ADDFILE':
      return ADDFILE_ID
    case 'DELETE':
      return DELETE_ID
    case 'GETFILESLIST':
      return GETFILESLIST_ID
    case 'GETFILE':
      return GETFILE_ID
    case 'EXIT':
      return EXIT_ID

# check the id command and returns it in message type
# command = command the client inputs (1, 2 , 3, 4, 5)
# return = command message
def get_command_name_by_id(command):
  match command:
    case 1:
      return 'ADDFILE'

    case 2:
      return 'DELETE'
    
    case 3:
      return 'GETFILESLIST'
    
    case 4:
      return 'GETFILE'
    
    case 5:
      return 'EXIT'
    
# check the status code and returns it in message type
# command = status returned by server (1, 2)
# return = status message
def get_status_code_by_id(status):
  match status:
    case 1:
      return "SUCCESS"
    case 2:
      return "ERROR"
    
# build the header that will be sent in commom by all requests
# command = command inputed by the client in message type ('ADDFILE', 'DELETE', 
# 'GETFILE', 'GETFILESLIST')
# file_name = file name that will be sent to server if command is not GETFILESLIST
# return = header builded
def build_header(command, file_name):  
  header = REQ.to_bytes(1, 'big')
  header += get_command_id_by_name(command).to_bytes(1, 'big') # command id

  if command in ['ADDFILE', 'DELETE', 'GETFILE']:
    file_name = message.split()[1]
  
  else:
    file_name = ''

  header += len(file_name).to_bytes(1, 'big') # file name size
  header += bytes(file_name, 'utf-8') # file name in bytes

  return header

# get the response and splits it into each info sent by the server
# response = the server response to the client request
# return = each info sent by the server in response
def desestructure_response(response):
  message_type = response[0:1]
  command_id = int.from_bytes(response[1:2], 'big')
  command_name = get_command_name_by_id(command_id)
  status_id = int.from_bytes(response[2:3], 'big')
  status_code = get_status_code_by_id(status_id)
  file_size = ''
  file_data = b''
  file_list = ''

  if command_name == 'ADDFILE' or command_name == 'GETFILE':
    file_size = int.from_bytes(response[3:7], 'big')
    file_data = response[7:]

  elif command_name == 'GETFILESLIST':
    file_list = response[3:].decode('utf-8')

  return message_type, command_name, status_code, file_size, file_data, file_list

# send the command inputed by client to the server
# client_socket = connection made with server by the client
# message = command input by the client
# return = response sent by the server
def send_command(client_socket, message):
  if (message.split()[0] != 'GETFILESLIST'):
    command, file_name = message.split()
  else:
    command = message.split()[0]
    file_name = ''

  header = build_header(command, file_name)
  client_socket.send(header)

  response = client_socket.recv(2**32)
  
  return response


HOST = "127.0.0.1"
PORT = 4444
PORT = 7770
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# client connection loop, it will run until client send 'EXIT' 
while True:
  message = input("$ ")

  if not message:
    continue

  if message.split()[0] in commands:
    response = send_command(client_socket, message)
  
    _, command_name, status_code, file_size, file_data, file_list = desestructure_response(response)

    print(f'{command_name} returned: {status_code}')
    print('file_size')
    print(file_size)
    print('file_data')
    print(file_data)
    print('file_list')
    print(file_list)
    if command_name == "EXIT":
      print('Closing connection')
      break 

    if command_name == "GETFILE":
      file_name = message.split()[-1]
      file_path = './files_client/' + file_name
      if os.path.exists(file_path):
        print(f"File {file_name} already exists")

      elif status_code == 'SUCCESS':
        with open(file_path, "wb") as file:
          file.write(file_data)
    