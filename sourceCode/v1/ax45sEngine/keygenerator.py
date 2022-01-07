#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random,time

def rnlm():
    rn=[]
    f=True
    while f==True:
        r=random.randint(1,94)
        if rn.count(r)==0:
            rn.append(r)
        if len(rn)==94:
            f=False
    return rn
rl=[[],[]]
rll=[[],[]]
for x in range(32,127):
    rl[0].append(chr(x))

rl[1]=rnlm()
for y in range(1,95):
    for z in range(0,94):
        if y==rl[1][z]:
            rll[1].append(y)
            rll[0].append(rl[0][z])
rfn=random.randint(1,10**4)

fn="key"+str(rfn)+".ax"
f = open(fn, "a")
for a in range(0,94):
    f.write(str(rll[1][a]))
    f.write("axen")
    f.write(rll[0][a])
    if a==len(rl[0])-1:
        pass
    else:
        f.write("split")
f.close()
