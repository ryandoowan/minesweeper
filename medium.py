import numpy as np
from PIL import Image, ImageGrab
import pyautogui as py
import time
import sys

clicks = 0

class Tile:
  def __init__(self):
    self.disc = False
    self.flag = False
    self.num = 0
    self.finished = False

def check_if_discovered(r, g, b):
    if r >= 150 and r <= 200 and g >= 200 and b <= 150:
        return False
    elif r >= 155 and r <= 165 and g >= 205 and g <= 215 and b >= 70 and b <= 80:
        return False
    return True

def check_if_flag(r, g, b):
    if r >= 200 and g <= 60 and b <= 50:
        return True
    return False

def what_num(r, g, b, x, y, numArr):
    if b >= 150:
        numArr[0].append((x,y))
        return 1
    elif r <= 75 and g >= 100 and b <= 75:
        numArr[1].append((x,y))
        return 2
    elif r >= 170 and g <= 100 and b <= 100:
        numArr[2].append((x,y))
        return 3
    else:
        r,g,b = pixels[(5 * box_sides / 8) + y * box_sides, (2 * box_sides / 3) + box_sides * x]
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
                py.click(baseY + half_box + (y + 1) * box_sides, baseX + half_box + box_sides * (x + i))
                tileArr[x + i, y + 1].disc = True
                add_tiles_arr.append((x + i, y + 1))
                # clicks += 1
            if y != 0 and not tileArr[x + i, y - 1].disc and not tileArr[x + i, y - 1].flag:
                py.click(baseY + half_box + (y - 1) * box_sides, baseX + half_box + box_sides * (x + i))
                tileArr[x + i, y - 1].disc = True
                add_tiles_arr.append((x + i, y - 1))
                # clicks += 1
            if i != 0 and not tileArr[x + i, y].disc and not tileArr[x + i, y].flag:
                py.click(baseY + half_box + y * box_sides, baseX + half_box + box_sides * (x + i))
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
        py.click(baseY + half_box + listY * box_sides, baseX + half_box + box_sides * listX)
        tileArr[listX, listY].disc = True
        add_tiles_arr.append((listX, listY))

def printArray(tileArr):
    for x in range(row):
        print("[", end=" ")
        for y in range(col):
            print(tileArr[x, y].num, end=" ")
        print("]")

    for x in range(row):
        print("[", end=" ")
        for y in range(col):
            print(tileArr[x, y].disc, end=" ")
        print("]")

time.sleep(1) # delay to switch to minesweeper"

screenWidth, screenHeight = py.size() # Get the size of the primary monitor.
print(screenWidth, screenHeight)

currentMouseX, currentMouseY = py.position() # Get the XY position of the mouse.
print("mouse coords", currentMouseX, currentMouseY)

if len(sys.argv) == 2:
    mode = sys.argv[1]
else:
    # default = easy
    mode = "easy"

# For Easy mode: top left = 680, 326 | bottom right = 1243 851

if mode == "easy":
    py.click(1215, 823)

    time.sleep(1) # break it
    baseX = 398
    baseY = 680
    im2 = ImageGrab.grab(bbox = (680, 398, 1241, 848)) 
    box_sides = 56
    half_box = 26
    row = 8    
    col = 10
elif mode == "medium":
    py.click(1278, 867)

    time.sleep(1) # break it
    baseX = 361
    baseY = 623
    im2 = ImageGrab.grab(bbox = (623, 361, 1297, 886))
    box_sides = 37
    half_box = 19
    row = 14
    col = 18
elif mode == "hard":
    idk = 0

im2.save('medium.jpg')
im = Image.open("medium.jpg")
pixels = im.load()

tile = Tile()
tileArr = np.full(shape=(row, col), fill_value=tile, dtype=Tile)
numArr = [[], [], [], [], [], []]

# print(a)



