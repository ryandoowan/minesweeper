import numpy as np
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
    self.eff_num = 0  # effective number

def check_if_discovered(r, g, b):
    if r >= 140 and r <= 200 and g >= 170 and b <= 100 and g > r:
        return False
    return True

def check_if_flag(r, g, b):
    if r >= 200 and g <= 60 and b <= 50:
        return True
    return False

def what_num(r, g, b, x, y, numArr):
    if r <= 100 and g <= 150 and b >= 150:
        numArr[0].append((x,y))
        return 1
    elif r <= 110 and g >= 100 and b <= 100:
        numArr[1].append((x,y))
        return 2
    elif r >= 170 and g <= 150 and b <= 150:
        # it could be 4
        if b > g and b >= 125 and g <= 125:
            r,g,b = pixels[20 + y * 31 + (y / 4), 20 + 31 * x + (x / 4)]
            if r >= 115 and r <= 175 and g <= 125 and b >= 115 and b <= 175:
                numArr[3].append((x,y))
                return 4
        numArr[2].append((x,y))
        return 3
    else:
        r,g,b = pixels[20 + y * 31 + (y / 4), 20 + 31 * x + (x / 4)]
        if r >= 115 and r <= 175 and g <= 125 and b >= 115 and b <= 200:
            numArr[3].append((x,y))
            return 4
        elif r >= 200 and g >= 100 and g <= 175 and b <= 60:
            numArr[4].append((x,y))
            return 5
        else:
            # rare 6 sighting
            r1,g1,b1 = pixels[11 + y * 31 + (y / 4), 19 + 31 * x + (x / 4)]
            r2,g2,b2 = pixels[20 + y * 31 + (y / 4), 19 + 31 * x + (x / 4)]
            if r2 < 50 and r1 < 50 and g1 > 125 and g2 > 125 and b1 > 125 and b2 > 125:
                numArr[5].append((x,y))
                return 6
    return 0

def check_if_can_mark_flags(x, y, num, tileArr):
    undisc_count = 0
    undisc_arr = []
    for i in [-1, 0, 1]:
        if not ((i == -1 and x == 0) or (i == 1 and x == 19)):
            if y != 23 and not tileArr[x + i, y + 1].disc:
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
        if not ((i == -1 and x == 0) or (i == 1 and x == 19)):
            if y != 23 and not tileArr[x + i, y + 1].disc and not tileArr[x + i, y + 1].flag:
                undisc_arr.append((x + i, y + 1))
            if y != 0 and not tileArr[x + i, y - 1].disc and not tileArr[x + i, y - 1].flag:
                undisc_arr.append((x + i, y - 1))
            if i != 0 and not tileArr[x + i, y].disc and not tileArr[x + i, y].flag:
                undisc_arr.append((x + i, y))
    return undisc_arr

def check_flags_around(x, y, tileArr):
    flags_spotted = 0
    for i in [-1, 0, 1]:
        if not ((i == -1 and x == 0) or (i == 1 and x == 19)):
            if y != 23 and tileArr[x + i, y + 1].flag:
                flags_spotted += 1
            if y != 0 and tileArr[x + i, y - 1].flag:
                flags_spotted += 1
            if i != 0 and tileArr[x + i, y].flag:
                flags_spotted += 1
    return flags_spotted

def clear_around_you(x, y, tileArr, add_tiles_arr):
    for i in [-1, 0, 1]:
        if not ((i == -1 and x == 0) or (i == 1 and x == 19)):
            if y != 23 and not tileArr[x + i, y + 1].disc and not tileArr[x + i, y + 1].flag:
                py.click(baseY + 15 + (y + 1) * 31 + (y / 4), baseX + 15 + 31 * (x + i) + (x / 4))
                tileArr[x + i, y + 1].disc = True
                add_tiles_arr.append((x + i, y + 1))
                # clicks += 1
            if y != 0 and not tileArr[x + i, y - 1].disc and not tileArr[x + i, y - 1].flag:
                py.click(baseY + 15 + (y - 1) * 31 + (y / 4), baseX + 15 + 31 * (x + i) + (x / 4))
                tileArr[x + i, y - 1].disc = True
                add_tiles_arr.append((x + i, y - 1))
                # clicks += 1
            if i != 0 and not tileArr[x + i, y].disc and not tileArr[x + i, y].flag:
                py.click(baseY + 15 + y * 31 + (y / 4), baseX + 15 + 31 * (x + i) + (x / 4))
                tileArr[x + i, y].disc = True
                add_tiles_arr.append((x + i, y))
                # clicks += 1

def update_eff_num(x, y, tileArr):
    for i in [-1, 0, 1]:
        if not ((i == -1 and x == 0) or (i == 1 and x == 19)):
            if y != 23 and tileArr[x + i, y + 1].num != "•":
                tileArr[x + i, y + 1].eff_num -= 1
            if y != 0 and tileArr[x + i, y - 1].num != "•":
                tileArr[x + i, y - 1].eff_num -= 1
            if i != 0 and tileArr[x + i, y].num != "•"!= "•":
                tileArr[x + i, y].eff_num -= 1

