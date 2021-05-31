
import subprocess
import os

def readfile():
    with open('D:/testfile.txt', 'r') as f:
       command_list = f.read().split('\n')
    return command_list

#print(readfile())