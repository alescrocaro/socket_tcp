import socket
import threading
import os
import logging

# config logger
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
  

def handle_connection(client_socket, client_address):
  print(f'client_socket', client_socket)
  print(f'client_address', client_address)
  while True:
    try:
      print('teste')
      data = client_socket.recv(1024)
      print(data)
      req_type = data[0:1]
      command_id = data[1:5]
      filename_size = data[5:6]
      last_pos_of_name = (6 + int(filename_size.decode()))
      filename = data[6:last_pos_of_name]

      if not data:
        logging.error("No data")
        break

      command, *args = data.decode().split()
      if command == "ADDFILE":
        handle_ADDFILE(client_socket, *args)
  
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

def handle_ADDFILE(client_socket, filename, file_size):
  with lock:
    if filename in files:
      client_socket.send("File already exists".encode())
    else:
      file_data = client_socket.recv(int(file_size))
      with open(os.path.join(os.getcwd(), filename), "wb") as f:
        f.write(file_data)
      files[filename] = file_data
      client_socket.send("File added successfully".encode())
      logging.info(f"File '{filename}' added by {client_socket.getpeername()}")

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
# PORT = 7777
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
