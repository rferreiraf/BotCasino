import pyautogui
import cv2
import json
import pytesseract
import time
import random

#POSITIONS
red = [1230,800]
black = [1330,800]
spin = [1476, 901]
double =[1323, 919]
clear = [1188, 914]

#VARIABLES
bet_color = None
num_lost =0;
times_bet =2;
win_times =0;


#CONFIG TESSERACT
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#READ JSON FILE ND CONVERT DATA
data_file = open('data.json', 'r')
json_data = data_file.read()
list_digit = json.loads(json_data)
data_file.close()

def takeScreenShoot_FindNumber():
    #SCREENSHOT
    screen_shot = pyautogui.screenshot(region=(520, 138, 30, 30))
    screen_shot.save(r"C:\PROJECTS\Python\Casino_Bot\screenshot.png")

    #MANIPULATE IMAGE
    img = cv2.imread('screenshot.png')
    img_resize = cv2.resize(img, None, fx=5, fy=5)
    img_grey = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    img_noise = cv2.medianBlur(img_grey, 5)
    img_threshold = cv2.threshold(img_noise, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img_invert = cv2.bitwise_not(img_threshold)




    #TEXT RECOGNICION
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    digit_find = int(pytesseract.image_to_string(img_invert, config=custom_config))

    #FIND NUMBER
    for i in range(len(list_digit)):
        if list_digit[i].get("digit") == digit_find:
            print("NUMERO::::", i)
            return list_digit[i]


def firstBet_ReturnBetColor(betColor):
    if betColor== "red":
        pyautogui.click(black[0], black[1])
        print("bet black")
        return "black"
    elif betColor== "black":
        pyautogui.click(red[0], red[1])
        print("bet red ")
        return "red"
    else:
        pyautogui.click(red[0], red[1])
        print("bet red ")
        return  "red"

def randomBetColor():
    random_int = random.randint(1, 2)
    if random_int ==1:
        return "red"
    else:
        return "black"

def betSystem(betColor, numLost, timesBet):
    if numLost ==0:
        if betColor == "red":
            pyautogui.click(red[0], red[1])
        else:
            pyautogui.click(black[0], black[1])
        return timesBet
    else:
        if betColor == "red":
            for x in range(timesBet):
                pyautogui.click(red[0], red[1])
                time.sleep(0.5)
        else:
            for x in range(timesBet):
                pyautogui.click(black[0], black[1])
                time.sleep(0.5)
        return timesBet * 2

def spinHandle():
    time.sleep(1)
    pyautogui.click(spin[0], spin[1])
    time.sleep(2)
    pyautogui.click(spin[0], spin[1])

def clearBetHandle():
    time.sleep(0.5)
    pyautogui.click(clear[0], clear[1])
    time.sleep(0.5)

##################################PROGRAM######################################


clearBetHandle()

digit = takeScreenShoot_FindNumber()
bet_color = firstBet_ReturnBetColor(digit.get("color"))
#FIRST SPIN
spinHandle()

while True:
    time.sleep(8)
    digit = takeScreenShoot_FindNumber()
    time.sleep(2)
    if digit.get("color") == bet_color:
        win_times = win_times+1
        print("win ---> ", win_times, " times")
        num_lost =0
        times_bet = 2;
        clearBetHandle()
    else:
        print("lost, double bet")
        num_lost = num_lost +1
    bet_color = randomBetColor()
    times_bet = betSystem(bet_color, num_lost, times_bet)
    spinHandle()

