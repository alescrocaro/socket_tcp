# socket_udp - chat p2p

## How to execute
open the first tab in terminal and run
```bash
# Alexandre
$ python3 p2p_chat.py
$ Nick (enter to be anonymous): Alexandre
$ IP address (enter if you want it to be localhost): # here you can just press enter 
$ UDP port: 7777
$ Alexandre: 
```

now open a second tab in terminal and run
```bash
# Pedro
$ python3 p2p_chat.py
$ Nick (enter to be anonymous): Pedro
$ IP address (enter if you want it to be localhost): # here you can just press enter 
$ UDP port: 7777
$ Pedro: 
```

that's it, now those users can send messages to each other, the user can send emojis, URLs and normal messages, like this:
```bash
$ Alexandre: oi
$ Alexandre: https://github.dev/alescrocaro/socket_tcp
$ Alexandre: :D
```

and the messages will be shown to the other user like this:
````bash
$ Pedro: Alexandre: oi
$ Alexandre: https://github.dev/alescrocaro/socket_tcp
$ Alexandre: :D
```


## Libraries
- `socket`: used to manage connections between client and server
- `threading`: used to manage client threads
- `re`: used detect URLs through a regex