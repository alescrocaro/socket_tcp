###########################################################################
# Description: This code is used to make the connection with the client,  #
#              using UDP sockets, and receive uploaded bin and text files.#
#              First, receives a header, then confirms that the header was#
#              received to the client, so the client send the file data,  #
#              then confirms to the client if all data was received       #
#              informing success or error.                                #
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
server_address = ("127.0.0.1", 57775)

# create UDP socket
# AF_INET = internet address family for ipv4
# SOCK_DGRAM = socket type for UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)
print("Server up and ready to receive files")


# main loop to keep receiving files
while True:
  # Recebe metadados do arquivo (nome, tamanho e checksum)
  header, client_address = server_socket.recvfrom(BUFFER_SIZE)

  filename_size = int.from_bytes(header[0:1], 'big')
  filename = header[1:filename_size + 1].decode('utf-8')
  file_size_firstpos = filename_size + 1
  file_size_lastpos = file_size_firstpos + 4
  file_size = int.from_bytes(header[file_size_firstpos:file_size_lastpos], 'big')
  checksum_firstpos = file_size_lastpos
  checksum = header[checksum_firstpos:].decode('utf-8')
 
  # send ACK to the client to confirm the header was received
  server_socket.sendto(b'ACK', client_address)

  # wait for file from client
  file_data = bytearray()
  while len(file_data) < file_size:
    file_array_buffer, _ = server_socket.recvfrom(BUFFER_SIZE)
    file_data.extend(file_array_buffer)

  # Check file integrity
  received_checksum = hashlib.sha1(file_data).hexdigest()
  if received_checksum == checksum:
    try:
      with open(f"./server_files/{filename}", "wb") as f:
        f.write(file_data)

    except:
      print('Error writing file')
      continue

    server_socket.sendto(b'ACK', client_address)
    print(f"File {filename} received")
  
    continue

  else:
    server_socket.sendto(b'nACK', client_address)
    print("upload not completed (checksum failed).")
  
    continue
