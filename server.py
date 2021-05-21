"""
Sets up a server on the Raspberry Pi for TCP/IP communication via sockets.

Authors: Aparajito Saha and Amulya Khurana
"""

import socket
import threading as Thread
import time
import sys

class SocketServer():
    def __init__(self, conn):
        # conn represents client connection, initializes the TCP/IP connection
        # between server on Pi and client on laptop
        self.conn = conn

    def run(self):
        # Runs the server on the Pi, checking for incoming connections from 
        # client over wireless TCP/IP
        global isConnected
        print("Python server started")
        while True:
            cmd = ""
            try:
                print("Calling blocking conn.recv()")
                msg = recvClientMessage()
            except:
                print("exception in conn.recv()") 
                # happens when connection is reset from the client
                break
                        
        conn.close()
        print("Client disconnected. Waiting for next client...")
        isConnected = False
        print("SocketServer terminated")

    def sendClientMessage(self, msg):
        # Sends a string message over to the client 
        msg = msg + "\0"
        msg = bytes(msg, 'utf-8')
        print("Message sent to client: ", msg)
        self.conn.sendall(msg)

    def recvClientMessage(self):
        # receives message from client and passes it on to 
        # other code modules
        msg = self.conn.recv(4096)
        msg = msg.decode('utf-8')
        print("Message received = ", msg[:-1])
        return msg
