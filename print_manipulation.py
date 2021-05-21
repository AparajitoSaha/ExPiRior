import time
import pyautogui
import csv 

def print_label(id):
    fields = []
    rows = []

    data = open("sample_student_data_read.csv", "r")
    csvreader = csv.reader(data)
    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    ind = 0     
    time.sleep(5)

    for row in rows:
        if row[0] != str(id):
            pyautogui.press('down')
            ind = rows.index(row)
            ind += 1
        else:            
            for col in row:
                print(col)
            break

    time.sleep(5)
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(3)
    pyautogui.hotkey('enter')
    time.sleep(3)

    for i in range(ind):
        pyautogui.press('up')