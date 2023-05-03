# This is a sample Python script.
import random

import pyautogui
import cv2 as OpenCV
import time
import os
import sys
import numpy

howManyFiles = 0
files = []
fileName = ""
currentPath = 'C:/Users/itsaz/PycharmProjects/pythonProject/Photos/'

lower_white = numpy.array([0, 0, 200])
upper_white = numpy.array([180, 30, 255])


# print(pyautogui.mouseInfo())
def removefile(fileName):
    os.remove(currentPath + fileName)


def removeAllFiles():
    for x in list(files):
        files.remove(x)
        removefile(x)
        time.sleep(0.01)


def screenshotandsave(filename):
    filename = filename + '.png'
    screenshot = pyautogui.screenshot(region=(1375, 30, 520, 295))
    screenshot.save(currentPath + filename)
    files.append(filename)
    print("Made File:[" + filename + ']')


# for i in range(10):
#     screenshotandsave("game_" + str(i))
#     time.sleep(10)
# print(files)

def readfile(filename):
    stuff = currentPath + filename
    img = OpenCV.imread(currentPath + filename)
    return img


screenshotandsave("New_York")


def showfile(filename):
    OpenCV.imshow(readfile(filename))


# removeAllFiles()


# you might not get anything at all something about how it changes it
# grey if the map is white then it's too hard to mess up
# New york is solid


def checkTransitLocation(givenX, givenY, diction):
    for xele, yele in diction.values():
        if abs(givenX - xele) <= 15 and abs(givenY - yele) <= 15 and givenX > 50:
            return False
    return True


def addLocations():
    TransitLocation = {}
    # empty starts an empty Array
    howManyStations = 0
    # this is to keep count of our locations
    screenshotandsave("current_Map")
    map = readfile('current_Map.png')

    greyMap = OpenCV.cvtColor(map, OpenCV.COLOR_BGR2GRAY)
    stationMap = OpenCV.threshold(greyMap, 240, 255, OpenCV.THRESH_BINARY)[1]
    # this makes a usable map, it'll only prints absolute white dots you can call the map
    # this becomes an issue if the map has anny white, it doesn't consider the white for the trains or nothing like that
    # New York works fine becuz its mimics the real life transit
    #
    # print("Start:[================================================================]")
    for y in range(stationMap.shape[0]):
        for x in range(stationMap.shape[1]):
            if stationMap.item(y, x) == 255:
                currentX = x
                currentY = y
                # print("X:[" + str(currentX) + "]  Y:[" + str(currentY) + "]")
                if checkTransitLocation(currentX, currentY, TransitLocation) and currentX > 60:
                    TransitLocation[howManyStations] = (currentX, currentY)
                    howManyStations += 1
    # print("End:[================================================================]")
    return stationMap, howManyStations, TransitLocation


# print(pyautogui.mouseInfo())

def connectLine(maps):
    firstStation = maps.get(0)
    pyautogui.moveTo(firstStation[0] + 1375, firstStation[1] + 32)
    pyautogui.click()

    for i in range(len(dict(maps)) - 1) :
        time.sleep(2)
        secondStation = maps.get(i+1)
        pyautogui.dragTo(secondStation[0] + 1375, secondStation[1] + 32,1,button='left')
        print(maps.get(i))

escape = 0
for i in range(600):
    if i % 5 == 0:
        values = addLocations()
        print(values[1])
        if 50 > len(values[2]) >= 2:
            connectLine(values[2])
            escape = 0

            # This means we might be able to play with it
        else:
            pyautogui.click()
            escape += 1
            pyautogui.click()
            pyautogui.move(random.randint(-20,20),random.randint(-20,20))
            print("We've hit a screen where theres to much white im just gonna click and hopefully i make it, ")

            if(escape > 4 ):
                print("nothing is working i don't wanna do this no more i quit")
                i = 600
                break;


    time.sleep(1)
