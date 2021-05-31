import os
import sys
import time
import hashlib
import ctypes
import gitpython
import re
import readtxt



tail_array = []
tail_dic ={}

class Branch:
    commandlist = list()
    branchlist = ['dev', 'dev-bug', 'dev-feat', 'dev-junk', 'feature', 'feature-bug', 'feature-feat', 
              'feature-junk', 'release-bug', 'release-feat', 'release-junk', 'bugfix-release', 
              'bugfix-master', 'master-feat', 'master-junk']
    checkoutlist =['master']


class Block:

    def __init__(self, index, timestamp, data, prevblockhash, hash_value):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prevblockhash = prevblockhash
        self.hash = hash_value
        self.pre = None
        self.mergepre = None
        self.rebasepre = None
       
    def SetHash(self):
        self.timestamp = str(self.timestamp)
        self.index = str(self.index)
        payload = self.index + self.timestamp + self.data + self.prevblockhash
        s = hashlib.sha256()
        s.update(payload.encode())
        self.hash = str(s.hexdigest())


class Blockchain:
    def __init__(self, block):
        self.blocks = block
        self.tail = None
        self.current = None
        self.branchname = 'master'
    def AddBlock(self, data):
        if len(tail_dic) > 1:             
            prevblock = self.tail
            new_block = Blockchain.CreateBlock(int(prevblock.index)+1, data, prevblock.hash)
            self.blocks.append(new_block)
            new_block.pre = self.tail
            self.tail = new_block  
            self.current = id(new_block)
            tail_dic[self.branchname] = self.current
        else :
            prevblock = self.blocks[len(self.blocks) - 1]
            new_block = Blockchain.CreateBlock(int(prevblock.index)+1, data, prevblock.hash)
            self.blocks.append(new_block)
            new_block.pre = prevblock
            self.tail = new_block
            self.current = id(new_block)
            tail_dic[self.branchname] = self.current


    def AddBlockpre(self, branchname):

        prevblock = self.tail
        new_block = Blockchain.CreateBlock(int(prevblock.index)+1, data, prevblock.hash)
        self.blocks.append(new_block)
        new_tail = self.tail
        new_block.pre = prevblock
        self.tail = new_block
        self.current = id(new_block)
        self.branchname = branchname
        Blockchain.addbranchname(self, branchname)


    def selecttail(self, select):
        address = tail_dic[select]
        get_value=ctypes.cast(address, ctypes.py_object).value        
        self.current = get_value
        self.tail = get_value
        self.branchname = select
        return self.current


    def AddmergeBlock(self, data, mergename):
        currentblock = self.tail                                     
        new_block = Blockchain.CreateBlock(int(currentblock.index)+1, data, currentblock.hash)
        self.blocks.append(new_block)
        new_block.pre = currentblock
        self.tail = new_block
        self.current = id(new_block)
        tail_dic[self.branchname] = self.current      
        address = tail_dic[mergename]
        get_value=ctypes.cast(address, ctypes.py_object).value 
        new_block.mergepre = get_value


    def AddresetBlock(self, headcount):
        currentblock = self.tail
        data = 'reset block'
        for i in range(int(headcount)):
            currentblock = currentblock.pre
        new_block = Blockchain.CreateBlock(int(currentblock.index)+1, data, currentblock.hash)
        self.blocks.append(new_block)
        new_block.pre = currentblock
        self.tail = new_block
        self.current = id(new_block)
        tail_dic[self.branchname] = self.current


    def AddrebaseBlock(self,rebasename):
        address = tail_dic[rebasename]
        get_value=ctypes.cast(address, ctypes.py_object).value 
        currentblock = self.tail 
        data = 'rebase block'
        new_block = Blockchain.CreateBlock(int(get_value.index)+1, data, get_value.hash)
        self.blocks.append(new_block)
        new_block.pre = get_value
        new_block.rebasepre = currentblock
        self.tail = new_block
        self.current = id(new_block)
        tail_dic[self.branchname] = self.current

    def CreateBlock(index, data, prevblockhash):
        b = Block(index, time.time(), data, prevblockhash, '')
        b.SetHash()
        return b


    def CreateGenesisBlock():
        genesisblcok = Blockchain.CreateBlock(0, "Genesis Block", '')
        genesisid = id(Blockchain.CreateBlock(0, "Genesis Block", ''))
        tail_dic['master'] = genesisid
        tail = genesisblcok
        return Blockchain.CreateBlock(0, "Genesis Block", '')
    
    def CreateBlockchain():
        return Blockchain([Blockchain.CreateGenesisBlock()])


    def listprint(self, blocks):
        print('Branch:',self.branchname)
        while(blocks is not None):
            print("PrevHash:",blocks.prevblockhash),
            print("Data:",blocks.data.encode("utf8").decode("cp950", "ignore")),
            print("Hash:",blocks.hash),
            print('-'*65)
            if blocks.mergepre != None:
                blocks = blocks.mergepre
            else:
                blocks = blocks.pre


    def addbranchname(self, branchname):
        tail_dic[branchname] = self.current
        print ("Branch:",tail_dic.keys())



