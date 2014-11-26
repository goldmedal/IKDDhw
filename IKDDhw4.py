import sys
import os
import re
import collections

# parse the page number

grap = dict()

def findLink( file, fileNum ):

    for line in file:
        httpfind = line.find('http')  # confirm existing hyperlink
        if httpfind != -1 :
            txtfind = line.find('.txt')
            pageNum = int(line[txtfind-1])
            grap[fileNum].append(pageNum)
    grap[fileNum].sort()
    return

for root, dirs, files in os.walk("webpage_data_5"):
    for name in files:
        numfind = name.find('.txt') - 1
        num = int(name[numfind])
        file = open(root+"/"+name,'r')
        grap[num] = list()
        findLink(file, num)

odict = collections.OrderedDict(sorted(grap.items()))







