import socket
import os


# the path passed as file name size can not be greater than 9 chars


COMMANDS_ID = [b"0x01", b"0x02", b"0x03", b"0x04"]
REQ_TYPE = "0x01"
RES_TYPE = "0x02"
SUCCESS = "0x01"
ERROR = "0x02"
ADDFILE_ID = "0x01"
DELETE_ID = "0x02"
GETFILESLIST_ID = "0x03"
GETFILE_ID = "0x04"
EXIT_ID = "0x05"



commands = ['ADDFILE', 'DELETE', 'GETFILESLIST', 'GETFILE']

def get_command_id_by_name(command):
  match command:
    case 'ADDFILE':
      return COMMANDS_ID[0]
    case 'DELETE':
      return COMMANDS_ID[1]
    case 'GETFILESLIST':
      return COMMANDS_ID[2]
    case 'GETFILE':
      return COMMANDS_ID[3]

def get_command_name_by_id(command):
  match command:
    case "0x01":
      return 'ADDFILE'

    case "0x02":
      return 'DELETE'
    
    case "0x03":
      return 'GETFILESLIST'
    
    case "0x04":
      return 'GETFILE'
    
    case "0x05":
      return 'EXIT'
    
def get_status_code_by_id(status):
  match status:
    case "0x01":
      return "SUCCESS"
    case "0x02":
      return "ERROR"
    
    
def build_header(command, file_name):  
  header = REQ_TYPE.encode()
  header += get_command_id_by_name(command) # command id

  if command in ['ADDFILE', 'DELETE', 'GETFILES']:
    file_name = message.split()[1]
  
  else:
    file_name = ''

  text_with_zeros = str(len(file_name)).zfill(4)
  header += text_with_zeros.encode() # file name size
  header += bytes(file_name, 'utf-8') # file name in bytes

  return header

def desestructure_response(response):
  response = response.decode()
  type = RES_TYPE
  command_name = get_command_name_by_id(response[4:8])
  status_code = get_status_code_by_id(response[8:12])

  return type, command_name, status_code

def send_command(client_socket, message):
  print('entrou sendcommand')
  command, file_name = message.split()

  header = build_header(command, file_name)
  print('header')
  print(header)
  client_socket.send(header)

  if command == "ADDFILE":
    data = b""
    try:
      with open(file_name, 'rb') as file:
        data = file.read()

      client_socket.send(data)

    except Exception as e:
      print(f"Error adding file: {e}")

  # else:
  #   print(header)
  #   client_socket.send(header)
  #   return
  response = client_socket.recv(1024)
  
  return response



HOST = "127.0.0.1"
PORT = 4444
# PORT = 7777
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
  message = input("$ ")
  print(f'message {message}')
  if not message:
    continue

  if message.split()[0] in commands:
    response = send_command(client_socket, message)
  
  _, command_name, status_code = desestructure_response(response)

  print(f'{command_name} returned: {status_code}')
  if command_name == "EXIT":
    print('Closing connection')
    break 
  