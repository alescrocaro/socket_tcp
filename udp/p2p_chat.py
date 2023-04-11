import socket
import threading
import re

NORMAL_MESSAGE = 1
EMOJI_MESSAGE = 2
URL_MESSAGE = 3
ECHO_MESSAGE = 4


def receive_message(sock):
  while True:
    (message, address) = sock.recvfrom(1024)

    message_type = int.from_bytes(message[0:1], 'big')

    len_nick = int.from_bytes(message[1:2], 'big')
    last_pos_nick = len_nick + 2
    nick = message[2:last_pos_nick].decode('utf-8')

    last_pos_len_message = last_pos_nick + 1
    len_message = int.from_bytes(message[last_pos_nick:last_pos_len_message], 'big')

    last_pos_message = last_pos_len_message + len_message
    message = message[last_pos_len_message:last_pos_message].decode('utf-8')

    if message_type == ECHO_MESSAGE:
      echo_message = message[5:]
      header = build_header(echo_message, nick)
      sock.sendto(header, address)
    
    else:
      print('{}: {}'.format(nick, message))

def user_inputs():
  nick = input('Nick: ')
  if nick == '' or nick.isspace():
    nick = 'Anonymous'

  address = input('IP address (input nothing if you want to be localhost): ')
  if address == '' or address.isspace():
    address = '127.0.0.1'
  
  port = int(input('UDP port: '))

  return nick, address, port

def is_url(text):
  url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

  return bool(url_pattern.match(text))

def is_emoji(text):
  if text == ':)' or text == ':(' or text == '8)' or text == ':D' or text == ':O' or text == ':P': 
    return True

  return False

def build_header(message, nick):
  len_nick = len(nick)

  echo_message = message.split()

  message_type = NORMAL_MESSAGE

  if is_emoji(message): 
    message_type = EMOJI_MESSAGE
  
  elif is_url(message):
    message_type = URL_MESSAGE

  elif echo_message[0] == 'ECHO':
    message_type = ECHO_MESSAGE
  
  header = message_type.to_bytes(1, 'big')
  header += len_nick.to_bytes(1, 'big')
  header += bytes(nick, 'utf-8')
  header += len(message).to_bytes(1, 'big')
  header += bytes(message, 'utf-8')

  return header
  
if __name__ == '__main__':
  nick, address, port = user_inputs()

  # AF_INET = internet address family for ipv4
  # SOCK_STREAM = socket type for UDP
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  # connect the socket to the UDP port
  server_address = (address, port)
  listen_address = (address, (port + 1))
  try:
    sock.bind(listen_address)
    print('server up')

  # when the port is being used, it means there is already a server running in
  # it, so we need to invert the ports to connect the two clients with each other
  except OSError:
    listen_address = server_address
    server_address = (address, (port + 1))
    sock.bind(listen_address)

  # create a thread to receive messages
  client_socket = threading.Thread(target=receive_message, args=(sock,))
  client_socket.start()

  # main thread to send messages 
  while True:
    message = input(f'{nick}: ')

    if (message == '' or message.isspace()):
      continue

    header = build_header(message, nick)

    sock.sendto(header, server_address)