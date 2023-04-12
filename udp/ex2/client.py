###########################################################################
# Description: This code is used to make the connection with the server,  #
#              using UDP sockets, and upload bin and text files. First,   #
#              send a header, when the server confirms the header was     #
#              sent, send the file data, then receives a confirmation that#
#              all data was received by the server to inform the user     #
#              success or error. The user must input the command:         #
#              "UPLOAD file_name.extension".                              #
#                                                                         #
# Authors: Alexandre Aparecido Scrocaro Junior, Pedro Klayn               #
#                                                                         #
# Dates: github.com/alescrocaro/socket_tcp/udp                            #
#                                                                         #
###########################################################################

###########################################################################
#                                PROTOCOL                                 #
#                                                                         #
#                                                                         #
#  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  #
#  | File name size |    File name    |  File size  |     Checksum     |  #
#  |     1 byte     |   0-255 bytes   |   4 bytes   |     20 bytes     |  #
#  |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|  #
#  |                                                                   |  #
#  |                            File data                              |  #
#  |                          1 - 2^32 bytes                           |  #
#  |                                                                   |  #
#  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  #
#                                                                         #
# Checksum has 20 bytes because the SHA1 generates 160 bits               #
#                                                                         #
#                                                                         #
###########################################################################


import socket
import hashlib
import os

BUFFER_SIZE = 1024

# this function builds the header to be sent to the server with filename_size,
# filename, file_size and checksum.
# params:
#   filename = name of the file to be uploaded
#   file_data = data contained in file to get the checksum
# return:
#   header = all data contained in header to be sent to server
#   file_size = file size to send the file data in correctly splitted in buffers 
def build_header(filename, file_data):
  header = len(filename).to_bytes(1, "big")
  header += bytes(filename, "utf-8")
  file_size = os.path.getsize(filename)
  header += file_size.to_bytes(4, "big")
  checksum = bytes(hashlib.sha1(file_data).hexdigest(), "utf-8")
  header += checksum

  return header, file_size
  
# main loop to keep receiving user inputs to upload files
if __name__ == "__main__":
  server_address = ("127.0.0.1", 57775)

  # create UDP socket
  # AF_INET = internet address family for ipv4
  # SOCK_DGRAM = socket type for UDP
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  while True:
    message = input("$ ")
    message = message.split()

    if message[0] == "UPLOAD":
      filename = message[1]

      # check if file exists and is not a directory
      if os.path.isfile(filename): 
        try:
          with open(message[1], "rb") as f:
            file_data = f.read()

        except:
          print("Error reading file")
          continue

        # build and send header
        header, file_size = build_header(filename, file_data)
        client_socket.sendto(header, server_address)

        # wait for server confirmation to send file data
        res, _ = client_socket.recvfrom(BUFFER_SIZE)
        if res != b"ACK":
          print("Error sending request header")
          continue

        # send file
        for i in range(0, file_size, BUFFER_SIZE):
          packet = file_data[i:i+BUFFER_SIZE]
          client_socket.sendto(packet, server_address)

        # wait for server to confirm integrity check
        res, _ = client_socket.recvfrom(BUFFER_SIZE)
        if res == b"ACK":
          print(f"File {filename} uploaded to './server_files'.")

        else:
          print(f"Error confirming file integrity.")


      else:
        print("File not found!")
        continue

    else:
      print('Invalid command')