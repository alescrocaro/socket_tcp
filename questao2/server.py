import socket
import threading
import os
import logging

# config logger
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
  
REQ_TYPE = "0x01"
ADDFILE_ID = "0x01"
DELETE_ID = "0x02"
GETFILESLIST_ID = "0x03"
GETFILE_ID = "0x04"

def handle_connection(client_socket, client_address):
  print(f'client_socket', client_socket)
  print(f'client_address', client_address)
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
          handle_ADDFILE(client_socket, file_name)

      else:
        print('algo deu errado')
        continue
  
      # elif command == "DELETE":
      #   delete_file(client_socket, *args)

      # elif command == "GETFILESLIST":
      #   send_file_list(client_socket)

      # elif command == "GETFILE":
      #   send_file(client_socket, *args)

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
  print('HANDLE ADD FILE')
  files_path = './files/'
  file_path = os.path.join(files_path, file_name)
  print('file_path')
  print(file_path)

  if os.path.exists(file_path):
    client_socket.send("File already exists".encode())
    logging.error(f"File {file_name} already exists")

  else:
    file_size = os.path.getsize(file_name)
    file_data = client_socket.recv(int(file_size))
    with open(file_path, "wb") as file:
      file.write(file_data)

    # files[file_name] = file_data
    client_socket.send("File added successfully".encode())
    logging.info(f"File '{file_name}' added by {client_socket.getpeername()}")

# def delete_file(client_socket, filename):
#   with lock:
#     if filename in files:
#       os.remove(os.path.join(os.getcwd(), filename))
#       del files[filename]
#       client_socket.send("File deleted successfully".encode())
#       logging.info(f"File '{filename}' deleted by {client_socket.getpeername()}")
#     else:
#       client_socket.send("File not found".encode())

# def send_file_list(self, client_socket):
#   with lock:
#     file_list = "\n".join(files.keys())
#     client_socket.send(file_list.encode())

# def send_file(self, client_socket, filename):
#   with lock:
#     if filename in files:
#       client_socket.send(files[filename])
#     else:
#       client_socket.send("File not found".encode())


HOST = "127.0.0.1"
PORT = 4444
PORT = 7777
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
