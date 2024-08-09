import numpy as np
import pyscreenshot
from PIL import Image, ImageGrab
# import pytesseract 
import pyautogui as py
import time
# import cv2

clicks = 0

class Tile:
  def __init__(self):
    self.disc = False
    self.flag = False
    self.num = 0
    self.finished = False

def check_if_discovered(r, g, b):
    if r >= 140 and r <= 200 and g >= 175 and b <= 150:
        return False
    elif r >= 155 and r <= 165 and g >= 205 and g <= 215 and b >= 70 and b <= 80:
        return False
    return True

def check_if_flag(r, g, b):
    if r >= 200 and g <= 60 and b <= 50:
        return True
    return False

def what_num(r, g, b, x, y, numArr):
    if r <= 70 and g <= 150 and b >= 150:
        numArr[0].append((x,y))
        return 1
    elif r <= 75 and g >= 100 and b <= 75:
        numArr[1].append((x,y))
        return 2
    elif r >= 170 and g <= 100 and b <= 100:
        numArr[2].append((x,y))
        return 3
    else:
        r,g,b,a = pixels[23 + y * 31, 22 + 31 * x]
        if r >= 115 and r <= 175 and g <= 100 and b >= 115 and b <= 175:
            numArr[3].append((x,y))
            return 4
        elif r >= 200 and g >= 100 and g <= 175 and b <= 60:
            numArr[4].append((x,y))
            return 5
        #elif 5?
    return 0
    #elif 6?

def check_if_can_mark_flags(x, y, num, tileArr):
    undisc_count = 0
    undisc_arr = []
    for i in [-1, 0, 1]:
        if not ((i == -1 and x == 0) or (i == 1 and x == 7)):
            if y != 9 and not tileArr[x + i, y + 1].disc:
                undisc_count += 1
                undisc_arr.append((x + i, y + 1))
            if y != 0 and not tileArr[x + i, y - 1].disc:
                undisc_count += 1
                undisc_arr.append((x + i, y - 1))
            if i != 0 and not tileArr[x + i, y].disc:
                undisc_count += 1
                undisc_arr.append((x + i, y))
        if undisc_count >= num + 1:
            return []
    return undisc_arr
    
def surrounding_undiscs(x, y, tileArr):
    undisc_arr = []
    for i in [-1, 0, 1]:
        if not ((i == -1 and x == 0) or (i == 1 and x == 7)):
            if y != 9 and not tileArr[x + i, y + 1].disc:
                undisc_arr.append((x + i, y + 1))
            if y != 0 and not tileArr[x + i, y - 1].disc:
                undisc_arr.append((x + i, y - 1))
            if i != 0 and not tileArr[x + i, y].disc:
                undisc_arr.append((x + i, y))
    return undisc_arr

def check_if_can_clear(x, y, num, tileArr):
    flags_spotted = 0
    for i in [-1, 0, 1]:
        if not ((i == -1 and x == 0) or (i == 1 and x == 7)):
            if y != 9 and tileArr[x + i, y + 1].flag:
                flags_spotted += 1
            if y != 0 and tileArr[x + i, y - 1].flag:
                flags_spotted += 1
            if i != 0 and tileArr[x + i, y].flag:
                flags_spotted += 1
    if flags_spotted > num:
        print("BIG PROBLEM!!! At ", x, y)
        printArray(tileArr)
        exit()
    if flags_spotted == num:
        return True
    return False

def clear_around_you(x, y, tileArr, add_tiles_arr):
    for i in [-1, 0, 1]:
        if not ((i == -1 and x == 0) or (i == 1 and x == 7)):
            if y != 9 and not tileArr[x + i, y + 1].disc and not tileArr[x + i, y + 1].flag:
                py.click(baseY + 28 + (y + 1) * 56, baseX + 28 + 56 * (x + i))
                tileArr[x + i, y + 1].disc = True
                add_tiles_arr.append((x + i, y + 1))
                # clicks += 1
            if y != 0 and not tileArr[x + i, y - 1].disc and not tileArr[x + i, y - 1].flag:
                py.click(baseY + 28 + (y - 1) * 56, baseX + 28 + 56 * (x + i))
                tileArr[x + i, y - 1].disc = True
                add_tiles_arr.append((x + i, y - 1))
                # clicks += 1
            if i != 0 and not tileArr[x + i, y].disc and not tileArr[x + i, y].flag:
                py.click(baseY + 28 + y * 56, baseX + 28 + 56 * (x + i))
                tileArr[x + i, y].disc = True
                add_tiles_arr.append((x + i, y))
                # clicks += 1

