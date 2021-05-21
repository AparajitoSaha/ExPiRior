from threading import Thread
import socket, time
from print_manipulation import *
import csv

IP_ADDRESS = '192.168.137.216'
IP_PORT = 65432

class Client():
    def run(self):
        print("Client started")
        while True:
            try:
                rcvMsg = self.readServerMsg()
            except:
                print("Exception in Client.run()")
                isClientRunning = False
                closeConnection()
                break
        print("Client thread terminated")

    def readServerMsg(self):
        bufSize = 2048
        data = ""
        while data[-1:] != "\0": # reply with end-of-message indicator
            try:
                blk = sock.recv(bufSize)
            except:
                raise Exception("Exception from blocking sock.recv()")
            data += blk.decode('utf-8')
        print("Data received:", data)
        return data

def sendCommand(data):
    print("sendCommand() with msg = " + data)
    data = data + "\0"
    data = bytes(data, 'utf-8')
    try:
        # append \0 as end-of-message indicator
        sock.sendall(data)
    except:
        print("Exception in sendCommand()")
        closeConnection()

def closeConnection():
    global isConnected
    print("Closing socket")
    sock.close()
    isConnected = False

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting...")
    try:
        sock.connect((IP_ADDRESS, IP_PORT))
    except:
        print("Connection failed.")
        return False
    return True

def read_csv(id):
    rows = []
    data = open("sample_student_data_read.csv", "r")
    csvreader = csv.reader(data)
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
    for row in rows:
        if row[0] == str(id):
            return row[2] + " " + row[3]

    return ""

sock = None
isConnected = False
id = 0

if connect():
    isConnected = True
    client = Client()
    print("Connection established")
    time.sleep(1)
    while isConnected:
        rcvd = client.readServerMsg()
        if (rcvd[:-1] == "yes"):
            print_label(id)
        elif (rcvd[0] == '@'):
            id = rcvd[1:-1]
            print(id, len(id))
            id = int(id)
            print(id, type(id))
            data = read_csv(id)
            if (type(id) == int):
                sendCommand(data)
else:
    print("Connection to %s:%d failed" % (IP_ADDRESS, IP_PORT))
print("done")    