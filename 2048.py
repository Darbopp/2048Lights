'''
Darius Bopp
Window 2048
'''
import random
import curses
import subprocess
import socket
import math
import json
#from neoclient import *

def makeBoard(boardSize):
    board = []
    for row in range(boardSize): board += [[0]*boardSize]
    return board

def makeStripBoard():
    stripBoard = []
    

def makeDicts(numberOfColors):
    alphabetString = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    alphabetList = alphabetString.split()
    NumberToLetter = {0 : "_"}
    LetterToColor = {}

    freq = .65

    for i in range(numberOfColors):
        NumberToLetter[2**(i+1)] = alphabetList[i]

        red = int(math.sin(freq*i+2)*127 + 128)
        blue = int(math.sin(freq*i+4)*127 + 128)
        green = int(math.sin(freq*i+6)*127 + 128)

        LetterToColor[alphabetList[i]] = (int(red), int(blue), int(green))

    return (NumberToLetter, LetterToColor)

def printBoard(board, nTCL):

    didWin = False

    boardString = "2 0 4 8 \n"

    for row in board:
        for value in row:
            if value not in nTCL or didWin:
                didWin = True
            else:
                boardString += nTCL[value] + " "
        boardString += "\n"
    boardString += "=======\n"

    if didWin:
        print("YOU WIN!\n")
    else:
        print(boardString)

'''
def showBoard(board, LtC, strips):

    for rowNum, row in enumerate(board):
        strip = strips[rowNum]
        strip.begin()
        for colNum, letter in enumerate(row):
            red = LtC[letter][0]
            blue = LtC[letter][1]
            green = LtC[letter][2]

            for i in range(colNum*30, (colNum+1)*30):
                strip.PixelColor(i, Color(red, blue, green))
            
        strip.show()

'''

def showBoard(board, LtC, strips, sock):

    pis = ["RPi5","RPi4","RPI3","RPi2"]

    for rowNum, row in enumerate(board):
        pi = strips[pis[rowNum]]

        byteList = bytearray()

        for colNum, letter in enumerate(row):
            red = LTC[letter][0]
            blue = LtC[letter][1]
            green = LtC[letter][2]

            byteList.append(red)
            byteList.append(blue)
            byteList.append(green)

        piIP = pi["ip"]
        piPort = pi["port"]

        server_address(piIP, piPort)

        sent = sock.sendto(byteList, server_address)


            
def add2(board):
    added = False

    while (not added):
        row = random.randint(0,len(board)-1)
        col = random.randint(0,len(board)-1)

        if (board[row][col] == 0):
            board[row][col] = 2
            added = True

def getInput():
    keysToNums = { "w" : 0, "d" : 1, "s" : 2, "a" : 3, "q" : 4}
    inputKey = 4
    gotInput = False

    inputString = input()
    if inputString not in keysToNums:
        print("Wrong Input. Now quitting.")
        return(4)
    else:
        return (keysToNums[inputString])

def moveBlockUp(board, mergeBoard, rowNum, colNum):
    canMove = True

    while (canMove):
        moveToValue = board[rowNum-1][colNum]

        #Moving into an empty square
        if moveToValue == 0:
            board[rowNum-1][colNum] = board[rowNum][colNum]
            board[rowNum][colNum] = 0

            if rowNum-1 == 0:
                canMove = False
            else:
                rowNum = rowNum - 1

        #Moving into a square of the same value
        elif moveToValue == board[rowNum][colNum]:
            if not mergeBoard[rowNum-1][colNum] and not mergeBoard[rowNum][colNum]:
                board[rowNum-1][colNum] = 2 * moveToValue
                board[rowNum][colNum] = 0
                mergeBoard[rowNum-1][colNum] = True

                if rowNum-1 == 0:
                    canMove = False
                else:
                    rowNum = rowNum - 1
            else:
                canMove = False
        
        #Blocked
        else:
            canMove = False

def moveBlockDown(board, mergeBoard, rowNum, colNum):
    canMove = True

    while (canMove):
        moveToValue = board[rowNum+1][colNum]

        #Moving into an empty square
        if moveToValue == 0:
            board[rowNum+1][colNum] = board[rowNum][colNum]
            board[rowNum][colNum] = 0

            if rowNum+1 == len(board)-1:
                canMove = False
            else:
                rowNum = rowNum + 1

        #Moving into a square of the same value
        elif moveToValue == board[rowNum][colNum]:
            if not mergeBoard[rowNum+1][colNum] and not mergeBoard[rowNum][colNum]:
                board[rowNum+1][colNum] = 2 * moveToValue
                board[rowNum][colNum] = 0
                mergeBoard[rowNum+1][colNum] = True

                if rowNum+1 == len(board)-1:
                    canMove = False
                else:
                    rowNum = rowNum + 1
            else:
                canMove = False
        
        #Blocked
        else:
            canMove = False    

def moveBlockLeft(board, mergeBoard, rowNum, colNum):
    canMove = True

    while (canMove):
        moveToValue = board[rowNum][colNum-1]

        #Moving into an empty square
        if moveToValue == 0:
            board[rowNum][colNum-1] = board[rowNum][colNum]
            board[rowNum][colNum] = 0

            if colNum-1 == 0:
                canMove = False
            else:
                colNum = colNum - 1

        #Moving into a square of the same value
        elif moveToValue == board[rowNum][colNum]:
            if not mergeBoard[rowNum][colNum-1] and not mergeBoard[rowNum][colNum]:
                board[rowNum][colNum-1] = 2 * moveToValue
                board[rowNum][colNum] = 0
                mergeBoard[rowNum][colNum-1] = True

                if colNum-1 == 0:
                    canMove = False
                else:
                    colNum = colNum - 1
            else:
                canMove = False
        
        #Blocked
        else:
            canMove = False