def special_1_1_edge(listA, listB, add_tiles_arr):
    listDiff = []
    for element in listB:
        if element not in listA:
            listDiff.append(element)
    # print("listA: ", listA)
    # print("listBs: ", listB)

    # print(listDiff)
    if len(listDiff) == 1:
        listX, listY = listDiff[0]
        py.click(baseY + 28 + listY * 56, baseX + 28 + 56 * listX)
        tileArr[listX, listY].disc = True
        add_tiles_arr.append((listX, listY))

def printArray(tileArr):
    print("nums:")
    for x in range(hard_row):
        print("[", end=" ")
        for y in range(hard_col):
            print(tileArr[x, y].num, end=" ")
        print("]")

    print("discovered:")
    for x in range(hard_row):
        print("[", end=" ")
        for y in range(hard_col):
            if tileArr[x, y].disc == True:
                print("T", end=" ")
            else:
                print("F", end=" ")
        print("]")

time.sleep(1) # delay to switch to minesweeper

screenWidth, screenHeight = py.size() # Get the size of the primary monitor.
print(screenWidth, screenHeight)

currentMouseX, currentMouseY = py.position() # Get the XY position of the mouse.
print("mouse coords", currentMouseX, currentMouseY)

# For Easy mode: top left = 680, 326 | bottom right = 1243 851

py.click(1215, 823)

time.sleep(1) # break it

# for easy

baseX = 311
baseY = 585
# im2 = ImageGrab.grab(bbox = (680, 398, 1241, 848), xdisplay=":0") 

# im2 = pyscreenshot.grab(bbox = (680, 398, 1241, 848))
# im2.save('temptemp.jpg')

# box sides = 56 pixels
# half a box = 26 pixels

im = Image.open("realhard.png")
# im1 = im.crop((585, 311, 1335, 937))
# im1.save("realhard.png")
pixels = im.load()

hard_row = 20
hard_col = 24
tile = Tile()
tileArr = np.full(shape=(hard_row, hard_col), fill_value=tile, dtype=Tile)
numArr = [[], [], [], [], [], []]
# print(a)

