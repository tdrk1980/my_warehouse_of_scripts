# http://ja.pymotw.com/2/subprocess/

import socket
host = "localhost"
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

while True:
    inp=input(">> ")
    client.send(bytearray(inp.encode("CP932")))
    if inp=='quit':
        client.close()
        break


