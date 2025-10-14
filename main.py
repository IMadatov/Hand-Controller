
import cv2
import mediapipe as mp
import tkinter as tk
import pyautogui 
from pygrabber.dshow_graph import FilterGraph 
import os
import numpy as np
import math

def MoveMouseTo(x,y):
    nowPositionMouse=pyautogui.position()
    pyautogui.moveTo(nowPositionMouse.x-x,
                     nowPositionMouse.y-y)
def ClickMouseLeft():
    pyautogui.click()
def DoubleClickMouseLeft():
    pyautogui.click(clicks=2)
    
def ScrollingMouse(x):
    pyautogui.scroll(x)
    
def Press(item):
    pyautogui.press(item)

def GetAvailableCameras():
    

    devices = FilterGraph().get_input_devices()
    cameras = {}

    for index,device in enumerate(devices):
        cameras[index] = device

    return cameras

def DetectHandInfo(hands,frame):
    myHands=[]
    handsType=[]
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(frameRGB)
    if results.multi_hand_landmarks != None:
        
        for hand in results.multi_handedness:
            
            handType=hand.classification[0].label
            handsType.append(handType)
        for handLandMarks in results.multi_hand_landmarks:
            myHand=[]
            for landMark in handLandMarks.landmark:
                myHand.append((int(landMark.x*width),int(landMark.y*height)))
            myHands.append(myHand)
    return myHands,handsType

def CountFingers(hand):
    if len(hand)!=0 :
        
        fingers=[]
        #checking the thumb
        if hand[tipIdsHands[0]][0]>hand[tipIdsHands[0]-1][0]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        for index in range(1,5):
            if hand[tipIdsHands[index]][1]<hand[tipIdsHands[index]-2][1]:
                fingers.append(1)
            else: 
                fingers.append(0)
                ##Selecttion MOde - two fingers are up
            nonTop=[0,3,4]
        
    return fingers
        

cameras = GetAvailableCameras()

selected_Camera = 0
if(len(cameras)!=1 and len(cameras)!=0):
    select_window = tk.Tk()
    select_window.geometry("300x200")
    select_window.title('Select Camera')

    options = tk.StringVar(select_window)
    options.set(cameras[0])

    om1=tk.OptionMenu(select_window, options, *cameras.values())
    om1.grid(row=1,column=1,padx=100,pady=10)

    menu=select_window.nametowidget(om1.menuname)   

    select_window.mainloop()

    for index in cameras:
        if cameras[index]==options.get():
            selected_Camera=index
            break



capture=cv2.VideoCapture(selected_Camera)

drawing = mp.solutions.drawing_utils
mp_hands=mp.solutions.hands


width = 1280
height = 720

capture.set(3, width)
capture.set(4, height)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
capture.set(cv2.CAP_PROP_FPS, 100)

tipIdsHands=[4,8,12,16,20]

xp,yp=[0,0]
xs,ys=[0,0]

lenOfLine=0

leftFingers=[0,0,0,0,0]
rightFingers=[0,0,0,0,0]
positionList=[()]

clicked=False
doubleClicked=False
clickRight=False
clickLeft=False
clickTop=False
clickDown=False
screenshoted=False

mode="default"
folderPath = 'header'
overlayList = []
myList = os.listdir(folderPath)
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
    
header = overlayList[-1]
drawColor = (0, 0, 255)
thickness = 20 # Thickness of the painting
tipIds = [4, 8, 12, 16, 20] # Fingertips indexes
xp, yp = [0, 0] # Coordinates that will keep track of the last position of the index finger
imgCanvas = np.zeros((height, width, 3), np.uint8)

