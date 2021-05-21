""""

Overarching finite state machine for the system. Sets up the server connection, creates PyGame text surfaces, and FSM transitions.  

Authors: Aparajito Saha and Amulya Khurana

""""

import pyaudio
import pygame
import signal
import os
import time
import subprocess
from speech_recog_test import * 
from test import *
from sensor_test import *
import arm
from server import SocketServer
import socket
import sys
import RPi.GPIO as GPIO

# Initialize server and carry out starting handshake
server_start_time = time.time()
HOSTNAME = "192.168.137.216"
IP_PORT = 65432
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
print("Socket created")
try:
    serverSocket.bind((HOSTNAME, IP_PORT))
except socket.error as msg:
    print("Bind failed", msg[0], msg[1])
    sys.exit()
serverSocket.listen(10)

print("Waiting for a connecting client...")
isConnected = False
while (time.time() - server_start_time <= 30 and not(isConnected)):
    print("Calling blocking accept()...")
    conn, addr = serverSocket.accept()
    print("Connected with client at " + addr[0])
    isConnected = True
    SocketServer = SocketServer(conn)

#set environment variables
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')

pygame.init()

size = width, height = 320, 240
speed = [2, 2]
BLACK = 0, 0, 0
WHITE = 255, 255, 255
screen = pygame.display.set_mode(size)

my_font=pygame.font.Font(None,30)
screen.fill(BLACK)
pygame.mouse.set_visible(False)

#Text Displays

text_surface_init=my_font.render('Wave and then say HI to begin',True,WHITE)
rect_init=text_surface_init.get_rect(center=(160,120))

text_surface_id1=my_font.render('Please say your Student ID',True,WHITE)
rect_id1=text_surface_id1.get_rect(center=(160,120))
text_surface_id2=my_font.render('number into the microphone',True,WHITE)
rect_id2=text_surface_id2.get_rect(center=(160,140))

text_surface_confirm1=my_font.render('Is this information correct?',True,WHITE)
rect_confirm1=text_surface_confirm1.get_rect(center=(160,120))
text_surface_confirm2=my_font.render('Please say Yes or No',True,WHITE)
rect_confirm2=text_surface_confirm2.get_rect(center=(160,140))

text_surface_swab1=my_font.render('Please collect the swab',True,WHITE)
rect_swab1=text_surface_swab1.get_rect(center=(160,60))
text_surface_swab2=my_font.render('and tear the package.',True,WHITE)
rect_swab2=text_surface_swab2.get_rect(center=(160,80))
text_surface_swab3=my_font.render('Insert the swab into your nostril',True,WHITE)
rect_swab3=text_surface_swab3.get_rect(center=(160,100))
text_surface_swab4=my_font.render('until you feel resistance.',True,WHITE)
rect_swab4=text_surface_swab4.get_rect(center=(160,120))
text_surface_swab5=my_font.render('Rotate it there for 10 seconds.',True,WHITE)
rect_swab5=text_surface_swab5.get_rect(center=(160,140))
text_surface_swab6=my_font.render('Then switch to the other nostril.',True,WHITE)
rect_swab6=text_surface_swab6.get_rect(center=(160,160))

text_surface_swab7=my_font.render('Say redo to try again',True,WHITE)
rect_swab7=text_surface_swab7.get_rect(center=(160,180))


text_surface_switch=my_font.render('Please switch to the other nostril.',True,WHITE)
rect_switch=text_surface_switch.get_rect(center=(160,120))

text_surface_tube1=my_font.render('Place the swab',True,WHITE)
rect_tube1=text_surface_tube1.get_rect(center=(160,70))
text_surface_tube2=my_font.render('in the test tube.',True,WHITE)
rect_tube2=text_surface_tube2.get_rect(center=(160,90))
text_surface_tube3=my_font.render('Collect the label and',True,WHITE)
rect_tube3=text_surface_tube3.get_rect(center=(160,110))
text_surface_tube4=my_font.render('paste it on the test tube.',True,WHITE)
rect_tube4=text_surface_tube4.get_rect(center=(160,130))
text_surface_tube5=my_font.render('Then place the test tube',True,WHITE)
rect_tube5=text_surface_tube5.get_rect(center=(160,150))
text_surface_tube6=my_font.render('in the tray to the left.',True,WHITE)
rect_tube6=text_surface_tube6.get_rect(center=(160,170))

text_surface_done=my_font.render('Thank You!',True,WHITE)
rect_done=text_surface_done.get_rect(center=(160,120))

