import os


regx_package="org/apache/logging/log4j"
result=set()
f = open('c:/1.txt','r+')
for e in f:
    sub = (e.split(' ')[-1])
    if(sub.find(regx_package)!=-1):
        result.add(sub[0:sub.rfind("/")])
f.close()     
fw = open('c:/package.txt','w+')
for e in result:
    if(e.find(regx_package)>0):
        continue
    e=e.replace("/",".")
    print(e)
    fw.write(" "+e+','+'\r')
fw.flush()
fw.close()

