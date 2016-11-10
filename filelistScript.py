#!/usr/bin/python
import pdb
f1 = open('c3d_ucf101_my_test.txt','r+')
pdb.set_trace()
for line in f1:
   #pdb.set_trace()
    li = line.replace('/media/TB/Videos','/scratch/xf362')
    print li
    f2 = open('c3d_ucf101_my_test1.txt','a+')
    f2.write(li)
#f.readline()
f1.close()
f2.close()