flags_used = 0
tiles_disc = 0
for x in range(hard_row):
    for y in range(hard_col):
        tile = Tile()

        red,gre,blu,a = pixels[3 + y * 31, 3 + 31 * x]
        if x == 17 and y == 0:
            print("Position: [" + str(x) + "," + str(y) + "]", "(", red, gre, blu, ")")
            py.click(baseY + 3 + y * 31, baseX + 3 + x * 31, button='right')
        if check_if_discovered(red, gre, blu):
            tile.disc = True
            tiles_disc += 1

        r,g,b,a = pixels[8 + y * 31, 10 + 31 * x]
        if x == 15 and y == 0:
            print("Flag: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
        if not tile.disc and check_if_flag(r, g, b):
            tile.flag = True
            tile.num = "•"
            flags_used += 1
            

        r,g,b,a = pixels[15 + y * 31, 15 + 31 * x]
        if x == 2 and y == 1:
            print("Num: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
        tempnum = what_num(r, g, b, x, y, numArr)
        if tile.num != "•":
            tile.num = tempnum

        tileArr[x, y] = tile

printArray(tileArr)

# add_tiles_arr = []
# count = 1
# while flags_used < 10:

#     if count % 25 == 0:
#         time.sleep(0.1)
#         im2 = ImageGrab.grab(bbox = (680, 398, 1241, 848)) 
#         im2.save('temptemp.jpg')
#         im = Image.open("temptemp.jpg")
#         pixels = im.load()

#         for x in range(hard_row):
#             for y in range(hard_col):
#                 red,gre,blu = pixels[5 + y * 56, 10 + 56 * x]
#                 # print("Position: [" + str(x) + "," + str(y) + "]", "(", red, gre, blu, ")")
#                 if check_if_discovered(red, gre, blu) and not tileArr[x, y].disc:
#                     tileArr[x, y].disc = True

#                 r,g,b = pixels[28 + y * 56, 24 + 56 * x]
#                 # print("Flag: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
#                 if not tileArr[x, y].disc and not tileArr[x, y].flag:
#                     if check_if_flag(r, g, b):
#                         tileArr[x, y].flag = True
#                         tileArr[x, y].num = "•"
#                         flags_used += 1

#                 r,g,b = pixels[28 + y * 56, 43 + 56 * x]
#                 # print("Position: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
#                 tempnum = what_num(r, g, b, x, y, numArr)
#                 if tileArr[x, y].num != "•":
#                     tileArr[x, y].num = tempnum
        
#         for x,y in numArr[0]:
#             if x == 0 and tileArr[x, y].num == 1 and tileArr[x + 1, y].num == 1:
#                 listA = surrounding_undiscs(x, y, tileArr)
#                 listB = surrounding_undiscs(x + 1, y, tileArr)
#                 special_1_1_edge(listA, listB)
#             elif x == 7 and tileArr[x, y].num == 1 and tileArr[x - 1, y].num == 1:
#                 listA = surrounding_undiscs(x, y, tileArr)
#                 listB = surrounding_undiscs(x - 1, y, tileArr)
#                 special_1_1_edge(listA, listB)
#             if y == 0 and tileArr[x, y].num == 1 and tileArr[x, y + 1].num == 1:
#                 listA = surrounding_undiscs(x, y, tileArr)
#                 listB = surrounding_undiscs(x, y + 1, tileArr)
#                 special_1_1_edge(listA, listB)
#             elif y == 9 and tileArr[x, y].num == 1 and tileArr[x, y - 1].num == 1:
#                 listA = surrounding_undiscs(x, y, tileArr)
#                 listB = surrounding_undiscs(x, y - 1, tileArr)
#                 special_1_1_edge(listA, listB)


#     # mark the flags
#     for i, arr in enumerate(numArr):
#         for x,y in arr:
#             undisc_arr = check_if_can_mark_flags(x, y, i + 1, tileArr)
#             # print(undisc_arr)
#             if len(undisc_arr) == i + 1:
#                 for xArr, yArr in undisc_arr:
#                     if not tileArr[xArr, yArr].flag:
#                         py.click(baseY + 28 + yArr * 56, baseX + 28 + 56 * xArr, button='right')
#                         tileArr[xArr, yArr].flag = True
#                         tileArr[xArr, yArr].num = "•"
#                         flags_used += 1
#                         # clicks += 1

#     # use the flags
#     for i, arr in enumerate(numArr):
#         for x,y in arr:
#             if check_if_can_clear(x, y, i + 1, tileArr):
#                 # print(x, y, "can clear")
#                 clear_around_you(x, y, tileArr, add_tiles_arr)
        
#     # add any tiles just discovered to arrays
#     for x,y in add_tiles_arr:
#         r,g,b = pixels[28 + y * 56, 43 + 56 * x]
#         # print("Position: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
#         tempnum = what_num(r, g, b, x, y, numArr)
#         if tile.num != "•":
#             tile.num = tempnum
    
#     count += 1


# for x in range(hard_row):
#     for y in range(hard_col):
#         if not tileArr[x,y].disc and not tileArr[x,y].flag:
#             py.click(baseY + 28 + y * 56, baseX + 28 + 56 * x)

# print("Complete!!", flags_used, "flags used and in", count, "iterations.")
# time.sleep(0.2)
# im2 = ImageGrab.grab(bbox = (680, 398, 1241, 848)) 
# im2.save('finished.jpg')
# printArray(tileArr)