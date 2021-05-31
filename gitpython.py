import subprocess
import os
import blocktree
import re
import codecs

tail_array = []
tail_dic ={}
#目前這樣沒有做切割所以每執行一次就會把所有的log資訊當作metadata存進去，一次會比一次多一筆
def get_git_log_hash():
    x = codecs.decode(subprocess.check_output(['git', 'log', '-p','-1']))
    y = x.split('\n')
    regular_y = []

    for i in y:
        if i == '':
            continue
        else:
            if 'commit' in i:
                regular_y.append(i)
                regular_y.append('\n')
            if 'Merge' in i:
                regular_y.append(i)
                regular_y.append('\n')
            if 'Author' in i:
                regular_y.append(i)
                regular_y.append('\n')
            if 'Date' in i:
                regular_y.append(i)
                regular_y.append('\n')
            if '+' == i[0]:
                regular_y.append(i)
                regular_y.append('\n')
            if '-' == i[0]:
                regular_y.append(i)
                regular_y.append('\n')
            if ' ' == i[0]:
                regular_y.append(i)
                regular_y.append('\n')
    result =''.join(regular_y)
    return result


def get_git_rebase_log(count):
    x = codecs.decode(subprocess.check_output(['git', 'log', '-p', str(count)]))
    y = x.split('\n')
    regular_y = []
    for i in y:
        if i == '':
            continue
        else:
            if 'commit' in i:
                regular_y.append(i)
                regular_y.append('\n')
            if 'Author' in i:
                regular_y.append(i)
                regular_y.append('\n')
            if 'Date' in i:
                regular_y.append(i)
                regular_y.append('\n')
            if '+' == i[0]:
                regular_y.append(i)
                regular_y.append('\n')
            if '-' == i[0]:
                regular_y.append(i)
                regular_y.append('\n')
            if ' ' == i[0]:
                regular_y.append(i)
                regular_y.append('\n')
    temp=[]
    res=[]
    for i in range(len(regular_y) - 1):
        temp.append(regular_y[i])

        if 'commit' in regular_y[i+1] or len(regular_y)-1 == i+1:
            res.append(temp)
            temp=[]
    res[len(res)-1].append(regular_y[len(regular_y)-1])
    res.reverse()
    res_str = [",".join(x) for x in res]    
    return res

def get_rebase_count(branchname):

    x = codecs.decode(subprocess.check_output(['git', 'rebase', branchname]))
    y = x.split('\n')

    count = 0
    for i in y:
        if 'Applying' in i:
            count -=1
    return get_git_rebase_log(count)
'''
def get_git_log_oneline():
    x = codecs.decode(subprocess.check_output(['git', 'log', '--oneline']))
    y = x.split('\n')
    return y
def main():    
    log_list = get_git_log_oneline()
    print(log_list)
    #new_blockchain.AddBlock(log_list)
    #log_list = get_rebase_count(master)
    #for i in range(len(log_list)):
    #    x = ''.join(log_list[i])
    #    new_blockchain.AddBlock(x)
    #new_blockchain.listprint(new_blockchain.tail)
 


if __name__ == '__main__':
    main()
'''