###########################################################################
# Description: This code is used to manage a connection with the client   #
#              using tcp sockets and threads. It process the commands     #
#              CONNECT, PWD, CHDIR GETFILES, GETDIRS and EXIT, make the   # 
#              needed processes send a response to the client             #
#                                                                         #
# Authors: Alexandre Aparecido Scrocaro Junior, Pedro Klayn               #
#                                                                         #
# Dates: github.com/alescrocaro/socket_tcp                                #
#                                                                         #
###########################################################################

import socket
import threading
import json
import os

# receives the command by the client and manage it (comments in each funcionality)
# client_socket = socket connection with client
# address = client address (Host and port)
# return the response to the client
def service_connection(client_socket, address):
  currentPath = os.getcwd()

  # loop to keep receiving client requests
  while True:
    recv_data = client_socket.recv(1024).decode('utf-8')

    if not recv_data:
      print(f"Closing connection to {address}")
      client_socket.close()
      break

    command = recv_data.split(" ")

    # authenticate the client using the 'users.json' file
    # username = user name input in the command sent by the client
    # password = password input in the command sent by the client
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

    # command = command sent by client
    # returns the current path of client
    elif command[0] == "PWD":
      try:
        response = currentPath

      except:
        response = "ERROR"

    # command = command sent by client
    # change the current path to the one the client is asking for
    elif command[0] == "CHDIR":
      try:
        os.chdir(command[1])
        currentPath = os.path.abspath(os.getcwd())
        response = "SUCCESS"

      except:
        response = "ERROR"

    # command = command sent by client
    # returns all files in current path (like 'ls' in linux)
    elif command[0] == "GETFILES":
      try:
        files = os.listdir(currentPath)
        response = (str(len(files)) + '\n')
        for file in files:
          response += (file + "\n")

      except:
        response = "ERROR"

    # command = command sent by client
    # returns only the directories in current path
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

    # send response builded above to the client in bytes
    response_in_bytes = response.encode()
    client_socket.sendall(response_in_bytes)


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

  # server loop to listen for client connections
  while True:
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")
    # Create a new thread for each client connection
    client_thread = threading.Thread(target=service_connection, args=(client_socket, address))
    client_thread.start()