def special_1_1or1_2_case(listA, listB, add_tiles_arr, case, flags_used):
    listDiff = []
    for element in listB:
        if element not in listA:
            listDiff.append(element)
    # print("listA: ", listA)
    # print("listBs: ", listB)

    # print(listDiff)
    if len(listDiff) == 1:
        listX, listY = listDiff[0]
        if case == 1:
            py.click(baseY + 15 + listY * 31 + (listY / 4), baseX + 15 + 31 * listX + (listX / 4))
            tileArr[listX, listY].disc = True
            add_tiles_arr.append((listX, listY))
        elif case == 2:
            # marked as flag
            py.click(baseY + 15 + listY * 31 + (listY / 4), baseX + 15 + 31 * listX + (listX / 4), button="right")
            tileArr[listX, listY].flag = True
            tileArr[listX, listY].num = "•"
            flags_used += 1

            # need to update the eff_num around placed flag
            update_eff_num(listX, listY, tileArr)
        return True
    return False

def use_eff_num(x, y, listA, tileArr):
    listB = surrounding_undiscs(x, y, tileArr)
    if len(listB) == 3:
        if tileArr[x, y].eff_num == 1:
            return special_1_1or1_2_case(listA, listB, add_tiles_arr, 1, flags_used)
        elif tileArr[x, y].eff_num == 2:
            return special_1_1or1_2_case(listA, listB, add_tiles_arr, 2, flags_used)
    return False

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

py.click(960, 624)

time.sleep(1) # break it

# for easy

baseX = 311
baseY = 585
im2 = ImageGrab.grab(bbox = (585, 311, 1335, 937)) 

im2.save('temptemp.jpg')
print("screenshot done")

# box sides = 56 pixels
# half a box = 26 pixels

im = Image.open("temptemp.jpg")
# im1 = im.crop((585, 311, 1335, 937))
# im1.save("realhard.png")
pixels = im.load()

hard_row = 20
hard_col = 24
tile = Tile()
tileArr = np.full(shape=(hard_row, hard_col), fill_value=tile, dtype=Tile)
numArr = [[], [], [], [], [], [], []]
# print(a)