#STATES
INIT = 0
NEW_USER = 1 #ask for student id
GET_DATA = 2 #display info and confirm
SWAB = 3 #pick up and present swab, display instructions
LABEL = 4 #ask to switch nostrils and print label
TUBE = 5 #pick up and present test tube and display instructions
DONE = 6 #display thank you message

current_state = INIT

while(1):
    screen.fill(BLACK)
    if(current_state == INIT):
	#current_state = NEW_USER if speech_recog_test.get_audio_hi() == 'hi'
    	screen.blit(text_surface_init,rect_init)
    	pygame.display.flip()
    	dist = sensor()
    	p=subprocess.Popen('./record.sh',shell=True)
    	time.sleep(3)
    	subprocess.Popen('sudo killall arecord',shell=True)
    	print("Detected Distance = " + str(dist))
    	try:
    	    if get_audio_hi() == 'hi' and dist<15 and dist>2:
    	        current_state = NEW_USER
    	except:
    	    pass
    elif(current_state == NEW_USER):
    	#get microphone input
    	screen.blit(text_surface_id1,rect_id1)
    	screen.blit(text_surface_id2,rect_id2)
    	pygame.display.flip()
    	p=subprocess.Popen('./studentID.sh',shell=True)
    	time.sleep(9)
    	subprocess.Popen('sudo killall arecord',shell=True)
    	id = get_audio_test().replace(" ","")
	#communicate student id to the client
    	SocketServer.sendClientMessage('@'+id)
    	current_state = GET_DATA
    elif(current_state == GET_DATA):
    	info = SocketServer.recvClientMessage()
    	while(info == ""):
    	    info = SocketServer.recvClientMessage()
    	print(info, len(info), type(info))
    	#get corresponding data and display it
    	#print 'Is this correct?'
    	#if microphone  input == 'Yes': current_state = SWAB
    	#else:
    	#print 'Please say your student id again'
    	text_surface_data=my_font.render(str(info[:-1]),True,WHITE)
    	rect_data=text_surface_data.get_rect(center=(160,100))
    	screen.blit(text_surface_confirm1,rect_confirm1)
    	screen.blit(text_surface_confirm2,rect_confirm2)
    	screen.blit(text_surface_data,rect_data)
    	pygame.display.flip()
    	p=subprocess.Popen('./yes.sh',shell=True)
    	time.sleep(3)
    	subprocess.Popen('sudo killall arecord',shell=True)
    	response = get_audio_yes()
    	if response == '': 
    	    response = 'no'
    	if response == 'yes':
    	    SocketServer.sendClientMessage(response)
    	    current_state=SWAB
    	else:
    	    current_state=NEW_USER
    elif(current_state == SWAB):
    	#pick up swab and present to user
    	#display instructions
    	arm.move_arm()
    	GPIO.cleanup()
    	screen.blit(text_surface_swab1,rect_swab1)
    	screen.blit(text_surface_swab2,rect_swab2)
    	screen.blit(text_surface_swab3,rect_swab3)
    	screen.blit(text_surface_swab4,rect_swab4)
    	screen.blit(text_surface_swab5,rect_swab5)
    	screen.blit(text_surface_swab6,rect_swab6)
    	screen.blit(text_surface_swab7,rect_swab7)
    	p = subprocess.Popen('./redo.sh',shell=True)
    	time.sleep(3)
    	subprocess.Popen('sudo killall arecord',shell=True)
	#retry robot arm movement if user says 'Redo'
    	response = get_audio_redo()
    	if response == 'redo':
    	    current_state = SWAB
    	else:
    	    current_state = LABEL

    elif(current_state == LABEL):
    	#send print command to label maker
    	#ask user to switch to other nostril
    	screen.blit(text_surface_switch,rect_switch)
    	time.sleep(5)
    	current_state = TUBE
    elif(current_state == TUBE):
    	#display instructions
    	screen.blit(text_surface_tube1,rect_tube1)
    	screen.blit(text_surface_tube2,rect_tube2)
    	screen.blit(text_surface_tube3,rect_tube3)
    	screen.blit(text_surface_tube4,rect_tube4)
    	screen.blit(text_surface_tube5,rect_tube5)
    	screen.blit(text_surface_tube6,rect_tube6)
    	time.sleep(10)
    	current_state = DONE
    elif(current_state == DONE):
    	#display 'Thank You'
    	screen.blit(text_surface_done,rect_done)
    	time.sleep(8)
    	current_state = INIT
    pygame.display.flip()

