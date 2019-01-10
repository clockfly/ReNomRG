#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:10:36 2018

@author: mikeogawa
"""

"""
this function takes the msgstr and insert below msgid
because python cannot overwrite files flexibly, we output the merged file as writefile

write file: which file to save as
readfile1: msgid file
readfile2: msgstr file

"""
def jap2eng(writefile,readfile1,readfile2):
    f=open(readfile2,"r")
    
    msgid=False
    word_list=""
    word_list1=""
    word_list2=""
    end_list=[]
    i=0
    
    for line in f:
        if msgid==False:  ##if msgid isnt found
            if 'msgid' in line:
                word_list1=line.replace('msgid','msgstr')
                msgid=True ##msgid is found
            else:
                pass
    
        else: ## if msgid is found, go to else
            if 'msgstr' in line:  ##if msgstr is found, then stop and restart, msgfalse
                msgid=False
                
                if word_list2:
                    word_list=word_list1+'"'+word_list2+'"\n'
                else:
                    word_list=word_list1
                
                end_list.append(word_list)
                word_list=""
                word_list1=""
                word_list2=""
                
            else: ##keep adding new strings until mstg is found
                line=str(line).strip('\n').strip('"')
                word_list2+=line

    ##iterator
    print(end_list)
    f.close
    out_list=iter(end_list)
    
    ##making new file
    read=open(readfile1,"r")
    write=open(writefile,"w")
    
    for line in read:
        if len(end_list)<=i:
            break
        
        if 'msgstr' in line:
            write.writelines(next(out_list)) ##overwrite existing mgstr blank with new saved ones
            i+=1
        else:
            write.writelines(line) ##if nothing then continue
    
    read.close
    write.close

#jap2eng("notebook3.po","notebook2.po","notebook-ja.po")
        