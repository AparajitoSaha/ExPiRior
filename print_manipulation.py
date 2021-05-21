""""
Code for keyboard manipulation to read user data and interact with the Brother 
editor to print a label.

Authors: Aparajito Saha and Amulya Khurana
"""

import time
import pyautogui
import csv 

def print_label(id):
    fields = []
    rows = []
       
    #read student data from a CSV
    data = open("sample_student_data_read.csv", "r")
    csvreader = csv.reader(data)
    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    ind = 0     
    time.sleep(5)
    
    #go through each row and compare the student ID
    for row in rows:
        if row[0] != str(id):
            #move down to required row
            pyautogui.press('down')
            ind = rows.index(row)
            ind += 1
        else:            
            for col in row:
                print(col)
            break

    #CTRL-P to print the label and confirm
    time.sleep(5)
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(3)
    pyautogui.hotkey('enter')
    time.sleep(3)
    
    #go back to the top of the CSV
    for i in range(ind):
        pyautogui.press('up')
