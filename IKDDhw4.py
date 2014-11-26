
import sys
import os
import re
import collections
import numpy as np
import operator

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
        item[value] = 1.0/float(pointLen)
        
    matrix.append(item)
    key += 1

# matrix count

pageNum = len(matrix)
pagelist = list()
i = 0
while i < pageNum:
    pagelist.append(1.0/float(pageNum))
    i += 1

a = np.array(matrix)
b = np.array(pagelist)
A = float(b[1])
B = 10.0

while B-A > 0.0001 :
    A = B
    b = np.dot(b,a)
    B = b[1]

# count the link end point
# genrate the page rank

pageRank = dict()
i = 0

for value in b :
    pageRank[exist[i]] = value
    i += 1

for item in linkToEnd :
    rate = 0
    for key, value in grap.items():
        if value.count(item) > 0 :
            rate += (1.0 / float(pageNum) * pageRank[key])
    pageRank[item] = rate

for item in deadEnd :
    rate = 0
    for key, value in grap.items():
        if value.count(item) > 0 :
            rate += (pageRank[key])
    pageRank[item] = rate

# search

query = sys.argv[1]
page = dict()

for root, dirs, files in os.walk("webpage_data_5"):
    for name in files:
        f = open(root+"/"+name)
        content = f.read()
        if content.find(query) != -1 :
       
            txtfind = name.find('.txt')
            pageNum = int(name[txtfind-1])
            page[name] = pageRank[pageNum]

# output format

sorted_x = sorted(page.items(), key= operator.itemgetter(1))

print " "
print "Rank     | Filename"

i = len(sorted_x) - 1
j = 1
while i >=0 :
    print "%-9s| %s" % (j, sorted_x[i][0])
    i -= 1
    j += 1


