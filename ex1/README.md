# socket_tcp

## How to execute
run the server in a terminal
```bash
$ python3 server.py
```

run the client in other terminal
```bash
$ python3 client.py
```

in client you can run on terminal
```bash
$ CONNECT admin,admin123
$ PWD
$ CHDIR teste
$ GETFILES
$ GETDIRS
$ EXIT
```

## Libraries
- `socket`: used to manage connections between client and server
- `os`: used to manage files paths
- `json`: used to get the users from a json file
- `threading`: used to manage client threads
- `hashlib`: used to encrypt the password input in client to send to server