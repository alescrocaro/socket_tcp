import socket
import os


REQ_TYPE = b"0x01"
COMMANDS_ID = [b"0x01", b"0x02", b"0x03", b"0x04"]

commands = ['ADDFILE', 'DELETE', 'GETFILESLIST', 'GETFILE']

def get_command_id(command):
  match command:
    case 'ADDFILE':
      return COMMANDS_ID[0]
    case 'DELETE':
      return COMMANDS_ID[1]
    case 'GETFILESLIST':
      return COMMANDS_ID[2]
    case 'GETFILE':
      return COMMANDS_ID[3]
    
def build_header(command, file_name):  
  header = REQ_TYPE
  header += get_command_id(command) # command id

  if command in ['ADDFILE', 'DELETE', 'GETFILES']:
    file_name = message.split()[1]
  
  else:
    file_name = ''
  text_with_zeros = str(len(file_name)).zfill(4)
  header += text_with_zeros.encode() # file name size
  header += bytes(file_name, 'utf-8') # file name in bytes

  return header

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
  response = client_socket.recv(1024).decode()
  print(response)


HOST = "127.0.0.1"
PORT = 4444
PORT = 7777
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
  message = input("$ ")
  print(f'message {message}')
  if not message:
    continue

  if message.split()[0] in commands:
    send_command(client_socket, message)
  
  