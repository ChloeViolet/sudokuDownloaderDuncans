# Author:        Christopher J. Kelly
# Creation Date: 6/7/2019
# Filename:      sudoku.py

import os
import sys
import urllib3
from bs4 import BeautifulSoup

url = "http://nine.websudoku.com?level="

# name:   get_numbers
# desc:   retrieves puzzle information from the webpage
# return: 0 on failure, list of cheat and mask on success
def get_numbers():
    http = urllib3.PoolManager()
    try:
        page = http.request("GET", url)
    except:
        print("Can't connect to website")
        return 0

    soup = BeautifulSoup(page.data, "lxml")
    cheat = soup.findAll(attrs={"name" : "cheat"})
    mask = soup.findAll(id="editmask")
    if cheat and mask:
        cheat = cheat[0]["value"] # all numbers in puzzle
        mask = mask[0]["value"] # which numbers are visible
    else:
        return 0

    return [cheat, mask]

    
# name:   file_exists
# param:  filename - name of file to check
# desc:   determines if the file already exists and presents options to user
# return: new filename to write to | "o" to overwrite | "c" to cancel
def file_exists(filename):
    print("File already exists. (O)verwrite, (N)ew Name, or (C)ancel")
    option = input()    
    if option.lower() == "n":
        print("Input new filename:")
        #newName = input()
        return input()
    elif option.lower() == "o":
        return "o"
    else:
        return "c"
   
   
# name:   write_file
# param:  filename - name of file to create
#         nums - list of cheat and mask
# desc:   writes puzzle # to file if mask is 0, else writes 0
# return: 0 on fail, 1 on success
def write_file(filename, nums):
    cheat = nums[0]
    mask = nums[1]    
    try:
        file = open(filename, "w")
    except:
        return 0

    file.write("*** SuDoku Solver save file format - do not edit this file by hand\n")
    file.write(filename)
    file.write(" - Difficulty ")
    file.write(url[-1])
    file.write("\n")

    for i in range(0, len(cheat)): # 81
        if mask[i] == "0":
            file.write(cheat[i])
        else:
            file.write("0")
        if (i+1) % 9 == 0 and i > 0: # every 9 numbers
            file.write("\n")

    file.write("\n00000000000000000000000000\n")
    file.close()
    return 1

    
# --------------------------------------------------------------------
# @main  
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ", sys.argv[0], "<Output File> [<Difficulty (1-4)]")
        sys.exit(0)
    if len(sys.argv) == 2: # default difficulty
        print("Retrieving Puzzle of Difficulty Level 1")
        url += "1"
    else:
        if int(sys.argv[2]) >= 1 and int(sys.argv[2]) <= 4: # given difficulty
            print("Retrieving Puzzle of Difficulty Level", sys.argv[2])
            url += sys.argv[2]
        else:
            print("Error: Difficulty level must be 1-4")
            sys.exit(0)
    
    fname = sys.argv[1]
    
    # retrieve puzzle data from website
    nums = get_numbers()
    if nums == 0:
        print("Error Retrieving Puzzle")
        sys.exit(0)

    # check if file already exists
    while os.path.isfile(fname):
        exists = file_exists(fname)
        if exists == "o":   # overwrite existing file
            print("Overwriting" , fname)
            break
        elif exists == "c": # cancel
            print("Canceling...\n")
            sys.exit(0)
        else:               # new filename
            fname = exists
    
    # write puzzle data to file
    if write_file(fname, nums) == 0:
        print("Error Opening File")
        sys.exit(0)

    print("Puzzle Successfully Created")
