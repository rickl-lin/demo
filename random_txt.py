
import random
import string
import os
import blocktree
from random import choice
name =[]
checkname = []
name= blocktree.Branch.branchlist
checkname = blocktree.Branch.checkoutlist


num = 1
add_number = 0
while num < 20:
    content = ''.join(random.sample(['0','1','2','3','4','5','6','7','8','9','z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'],15))
    filename = random.randint(1,100)
    txt= 'echo '+ str(content)  + " >> " + 'file'+ str(filename)+".txt" + "\n"

    with open("testfile.txt","a") as f:
        f.write(txt)
    num +=1
    
    if num % 3 == 0:
        add_number += 1
        txt = "git add ." + "\n"
        with open("testfile.txt","a") as f:
            f.write(txt)
        txt = "git commit -m " + '"' + str(add_number) +" upload" + '"' + "\n"
        with open("testfile.txt","a") as f:
            f.write(txt)
        currentname = choice(name)
        txt = "git branch " + currentname + "\n"
        checkname.append(currentname) 
        with open("testfile.txt","a") as f:
            f.write(txt)
        num +=1

    if num % 13 == 0:
        add_number += 1
        txt = "git add ." + "\n"
        with open("testfile.txt","a") as f:
            f.write(txt)
        txt = "git commit -m " + '"' + str(add_number) +" upload" + '"' + "\n"
        with open("testfile.txt","a") as f:
            f.write(txt)
        txt = "git checkout " + choice(checkname) + "\n"
        with open("testfile.txt","a") as f:
            f.write(txt)
        num +=1
         