flags_used = 0
tiles_disc = 0
for x in range(row):
    for y in range(col):
        tile = Tile()

        red,gre,blu = pixels[(box_sides / 11) + y * box_sides, (2 * box_sides / 11) + box_sides * x]
        # print("Position: [" + str(x) + "," + str(y) + "]", "(", red, gre, blu, ")")
        if check_if_discovered(red, gre, blu):
            tile.disc = True
            tiles_disc += 1

        r,g,b = pixels[half_box + y * box_sides, (3 * box_sides / 7) + box_sides * x]
        # print("Flag: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
        if not tile.disc and check_if_flag(r, g, b):
            tile.flag = True
            tile.num = "•"
            

        r,g,b = pixels[half_box + y * box_sides, (3 * box_sides / 4) + box_sides * x]
        if x == 2 and y == 3:
            print("Position: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
        tempnum = what_num(r, g, b, x, y, numArr)
        if tile.num != "•":
            tile.num = tempnum

        tileArr[x, y] = tile

printArray(tileArr)

add_tiles_arr = []
count = 1
while flags_used < 10:

    if count % 25 == 0:
        time.sleep(0.5)
        if mode == "easy":
            im2 = ImageGrab.grab(bbox = (680, 398, 1241, 848)) 
        elif mode == "medium":
            im2 = ImageGrab.grab(bbox = (623, 361, 1297, 886)) 
        im2.save('medium.jpg')
        im = Image.open("medium.jpg")
        pixels = im.load()

        for x in range(row):
            for y in range(col):
                red,gre,blu = pixels[(box_sides / 11) + y * box_sides, (2 * box_sides / 11) + box_sides * x]
                # print("Position: [" + str(x) + "," + str(y) + "]", "(", red, gre, blu, ")")
                if check_if_discovered(red, gre, blu) and not tileArr[x, y].disc:
                    tileArr[x, y].disc = True

                r,g,b = pixels[half_box + y * box_sides, (3 * box_sides / 7) + box_sides * x]
                # print("Flag: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
                if not tileArr[x, y].disc and not tileArr[x, y].flag:
                    if check_if_flag(r, g, b):
                        tileArr[x, y].flag = True
                        tileArr[x, y].num = "•"
                        flags_used += 1

                r,g,b = pixels[half_box + y * box_sides, (3 * box_sides / 4) + box_sides * x]
                # print("Position: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
                tempnum = what_num(r, g, b, x, y, numArr)
                if tileArr[x, y].num != "•":
                    tileArr[x, y].num = tempnum
        
        for x,y in numArr[0]:
            if x == 0 and tileArr[x, y].num == 1 and tileArr[x + 1, y].num == 1:
                listA = surrounding_undiscs(x, y, tileArr)
                listB = surrounding_undiscs(x + 1, y, tileArr)
                special_1_1_edge(listA, listB, add_tiles_arr)
            elif x == 7 and tileArr[x, y].num == 1 and tileArr[x - 1, y].num == 1:
                listA = surrounding_undiscs(x, y, tileArr)
                listB = surrounding_undiscs(x - 1, y, tileArr)
                special_1_1_edge(listA, listB, add_tiles_arr)
            if y == 0 and tileArr[x, y].num == 1 and tileArr[x, y + 1].num == 1:
                listA = surrounding_undiscs(x, y, tileArr)
                listB = surrounding_undiscs(x, y + 1, tileArr)
                special_1_1_edge(listA, listB, add_tiles_arr)
            elif y == 9 and tileArr[x, y].num == 1 and tileArr[x, y - 1].num == 1:
                listA = surrounding_undiscs(x, y, tileArr)
                listB = surrounding_undiscs(x, y - 1, tileArr)
                special_1_1_edge(listA, listB, add_tiles_arr)

    # mark the flags
    for i, arr in enumerate(numArr):
        for x,y in arr:
            undisc_arr = check_if_can_mark_flags(x, y, i + 1, tileArr)
            # print(undisc_arr)
            if len(undisc_arr) == i + 1:
                for xArr, yArr in undisc_arr:
                    if not tileArr[xArr, yArr].flag:
                        py.click(baseY + half_box + yArr * box_sides, baseX + half_box + box_sides * xArr, button='right')
                        tileArr[xArr, yArr].flag = True
                        tileArr[xArr, yArr].num = "•"
                        flags_used += 1
                        # clicks += 1

    # use the flags
    for i, arr in enumerate(numArr):
        for x,y in arr:
            if check_if_can_clear(x, y, i + 1, tileArr):
                # print(x, y, "can clear")
                clear_around_you(x, y, tileArr, add_tiles_arr)
        
    # add any tiles just discovered to arrays
    for x,y in add_tiles_arr:
        r,g,b = pixels[half_box + y * box_sides, (3 * box_sides / 4) + box_sides * x]
        # print("Position: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
        tempnum = what_num(r, g, b, x, y, numArr)
        if tile.num != "•":
            tile.num = tempnum
    
    count += 1


for x in range(row):
    for y in range(col):
        if not tileArr[x,y].disc and not tileArr[x,y].flag:
            py.click(baseY + half_box + y * box_sides, baseX + half_box + box_sides * x)

print("Complete!!", flags_used, "flags used and in", count, "iterations.")
time.sleep(0.2)
im2 = ImageGrab.grab(bbox = (680, 398, 1241, 848)) 
im2.save('finished.jpg')
printArray(tileArr)