def moveBlockRight(board, mergeBoard, rowNum, colNum):
    canMove = True

    while (canMove):
        moveToValue = board[rowNum][colNum+1]

        #Moving into an empty square
        if moveToValue == 0:
            board[rowNum][colNum+1] = board[rowNum][colNum]
            board[rowNum][colNum] = 0

            if colNum+1 == len(board)-1:
                canMove = False
            else:
                colNum = colNum + 1

        #Moving into a square of the same value
        elif moveToValue == board[rowNum][colNum]:
            if not mergeBoard[rowNum][colNum+1] and not mergeBoard[rowNum][colNum]:
                board[rowNum][colNum+1] = 2 * moveToValue
                board[rowNum][colNum] = 0
                mergeBoard[rowNum][colNum+1] = True

                if colNum+1 == len(board) - 1:
                    canMove = False
                else:
                    colNum = colNum + 1
            else:
                canMove = False
        
        #Blocked
        else:
            canMove = False

def moveBoardUp(board, mergeBoard):
    for rowNum, row in enumerate(board):
        if rowNum > 0:
            for colNum, block in enumerate(row):
                moveBlockUp(board, mergeBoard, rowNum, colNum)

def moveBoardDown(board, mergeBoard):
    for rowNum in reversed(range(len(board))):
        if rowNum < len(board)-1:
            row = board[rowNum]
            for colNum, block in enumerate(row):
                moveBlockDown(board, mergeBoard, rowNum, colNum)

def moveBoardLeft(board, mergeBoard):
    for colNum in range(len(board)):
        if colNum > 0:
            for rowNum in range(len(board)):
                moveBlockLeft(board, mergeBoard, rowNum, colNum)            

def moveBoardRight(board, mergeBoard):
    for colNum in reversed(range(len(board))):
        if colNum < len(board) -1:
            for rowNum in range(len(board)):
                moveBlockRight(board, mergeBoard, rowNum, colNum)


def enactInput(board, inputNum):

    mergeBoard = []
    for row in range(len(board)): mergeBoard += [[False]*len(board)]

    if inputNum == 0:
        #move up
        moveBoardUp(board, mergeBoard)

    elif inputNum == 1:
        #move right
        moveBoardRight(board, mergeBoard)

    elif inputNum == 2:
        #move down
        moveBoardDown(board, mergeBoard)
        
    elif inputNum == 3:
        #move left
        moveBoardLeft(board, mergeBoard)
        



if __name__ == '__main__':
    numsToColorLetters = { 0 : "_", 2 : "R", 4 : "O", 8: "Y", 
                          16 : "G", 32: "B", 64 : "I", 128 : "V"}

    numberOfColors = 3 #Cant be greater than 26

    dicts = makeDicts(numberOfColors)

    numsToLetters = dicts[0]
    lettersToColors = dicts[1]

    print(lettersToColors)

    boardSize = 4

    board = makeBoard(boardSize)

    printBoard(board, numsToLetters)

    '''
    LED_COUNT = 120
    strip0 = Adafruit_NeoPixel(LED_COUNT, 'pi.wsmoses.com', 4756)
    strip1 = Adafruit_NeoPixel(LED_COUNT, 'pi.wsmoses.com', 4756)
    strip2 = Adafruit_NeoPixel(LED_COUNT, 'pi.wsmoses.com', 4756)
    strip3 = Adafruit_NeoPixel(LED_COUNT, 'pi.wsmoses.com', 4756)
    strips = [strip0, strip1, strip2, strip3]
    '''

    #Internet connectivity stuff

    # allIPs = subprocess.Popen("hostname -I", stdout=subprocess.PIPE).stdout.read()
    # allIPList = allIPs.split()
    # firstIP = allIPList[0]

    # packetDict = {"ip":firstIP, "mac":"nothingRelevent", "msg_type":"startup"}
    # jsonPacket = json.dumps(packet)


    # # Create a UDP socket
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # server_address = ('129.0.0.0.1', 10000)
    # message = jsonPakcet

    # try:

    #     # Send data
    #     sent = sock.sendto(message, server_address)

    #     # Receive response
    #     data0, server0 = sock.recvfrom(0)
    #     data1, server1 = sock.recvfrom(1)
    #     data2, server2 = sock.recvfrom(2)
    #     data3, server3 = sock.recvfrom(3)

    # finally:
    #     sock.close()

    # dataDict0 = json.loads(data0)
    # dataDict1 = json.loads(data1)
    # dataDict2 = json.loads(data2)
    # dataDict3 = json.loads(data3)

    # strips = {dataDict0["name"]:dataDict0, dataDict1["name"]:dataDict1, dataDict2["name"]:dataDict2, dataDict3["name"]:dataDict3}




    add2(board)
    add2(board)

    printBoard(board, numsToLetters)

    while (True):
        inputNum = getInput()

        if inputNum == 4:
            break
        
        else:
            enactInput(board, inputNum)
            add2(board)
            printBoard(board, numsToLetters)
            #showBoard(board, lettersToColors, strips, sock)