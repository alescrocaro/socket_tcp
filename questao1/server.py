import socket
import threading
import json
import os

def service_connection(clientSocket, address):
  currentPath = os.getcwd()

  while True:
    recv_data = clientSocket.recv(1024).decode('utf-8')

    if not recv_data:
      print(f"Closing connection to {address}")
      clientSocket.close()
      break

    command = recv_data.split(" ")

    if command[0] == "CONNECT":
      try:
        (username, password) = command[1].split(",")

        with open('users.json') as file:
          users = json.load(file)['users']

        for user in users:
          if user['username'] == username and user['password'] == password:
            response = "SUCCESS"
            break

        else:  # this else points to 'for' loop
          response = "ERROR"

      except:
        response = "ERROR"

    elif command[0] == "PWD":
      try:
        response = currentPath

      except:
        response = "ERROR"


    elif command[0] == "CHDIR":
      try:
        os.chdir(command[1])
        currentPath = os.path.abspath(os.getcwd())
        response = "SUCCESS"

      except:
        response = "ERROR"

    elif command[0] == "GETFILES":
      try:
        files = os.listdir(currentPath)
        response = (str(len(files)) + '\n')
        for file in files:
          response += (file + "\n")

      except:
        response = "ERROR"

    elif command[0] == "GETDIRS":
      try:
        dirs_only = [file for file in os.listdir() if os.path.isdir(file)]
        response = (str(len(dirs_only)) + '\n')
        for dir in dirs_only:
          response += (dir + "\n")

      except:
        response = "ERROR"

    else:
      response = "ERROR"

    
    response_in_bytes = response.encode()
    clientSocket.sendall(response_in_bytes)


HOST = "127.0.0.1" # localhost
PORT = 4444
# PORT = 7777

# socket.AF_INET = internet address family for ipv4
# socket.SOCK_STREAM = socket type for TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
  try:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Listening on {(HOST, PORT)}")

  except:
    print(f"Failed to listen on {(HOST, PORT)}")

  while True:
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")
    # Create a new thread for each client connection
    client_thread = threading.Thread(target=service_connection, args=(client_socket, address))
    client_thread.start()
