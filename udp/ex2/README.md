# socket udp

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
$ UPLOAD nums2
$ UPLOAD emoji
```

now you can open the server_files folder and see the files uploaded

## Libraries
- `socket`: used to manage connections between client and server
- `os`: used to manage files paths
- `hashlib`: used to make a checksum, first encrypt the file (using SHA1) in client and send the encrypted string in header, in the server, the received file also is encrypted, then compares the checksum generated by server to the on received in header
