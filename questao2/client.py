import socket
import os


# the path passed as file name size can not be greater than 9 chars


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

def get_command_name_by_id(command):
  print('get_command_name_by_id command')
  print(command)
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
    
def get_status_code_by_id(status):
  match status:
    case 1:
      return "SUCCESS"
    case 2:
      return "ERROR"
    
    
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

def desestructure_response(response):
  type = response[0:1]
  command_id = int.from_bytes(response[1:2], 'big')
  command_name = get_command_name_by_id(command_id)
  status_id = int.from_bytes(response[2:3], 'big')
  status_code = get_status_code_by_id(status_id)
  file_size = ''
  file_data = ''
  file_list = ''

  if command_name == 'ADDFILE' or command_name == 'GETFILE':
    file_size = int.from_bytes(response[3:4], 'big')
    file_data = response[4:].decode('utf-8')

  elif command_name == 'GETFILESLIST':
    file_list = response[3:].decode('utf-8')

  return type, command_name, status_code, file_size, file_data, file_list

def send_command(client_socket, message):
  print('entrou sendcommand')
  if (message.split()[0] != 'GETFILESLIST'):
    command, file_name = message.split()
  else:
    command = message.split()[0]
    file_name = ''

  header = build_header(command, file_name)
  print('header')
  print(header)
  client_socket.send(header)
  
  response = client_socket.recv(1024)
  
  return response


HOST = "127.0.0.1"
PORT = 4444
# PORT = 7770
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
  message = input("$ ")
  print(f'message {message}')
  if not message:
    continue

  if message.split()[0] in commands:
    response = send_command(client_socket, message)
    print('response')
    print(response)
  
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

      else:
        with open(file_path, "wb") as file:
          file.write(file_data)
    