"""
Test a TCP/IP communication based server on the Raspberry Pi

Authors: Aparajito Saha and Amulya Khurana
"""

import socket

HOST = '192.168.0.201'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("binding socket")
    s.bind((HOST, PORT))
    print("socket ready")
    s.listen()
    print("waiting for connection")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
