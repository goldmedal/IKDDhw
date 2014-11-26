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
noEndPoint = list()
deadEnd = list()

# check dead end point

for item in odict :
    if odict[item] :
        noEndPoint.append(odict[item])
    else :
        deadEnd.append(item)

# check the point link to dead end and remove the dead end point

noLinkToEnd = list()
linkToEnd = list()

for endPoint in deadEnd :
    i = 0
    for item in noEndPoint:
        i += 1
        if item.count(endPoint) == 0 :
            noLinkToEnd.append(item)
        else:
            linkToEnd.append(i)

# remote the point link to dead end

finalList = list()

for link2end in linkToEnd :
    i = 0
    for item in noLinkToEnd :
        i += 1
        newItem = list()   
        for value in item :
            if value != link2end :
                 newItem.append(value)
        finalList.append(newItem)         

# count the rate 
        
matrix = list()
key = 0
length = len(finalList)
exist = list()

# re number 

for item in finalList : 
    for value in item:
        if exist.count(value) == 0 :
            exist.append(value)
exist.sort()

for item in finalList :
    for value in item:
        i = item.index(value)
        item[i] = exist.index(value)       

# generate the matrix
  
for point in finalList :
    pointLen = len(point)
    item = list()
    i=0
    while i < length:
       item.append(0)
       i += 1
    for value in point :
        item[value] = 1/pointLen
        
    matrix.append(item)
    key += 1

#





            