def Help():
    print("There are 5 operations:")
    print("add for adding a new Block")
    print("log for printing the Blockchain")
    print("branch for branch")
    print("checkout for checkout branch")
    print("exit for exiting")

def main():
    print("Enter h for help")
    Branch.commandlist = readtxt.readfile()
    new_blockchain = Blockchain.CreateBlockchain()
    for item in Branch.commandlist:
        if 'git rebase' in item:
               branchname=item.split(' ')
               new_blockchain.AddrebaseBlock(branchname[2])
               log_list = gitpython.get_rebase_count(branchname[2])
               for i in range(len(log_list)):
                   x = ''.join(log_list[i])
                   new_blockchain.AddBlock(x)
        else:
            os.system(item)
            if 'git commit' in item:
                   log_list = gitpython.get_git_log_hash()
                   new_blockchain.AddBlock(log_list)
            if 'git branch' in item:
                   branchname=item.split(' ')
                   new_blockchain.addbranchname(branchname[2])
            if 'git checkout' in item:
                   branchname=item.split(' ')
                   new_blockchain.selecttail(branchname[2])
            if 'git merge' in item:
                   branchname=item.split(' ')
                   data = gitpython.get_git_log_hash()
                   new_blockchain.AddmergeBlock(data, branchname[2])
            if 'git revert' in item:
                   log_list = gitpython.get_git_log_hash()
                   new_blockchain.AddBlock(log_list)
            if 'git reset' in item:
                   ret = re.findall(r'(\d)',item)
                   print(ret[0])
                   new_blockchain.AddresetBlock(int(ret[0]))
    
    while True:
        op = input("Enter your command: ")
        if op == 'help':
            Help()
        elif op == 'add':
            data = input("Enter your data: ")
            new_blockchain.AddBlock(data)
            
        elif op == '2':
            for b in new_blockchain.blocks:
                print("Index: {:s}".format(b.index))
                print("PrevHash: {:s}".format(b.prevblockhash))
                print("Data: {:s}".format(b.data))
                print("Hash: {:s}".format(b.hash))
                print("tail_id: ",id(b))
                print('')
        elif op == 'exit':
            break
        elif op == 'branch':
            branchname = input("Create new branch name: ")
            new_blockchain.addbranchname(branchname)
        elif op == 'log':
            new_blockchain.listprint(new_blockchain.tail)
        elif op == 'checkout':
            print ("Branch:",tail_dic.keys()) 
            select = input('select your branch name:')
            new_blockchain.selecttail(select)
        elif op == 'merge':
            mergename = input("Merge branch name: ")
            data = 'merge block'
            new_blockchain.AddmergeBlock(data,mergename)
        elif op == 'rebase':
            rebasename = input("Rebase branch name: ")
            new_blockchain.AddrebaseBlock(rebasename)
        elif op == 'revert':
            data = 'revert block'
            new_blockchain.AddBlock(data)
        elif op == 'reset':
            rebasename = input("Reset number: ")
            new_blockchain.AddresetBlock(rebasename)
        else:
            print("Please Enter help, add, branch, checkout, log, reset, revert, merge, exit")

if __name__ == '__main__':
    main()

