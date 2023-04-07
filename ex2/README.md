# socket_tcp - manage files

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
$ GETILE nums
$ GETILESLIST
$ ADDFILE ../nums2
$ DELETE nums
$ EXIT
```

## Libraries
- `socket`: used to manage connections between client and server
- `os`: used to manage files paths
- `threading`: used to manage client threads
- `logging`: used to create a log system for the server