flags_used = 0
tiles_disc = 0
for x in range(hard_row):
    for y in range(hard_col):
        tile = Tile()

        red,gre,blu = pixels[3 + y * 31 + (y / 4), 3 + 31 * x + (x / 4)]
        if x == 17 and y == 0:
            print("Position: [" + str(x) + "," + str(y) + "]", "(", red, gre, blu, ")")
            # py.click(baseY + 3 + y * 31 + (y / 4), baseX + 3 + x * 31 + (x / 4), button='right')
        if check_if_discovered(red, gre, blu):
            tile.disc = True
            tiles_disc += 1

        r,g,b = pixels[8 + y * 31 + (y / 4), 10 + 31 * x + (x / 4)]
        if x == 15 and y == 0:
            print("Flag: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
        if not tile.disc and check_if_flag(r, g, b):
            tile.flag = True
            tile.num = "•"
            flags_used += 1
            

        r,g,b = pixels[17 + y * 31 + (y / 4), 17 + 31 * x + (x / 4)]
        if x == 2 and y == 20:
            print("Num: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
            # py.click(baseY + 11 + y * 31 + (y / 4), baseX + 19 + x * 31 + (x / 4), button='right')
        # for 4 and 5
        if x == 4 and y == 15:
            r,g,b = pixels[20 + y * 31 + (y / 4), 20 + 31 * x + (x / 4)]
            print("Num 4 or 5: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
            # py.click(baseY + 20 + y * 31 + (y / 4), baseX0+ 20 + 31 * x + (x / 4), button='right')
        tempnum = what_num(r, g, b, x, y, numArr)
        if tile.num != "•":
            tile.num = tempnum

        tileArr[x, y] = tile

printArray(tileArr)

count = 1
while flags_used < 99:
    add_tiles_arr = []
    if count % 5 == 0:
        im2 = ImageGrab.grab(bbox = (585, 311, 1335, 937)) 
        im2.save('temptemp.jpg')
        im = Image.open("temptemp.jpg")
        pixels = im.load()

        for x in range(hard_row):
            for y in range(hard_col):
                red,gre,blu = pixels[3 + y * 31 + (y / 4), 3 + 31 * x + (x / 4)]
                # print("Position: [" + str(x) + "," + str(y) + "]", "(", red, gre, blu, ")")
                if check_if_discovered(red, gre, blu) and not tileArr[x, y].disc and tileArr[x, y].num != "•":
                    tileArr[x, y].disc = True

                r,g,b = pixels[8 + y * 31 + (y / 4), 10 + 31 * x + (x / 4)]
                # print("Flag: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
                if not tileArr[x, y].disc and not tileArr[x, y].flag:
                    if check_if_flag(r, g, b):
                        tileArr[x, y].flag = True
                        tileArr[x, y].num = "•"
                        flags_used += 1

                r,g,b = pixels[17 + y * 31 + (y / 4), 17 + 31 * x + (x / 4)]
                # print("Position: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
                tempnum = what_num(r, g, b, x, y, numArr)
                if tileArr[x, y].num != "•":
                    tileArr[x, y].num = tempnum

                num_flags = check_flags_around(x, y, tileArr)
                if tileArr[x,y].num != "•":
                    tileArr[x, y].eff_num = int(tileArr[x, y].num) - num_flags
        
        for i, arr in enumerate(numArr):
            for x,y in arr:
                if tileArr[x, y].eff_num == 1:
                    listA = surrounding_undiscs(x, y, tileArr)
                    if len(listA) == 2:
                        if x != 19 and use_eff_num(x + 1, y, listA, tileArr):
                            continue
                        elif x != 0 and use_eff_num(x - 1, y, listA, tileArr):
                            continue
                        elif y != 23 and use_eff_num(x, y + 1, listA, tileArr):
                            continue
                        elif y != 0 and use_eff_num(x, y - 1, listA, tileArr):
                            continue

        # for x,y in numArr[0]:
        #     if x == 0 and tileArr[x, y].num == 1 and tileArr[x + 1, y].num == 1:
        #         listA = surrounding_undiscs(x, y, tileArr)
        #         listB = surrounding_undiscs(x + 1, y, tileArr)
        #         special_1_1_edge(listA, listB, add_tiles_arr)
        #     elif x == 19 and tileArr[x, y].num == 1 and tileArr[x - 1, y].num == 1:
        #         listA = surrounding_undiscs(x, y, tileArr)
        #         listB = surrounding_undiscs(x - 1, y, tileArr)
        #         special_1_1_edge(listA, listB, add_tiles_arr)
        #     if y == 0 and tileArr[x, y].num == 1 and tileArr[x, y + 1].num == 1:
        #         listA = surrounding_undiscs(x, y, tileArr)
        #         listB = surrounding_undiscs(x, y + 1, tileArr)
        #         special_1_1_edge(listA, listB, add_tiles_arr)
        #     elif y == 23 and tileArr[x, y].num == 1 and tileArr[x, y - 1].num == 1:
        #         listA = surrounding_undiscs(x, y, tileArr)
        #         listB = surrounding_undiscs(x, y - 1, tileArr)
        #         special_1_1_edge(listA, listB, add_tiles_arr)


    # mark the flags
    for i, arr in enumerate(numArr):
        for x,y in arr:
            undisc_arr = check_if_can_mark_flags(x, y, i + 1, tileArr)
            # print(undisc_arr)
            if len(undisc_arr) == i + 1:
                for xArr, yArr in undisc_arr:
                    if not tileArr[xArr, yArr].flag and tileArr[xArr, yArr].num != "•":
                        py.click(baseY + 15 + yArr * 31 + (yArr / 4), baseX + 15 + 31 * xArr + (xArr / 4), button='right')
                        tileArr[xArr, yArr].flag = True
                        tileArr[xArr, yArr].num = "•"
                        flags_used += 1
                        # clicks += 1

    # use the flags
    for i, arr in enumerate(numArr):
        for x,y in arr:
            num_flags = check_flags_around(x, y, tileArr)
            if num_flags > (i + 1):
                print("BIG PROBLEM!!! At ", x, y)
                py.click(baseY + 15 + y * 31 + (y / 4), baseX + 15 + 31 * x + (x / 4), button='right')
                printArray(tileArr)
                exit()
            elif num_flags == (i + 1):
                # print(x, y, "can clear")
                clear_around_you(x, y, tileArr, add_tiles_arr)
        
    # add any tiles just discovered to arrays
    for x,y in add_tiles_arr:
        r,g,b = pixels[17 + y * 31 + (y / 4), 17 + 31 * x + (x / 4)]
        # print("Position: [" + str(x) + "," + str(y) + "]", "(", r, g, b, ")")
        tempnum = what_num(r, g, b, x, y, numArr)
        if tile.num != "•":
            tile.num = tempnum
    
    count += 1


for x in range(hard_row):
    for y in range(hard_col):
        if not tileArr[x,y].disc and not tileArr[x,y].flag:
            py.click(baseY + 15 + y * 31 + (y / 4), baseX + 15 + 31 * x + (x / 4))

print("Complete!!", flags_used, "flags used and in", count, "iterations.")
time.sleep(0.2)
im2 = ImageGrab.grab(bbox = (680, 398, 1241, 848)) 
im2.save('finished.jpg')
printArray(tileArr)