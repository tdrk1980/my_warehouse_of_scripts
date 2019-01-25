import serial
import time

# pySerial API
# http://pythonhosted.org/pyserial/pyserial_api.html

# http://ja.pymotw.com/2/subprocess/
# https://blog.amedama.jp/entry/2017/03/29/080000

def cmd(cmd):
    cmd=cmd+'\n'
    return bytes(cmd.encode('cp932'))


import socket
host = "localhost" #お使いのサーバーのホスト名を入れます
port = 12345 #クライアントと同じPORTをしてあげます

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port)) #IPとPORTを指定してバインドします
serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）

import subprocess
print("launch subprcess")
proc = subprocess.Popen(["start", "cmd", "/K", r"D:\Anaconda3\python", "sender.py"], stdout=subprocess.PIPE, shell=True)

print('Waiting for connections...')
clientsocket, client_address = serversock.accept() #接続されればデータを格納

while True:
    # クライアントソケットから指定したバッファバイト数だけデータを受け取る
    try:
        message = clientsocket.recv(1024)
        message = message.decode("CP932")
        print(f"Recv: {message}")
        if message == "quit":
            break
    except OSError:
        break

    # 受信したデータの長さが 0 ならクライアントからの切断を表す
    if len(message) == 0:
        break

clientsocket.close()
serversock.close()

if False:
    ser = serial.Serial(port='COM6', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN)
    while True:
        print(ser.readline().decode('cp932').strip())
