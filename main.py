
import cv2
import mediapipe as mp
import tkinter as tk
import pyautogui 
from pygrabber.dshow_graph import FilterGraph 
import os
import numpy as np
import math
from utils import resource_path

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
      
  
def main():
    # make module-level constants visible to functions like DetectHandInfo / CountFingers
    global width, height, tipIdsHands

    # ---- camera selection (same as your code, wrapped) ----
    cameras = GetAvailableCameras()
    selected_Camera = 0
    if len(cameras) > 1:
        try:
            select_window = tk.Tk()
            select_window.geometry("300x200")
            select_window.title('Select Camera')

            options = tk.StringVar(select_window)
            # default to first device name
            options.set(next(iter(cameras.values())))

            om1 = tk.OptionMenu(select_window, options, *cameras.values())
            om1.grid(row=1, column=1, padx=100, pady=10)

            select_window.mainloop()

            for index in cameras:
                if cameras[index] == options.get():
                    selected_Camera = index
                    break
        except Exception:
            # if Tk fails in frozen/NoGUI contexts, just fall back to camera 0
            selected_Camera = 0

    # ---- capture / mediapipe init ----
    # CAP_DSHOW helps on Windows to open cameras reliably
    capture = cv2.VideoCapture(selected_Camera, cv2.CAP_DSHOW)

    width, height = 1280, 720
    capture.set(3, width)
    capture.set(4, height)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_FPS, 100)

    drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    tipIdsHands = [4, 8, 12, 16, 20]

    # state
    xp, yp = [0, 0]
    xs, ys = [0, 0]
    leftFingers = [0, 0, 0, 0, 0]
    rightFingers = [0, 0, 0, 0, 0]

    clicked = False
    doubleClicked = False
    clickRight = False
    clickLeft = False
    clickTop = False
    clickDown = False
    screenshoted = False

    mode = "default"

    # ---- load header assets (robust path for EXE) ----
    # your folder was 'header' in code; make sure the real folder is 'Header' or adjust here
    folderPath = resource_path('Header')
    overlayList = []
    if os.path.isdir(folderPath):
        for imName in os.listdir(folderPath):
            imgPath = os.path.join(folderPath, imName)
            image = cv2.imread(imgPath)
            if image is not None:
                overlayList.append(image)
    # fallback: solid bar if assets missing
    header = overlayList[-1] if overlayList else np.zeros((125, width, 3), dtype=np.uint8)

    drawColor = (0, 0, 255)
    thickness = 20
    tipIds = [4, 8, 12, 16, 20]
    xp, yp = [0, 0]
    imgCanvas = np.zeros((height, width, 3), np.uint8)

    try:
        with mp_hands.Hands(min_detection_confidence=0.85,
                            min_tracking_confidence=0.5,
                            max_num_hands=1) as hands:

            while capture.isOpened():
                ok, frame = capture.read()
                if not ok:
                    break

                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (width, height))

                frame.flags.writeable = False
                handData, handsType = DetectHandInfo(hands, frame)
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                for hand, handType in zip(handData, handsType):
                    x1, y1 = hand[8]   # index
                    x2, y2 = hand[12]  # middle
                    x3, y3 = hand[4]   # thumb
                    x4, y4 = hand[20]  # pinky
                    x5, y5 = hand[9]   # scroll anchor

                    if mode == "default":
                        if handType == 'Right':
                            rightFingers = CountFingers(hand=hand) or []
                            if rightFingers != []:
                                # invert thumb logic per your original code
                                rightFingers[0] = 1 if rightFingers[0] == 0 else 0
                            handColor = (255, 0, 0)

                        if handType == 'Left':
                            leftFingers = CountFingers(hand=hand) or []
                            handColor = (0, 0, 255)

                        for ind in range(20):
                            cv2.circle(frame, hand[ind], 5, handColor, 5)

                        # ---- Right-hand actions ----
                        # Move: only index up
                        nonMove = [0, 2, 3, 4]
                        if len(rightFingers) == 5 and rightFingers[1] and all(rightFingers[i] == 0 for i in nonMove):
                            if xp == 0 and yp == 0:
                                xp, yp = [x1, y1]
                            MoveMouseTo(xp - x1, yp - y1)
                            xp, yp = [x1, y1]
                        if len(rightFingers) != 5 or any(rightFingers[i] == 1 for i in nonMove) or all(r == 0 for r in rightFingers):
                            xp, yp = 0, 0

                        # Scroll: all fingers up
                        if len(rightFingers) == 5 and all(r == 1 for r in rightFingers):
                            if xs == 0 and ys == 0:
                                xs, ys = [0, y5]
                            ScrollingMouse(y5 - ys)
                            xs, ys = [0, y5]
                        else:
                            xs, ys = 0, 0

                        # Single left click: index+middle up
                        nonDoubleClick = [0, 3, 4]
                        if (len(rightFingers) == 5 and rightFingers[1] and rightFingers[2]
                                and all(rightFingers[i] == 0 for i in nonDoubleClick) and not doubleClicked):
                            ClickMouseLeft()
                            doubleClicked = True
                        if (len(rightFingers) != 5 or any(rightFingers[i] == 1 for i in nonDoubleClick)
                                or (not rightFingers[1] or not rightFingers[2])):
                            doubleClicked = False

                        # Double click: thumb+index up
                        nonClick = [2, 3, 4]
                        if (len(rightFingers) == 5 and rightFingers[0] and rightFingers[1]
                                and all(rightFingers[i] == 0 for i in nonClick) and not clicked):
                            DoubleClickMouseLeft()
                            clicked = True
                        if (len(rightFingers) != 5 or any(rightFingers[i] == 1 for i in nonClick)
                                or (not rightFingers[0] or not rightFingers[1])):
                            clicked = False

                        # Enter draw mode via header button
                        nonSel = [0, 3, 4]
                        if (len(rightFingers) == 5 and rightFingers[1] and rightFingers[2]
                                and all(rightFingers[i] == 0 for i in nonSel)):
                            xp, yp = [x1, y1]
                            if y1 < 125:
                                if 170 < x1 < 295:
                                    header = overlayList[0] if overlayList else header
                                    mode = "draw"

                        # ---- Left-hand actions ----
                        # Right arrow
                        nonToRight = [1, 2, 3, 4]
                        if len(leftFingers) == 5 and leftFingers[0] == 1 and all(leftFingers[i] == 0 for i in nonToRight) and not clickRight:
                            Press('right'); clickRight = True
                        if len(leftFingers) != 5 or leftFingers[0] == 0 or any(leftFingers[i] == 1 for i in nonToRight):
                            clickRight = False

                        # Up arrow
                        nonToUp = [0, 2, 3, 4]
                        if len(leftFingers) == 5 and leftFingers[1] == 1 and all(leftFingers[i] == 0 for i in nonToUp) and not clickTop:
                            Press('up'); clickTop = True
                        if len(leftFingers) != 5 or (leftFingers[1] == 0 and leftFingers[0] == 0) or any(leftFingers[i] == 1 for i in nonToUp):
                            clickTop = False

                        # Left arrow
                        nonToLeft = [0, 1, 2, 3]
                        if len(leftFingers) == 5 and leftFingers[4] == 1 and all(leftFingers[i] == 0 for i in nonToLeft) and not clickLeft:
                            Press('left'); clickLeft = True
                        if len(leftFingers) != 5 or leftFingers[4] == 0 or any(leftFingers[i] == 1 for i in nonToLeft):
                            clickLeft = False

                        # Down arrow
                        nonToDown = [1, 2, 3, 4]
                        if len(leftFingers) == 5 and leftFingers[0] == 0 and all(leftFingers[i] == 1 for i in nonToDown) and not clickDown:
                            Press('down'); clickDown = True
                        if len(leftFingers) != 5 or leftFingers[0] == 1 or any(leftFingers[i] == 0 for i in nonToDown):
                            clickDown = False

                        # Screenshot (PrintScreen)
                        if len(leftFingers) == 5 and all(leftFingers):
                            if not screenshoted:
                                Press('prtscr'); screenshoted = True
                        else:
                            screenshoted = False

                    # ---- Draw mode ----
                    if mode == "draw":
                        fingers = []
                        # thumb
                        fingers.append(1 if hand[tipIds[0]][0] < hand[tipIds[0] - 1][0] else 0)
                        # others
                        for id_ in range(1, 5):
                            fingers.append(1 if hand[tipIds[id_]][1] < hand[tipIds[id_] - 2][1] else 0)

                        # selection (two fingers)
                        nonSel = [0, 3, 4]
                        if (fingers[1] and fingers[2]) and all(fingers[i] == 0 for i in nonSel):
                            xp, yp = [x1, y1]
                            if y1 < 125:
                                if 170 < x1 < 295:
                                    header = overlayList[0] if overlayList else header
                                    drawColor = (0, 0, 255)
                                elif 436 < x1 < 561:
                                    header = overlayList[1] if len(overlayList) > 1 else header
                                    drawColor = (255, 0, 0)
                                elif 700 < x1 < 825:
                                    header = overlayList[2] if len(overlayList) > 2 else header
                                    drawColor = (0, 255, 0)
                                elif 980 < x1 < 1105:
                                    header = overlayList[3] if len(overlayList) > 3 else header
                                    drawColor = (0, 0, 0)
                                elif 30 < x1 < 100:
                                    header = overlayList[-1] if overlayList else header
                                    drawColor = (0, 0, 255)
                                    thickness = 20
                                    mode = "default"
                                    xp, yp = [0, 0]
                                    imgCanvas = np.zeros((height, width, 3), np.uint8)

                            cv2.rectangle(frame, (x1 - 10, y1 - 15), (x2 + 10, y2 + 23), drawColor, cv2.FILLED)

                        # standby: index + pinky
                        nonStand = [0, 2, 3]
                        if (fingers[1] and fingers[4]) and all(fingers[i] == 0 for i in nonStand):
                            cv2.line(frame, (xp, yp), (x4, y4), drawColor, 5)
                            xp, yp = [x1, y1]

                        # draw: only index
                        nonDraw = [0, 2, 3, 4]
                        if fingers[1] and all(fingers[i] == 0 for i in nonDraw):
                            cv2.circle(frame, (x1, y1), int(thickness/2), drawColor, cv2.FILLED)
                            if xp == 0 and yp == 0:
                                xp, yp = [x1, y1]
                            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, thickness)
                            xp, yp = [x1, y1]

                        # clear
                        if all(f == 0 for f in fingers):
                            imgCanvas = np.zeros((height, width, 3), np.uint8)
                            xp, yp = [x1, y1]

                        # thickness adjust via index + thumb
                        selecting = [1, 1, 0, 0, 0]
                        setting =   [1, 1, 0, 0, 1]
                        if fingers == selecting or fingers == setting:
                            r = int(math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) / 3)
                            x0, y0 = [(x1 + x3) / 2, (y1 + y3) / 2]
                            v1, v2 = [x1 - x3, y1 - y3]
                            v1, v2 = [-v2, v1]
                            mod_v = math.sqrt(v1 ** 2 + v2 ** 2) or 1.0
                            v1, v2 = [v1 / mod_v, v2 / mod_v]
                            c = 3 + r
                            x0, y0 = [int(x0 - v1 * c), int(y0 - v2 * c)]
                            cv2.circle(frame, (x0, y0), int(r / 2), drawColor, -1)
                            if fingers[4]:
                                thickness = max(1, r)
                            xp, yp = [x1, y1]

                # composite canvas
                try:
                    frame[0:125, 0:width] = header
                except Exception:
                    pass

                imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
                _, imgInv = cv2.threshold(imgGray, 5, 255, cv2.THRESH_BINARY_INV)
                imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
                img = cv2.bitwise_and(frame, imgInv)
                img = cv2.bitwise_or(img, imgCanvas)

                cv2.imshow("Hand Controller", img)

                # exit on ESC or window close
                if cv2.waitKey(1) == 27 or cv2.getWindowProperty('Hand Controller', cv2.WND_PROP_VISIBLE) < 1:
                    break

    finally:
        try:
            capture.release()
        except Exception:
            pass
        cv2.destroyAllWindows()


# allow running as script AND importing from app.py
if __name__ == "__main__":
    main()
    



    