with mp_hands.Hands(min_detection_confidence=0.85, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while capture.isOpened():
        
        _,frame=capture.read()
        if not _:
            break

        frame=cv2.flip(frame,1)
        frame=cv2.resize(frame,(width,height))
        # frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

        frame.flags.writeable = False
        handData,handsType = DetectHandInfo(hands,frame)
        frame.flags.writeable = True
        frame=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # the BGR image to RGB.
        for hand,handType in zip(handData,handsType):
            x1, y1 = hand[8]  # Index finger
            x2, y2 = hand[12] # Middle finger
            x3, y3 = hand[4]  # Thumb
            x4, y4 = hand[20] # Pinky
            x5, y5 = hand[9] #To scroll
            if mode=="default":
                if handType=='Right':
                    rightFingers=CountFingers(hand=hand)
                    if rightFingers!=[] : 
                        if rightFingers[0]==0:
                            rightFingers[0]=1
                        else :
                            rightFingers[0]=0

                    handColor=(255,0,0)
                if handType=='Left':
                    leftFingers=CountFingers(hand=hand)
                    handColor=(0,0,255)
                for ind in range(20):
                    cv2.circle(frame,hand[ind],5,handColor,5)

                #######################################################################
                #Right hand
                #######################################################################
                #Mouse move - One finger is up
                nonMove=[0,2,3,4]
                if rightFingers[1] and all(rightFingers[i]==0 for i in nonMove):
                    #logic for mouse
                    if xp==0 and yp==0:
                        xp,yp=[x1,y1]
                    MoveMouseTo(xp-x1,yp-y1)
                    xp,yp=[x1,y1]
                if any(rightFingers[i]==1 for i in nonMove) or all(rightFingers[i]==0 for i in range(0,5)):
                    xp,yp=0,0
                #Scrolling
                if all(rightFingers[i]==1 for i in range(0,5)):
                    if xs==0 and ys==0:
                        xs,ys=[0,y5]
                    ScrollingMouse(y5-ys)
                    xs,ys=[0,y5]
                else:
                    xs,ys=0,0
                #Mouse click-two fingers are up
                nonDoubleClick=[0,3,4]
                if rightFingers[1] and rightFingers[2] and all(rightFingers[i]==0 for i in nonDoubleClick) and not doubleClicked:
                    ClickMouseLeft()
                    doubleClicked=True


                if any(rightFingers[i]==1 for i in nonDoubleClick) or (rightFingers[2]==0 or rightFingers[1]==0):
                    doubleClicked=False
                #double click
                nonClick=[2,3,4]
                if rightFingers[0] and rightFingers[1] and all(rightFingers[i]==0 for i in nonClick) and not clicked:
                    DoubleClickMouseLeft()
                    clicked=True
                if any(rightFingers[i]==1 for i in nonClick) or (rightFingers[0]==0 or rightFingers[1]==0):
                    clicked=False
                nonSel = [0, 3, 4] # indexes of the fingers that need to be down in the Selection Mode
                if (rightFingers[1] and rightFingers[2]) and all(rightFingers[i] == 0 for i in nonSel):
                        xp, yp = [x1, y1]
                        # Selecting the colors and the eraser on the screen
                        if(y1 < 125):
                            if(170 < x1 < 295):
                                header = overlayList[0]
                                mode="draw"
                #######################################################################
                #Left hand
                #######################################################################
                #ToRight
                nonToRight=[1,2,3,4]
                if leftFingers[0]==1 and all(leftFingers[i]==0 for i in nonToRight) and not clickRight:
                    Press('right')
                    clickRight=True
                if leftFingers[0]==0 or any (leftFingers[i]==1 for i in nonToRight):
                    clickRight=False
                #ToUp
                nonToUp=[0,2,3,4]
                if leftFingers[1]==1 and all(leftFingers[i]==0 for i in nonToUp) and not clickTop:
                    Press('up')
                    clickTop=True
                if (leftFingers[1]==0 and leftFingers[0]==0) or  any (leftFingers[i]==1 for i in nonToUp):
                    clickTop=False

                #ToLeft
                nonToLeft=[0,1,2,3]
                if leftFingers[4]==1 and all(leftFingers[i]==0 for i in nonToLeft) and not clickLeft:
                    Press('left')
                    clickLeft=True
                if leftFingers[4]==0 or any (leftFingers[i]==1 for i in nonToLeft):
                    clickLeft=False
                #ToDown
                nonToDown=[1,2,3,4]
                if leftFingers[0]==0 and all(leftFingers[i]==1 for i in nonToDown) and not clickDown:
                    Press('down')
                    clickDown=True
                if leftFingers[0]==1  or any (leftFingers[i]==0 for i in nonToDown):
                    clickDown=False

                #screenshot
                if all(leftFingers[i] for i in range(0,5)) and not screenshoted:
                    Press('prtscr')
                    screenshoted=True
                else :
                    screenshoted=False
                
            # title = ':'.join(str(e) for e in rightFingers)
            # cv2.putText(frame,'Right {'+title+'}', (25, 60), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0,0,0), 1)
            # title = ':'.join(str(e) for e in leftFingers)
            # cv2.putText(frame,'Left {'+title+'}', (25, 90), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0,0,0), 1)      
            # cv2.putText(frame,'Author: islam_madatov.t.me',(800,30),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,0,0),1)         
                
            if mode=="draw":
                ## Checking which fingers are up
                fingers = []
                # Checking the thumb
                if hand[tipIds[0]][0] < hand[tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # The rest of the fingers
                for id in range(1, 5):
                    if hand[tipIds[id]][1] < hand[tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                ## Selection Mode - Two fingers are up
                nonSel = [0, 3, 4] # indexes of the fingers that need to be down in the Selection Mode
                if (fingers[1] and fingers[2]) and all(fingers[i] == 0 for i in nonSel):
                    xp, yp = [x1, y1]
                    # Selecting the colors and the eraser on the screen
                    if(y1 < 125):
                        if(170 < x1 < 295):
                            header = overlayList[0]
                            drawColor = (0, 0, 255)
                        elif(436 < x1 < 561):
                            header = overlayList[1]
                            drawColor = (255, 0, 0)
                        elif(700 < x1 < 825):
                            header = overlayList[2]
                            drawColor = (0, 255, 0)
                        elif(980 < x1 < 1105):
                            header = overlayList[3]
                            drawColor = (0, 0, 0)
                        elif(30<x1<100):
                            header = overlayList[-1]
                            drawColor = (0, 0, 255)
                            thickness = 20 
                            mode="default"
                            xp, yp = [0, 0]
                            imgCanvas = np.zeros((height, width, 3), np.uint8)

                    cv2.rectangle(frame, (x1-10, y1-15), (x2+10, y2+23), drawColor, cv2.FILLED)
                ## Stand by Mode - Checking when the index and the pinky fingers are open and dont draw
                nonStand = [0, 2, 3] # indexes of the fingers that need to be down in the Stand Mode
                if (fingers[1] and fingers[4]) and all(fingers[i] == 0 for i in nonStand):
                    # The line between the index and the pinky indicates the Stand by Mode
                    cv2.line(frame, (xp, yp), (x4, y4), drawColor, 5) 
                    xp, yp = [x1, y1]
                ## Draw Mode - One finger is up
                nonDraw = [0, 2, 3, 4]
                if fingers[1] and all(fingers[i] == 0 for i in nonDraw):
                    # The circle in the index finger indicates the Draw Mode
                    cv2.circle(frame, (x1, y1), int(thickness/2), drawColor, cv2.FILLED) 
                    if xp==0 and yp==0:
                        xp, yp = [x1, y1]
                    # Draw a line between the current position and the last position of the index finger
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, thickness)
                    # Update the last position
                    xp, yp = [x1, y1]
                ## Clear the canvas when the hand is closed
                if all(fingers[i] == 0 for i in range(0, 5)):
                    imgCanvas = np.zeros((height, width, 3), np.uint8)
                    xp, yp = [x1, y1]
                ## Adjust the thickness of the line using the index finger and thumb
                selecting = [1, 1, 0, 0, 0] # Selecting the thickness of the line
                setting = [1, 1, 0, 0, 1]   # Setting the thickness chosen
                if all(fingers[i] == j for i, j in zip(range(0, 5), selecting)) or all(fingers[i] == j for i, j in zip(range(0, 5), setting)):
                    # Getting the radius of the circle that will represent the thickness of the draw
                    # using the distance between the index finger and the thumb.
                    r = int(math.sqrt((x1-x3)**2 + (y1-y3)**2)/3)
                    
                    # Getting the middle point between these two fingers
                    x0, y0 = [(x1+x3)/2, (y1+y3)/2]
                    
                    # Getting the vector that is orthogonal to the line formed between
                     # these two fingers
                    v1, v2 = [x1 - x3, y1 - y3]
                    v1, v2 = [-v2, v1]
                    # Normalizing it 
                    mod_v = math.sqrt(v1**2 + v2**2)
                    v1, v2 = [v1/mod_v, v2/mod_v]
                    
                    # Draw the circle that represents the draw thickness in (x0, y0) and orthogonaly 
                    # translated c units
                    c = 3 + r
                    x0, y0 = [int(x0 - v1*c), int(y0 - v2*c)]
                    cv2.circle(frame, (x0, y0), int(r/2), drawColor, -1)
                    # Setting the thickness chosen when the pinky finger is up
                    if fingers[4]:                        
                        thickness = r
                        cv2.putText(frame, 'Check', (x4-25, y4-8), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0,0,0), 1)
                    xp, yp = [x1, y1]
        
        frame[0:125,0:width]=header

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 5, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(frame, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        cv2.imshow("Hand Controller",img)
        

        if cv2.waitKey(1)==27 or cv2.getWindowProperty('Hand Controller',cv2.WND_PROP_VISIBLE)<1:
            cv2.destroyAllWindows()
            capture.release()
            break
        
    



    

