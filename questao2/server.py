import socket
import threading
import os
import logging

# config logger
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
  
REQ_TYPE = "0x01"
RES_TYPE = "0x02"
SUCCESS = "0x01"
ERROR = "0x02"
ADDFILE_ID = "0x01"
DELETE_ID = "0x02"
GETFILESLIST_ID = "0x03"
GETFILE_ID = "0x04"
EXIT_ID = "0x05"

def handle_connection(client_socket, client_address):
  print(f'client_socket', client_socket)
  print(f'client_address', client_address)
  global response

  while True:
    try:
      print('teste')
      data = client_socket.recv(258).decode()
      print('data')
      print(data)
      req_type = data[0:4]
      print('req_type')
      print(req_type)
      command_id = data[4:8]
      print('command_id')
      print(command_id)
      file_name_size = data[8:12]
      file_name_size = int(file_name_size)
      print('file_name_size')
      print(file_name_size)
      last_pos_of_name = (12 + file_name_size)
      file_name = data[12:last_pos_of_name]
      print('file_name')
      print(file_name)

      if not data:
        logging.error("No data")
        print("No data")
        break

      print('command')
      if req_type == REQ_TYPE:
        if command_id == ADDFILE_ID:
          print('COMMAND: ADDFILE')
          handle_ADDFILE(client_socket, file_name)
        elif command_id == DELETE_ID:
          print('COMMAND: DELETE')
          handle_DELETE(client_socket, file_name)
        
        elif command_id == GETFILE_ID:
          print('COMMAND: GETFILE')
          handle_GETFILE(client_socket, file_name)

      else:
        print('algo deu errado')
        continue
  
      # elif command == "GETFILESLIST":
      #   send_file_list(client_socket)


      # else:
      #   client_socket.send("Invalid command".encode())

    except Exception as e:
      logging.error(f"Error while handling connection: {e}")
      print(f"Error while handling connection: {e}")
      break

  print("Closing connection")
  client_socket.close()

# client_socket = socket used to send the message to the client
# file_name = the file name the client is tryng to add to the server
def handle_ADDFILE(client_socket, file_name):
  response =  f"{RES_TYPE}{ADDFILE_ID}"
  name = file_name.split('/')[-1]
  files_path = './files_server/'
  file_path = os.path.join(files_path, name)
  print('file_path')
  print(file_path)

  if os.path.exists(file_path):
    response += f"{ERROR}"
    client_socket.send(response.encode())
    print(f"File {name} already exists")
    logging.error(f"File {name} already exists")

  else:
    file_size = os.path.getsize(file_name)
    file_data = client_socket.recv(int(file_size))
    with open(file_path, "wb") as file:
      file.write(file_data)

    response += f"{SUCCESS}"
    client_socket.send(response.encode())
    print(f"File '{name}' added by {client_socket.getpeername()}")
    logging.info(f"File '{name}' added by {client_socket.getpeername()}")

# has no validation if file_name receives ../file_name
# client_socket = socket used to send the message to the client
# file_name = the file name the client is tryng to remove from files folder
def handle_DELETE(client_socket, file_name):
  response =  f"{RES_TYPE}{DELETE_ID}"
  file_path = './files_server/' + file_name
  print (file_path)
  if not os.path.exists(file_path):
    response += f"{ERROR}"
    client_socket.send(response.encode())
    print(f"File {file_name} does not exists")
    logging.error(f"File {file_name} does not exists")

  else:
    try:
      os.remove(file_path)
      logging.info(f"File '{file_name}' deleted by {client_socket.getpeername()}")
      print(f"File '{file_name}' deleted by {client_socket.getpeername()}")
      response += f"{SUCCESS}"
      client_socket.send(response.encode())
    except:
      response += f"{ERROR}"
      client_socket.send(response.encode())
      logging.error(f"Error tryng to delete file '{file_name}' by {client_socket.getpeername()}")

def handle_GETFILE(client_socket, file_name):
  response =  f"{RES_TYPE}{GETFILE_ID}"
  file_path = './files_server/' + file_name
  if not os.path.exists(file_path):
    response += f"{ERROR}"
    client_socket.send(response.encode())
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

      file_size_with_zeros = str(file_size).zfill(16)
      response += f"{SUCCESS}"
      response += file_size_with_zeros
      response = response.encode()
      response += data
      client_socket.send(response)
      logging.info(f"File {file_name} sent to client: {client_socket}")

    except:
      response += f"{ERROR}"
      client_socket.send(response.encode())
      logging.error(f"Error tryng to send {file_name}")
      print(f"Error tryng to send {file_name}")


# def send_file_list(self, client_socket):
#   with lock:
#     file_list = "\n".join(files.keys())
#     client_socket.send(file_list.encode())



HOST = "127.0.0.1"
PORT = 4444
# PORT = 7770
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
