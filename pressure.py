import matplotlib.pyplot as plt
import sys
import struct
import math

y=[]
t=[]
l=[]
if(len(sys.argv)==2):
    fname=sys.argv[1]

f=open(fname, 'r')
i=0.0;
for r in f.readlines():
    x=r.split(",")
    print(x)
    if(len(x)==2):
        y.append(float(x[0]))
        t0=x[1][:-1]
        t.append(float(t0)*0.001)
        l.append(i);
        i=i+1


def extract_nth_sequence_from_end(N, fn):
    i=len(l)-1
    index = 0
    lastindex = i+1
    while(N):
        while(i>1):   
           #print(t[i], t[i-1])
           if((t[i]-t[i-1])<0):
               index = i   
               i=i-1
               break 
           i=i-1
        N=N-1
        if(N>0):
           lastindex = index
    f=open(fn, 'wb')
    Ts=t[index]
    s=b""
    for i in range(index, lastindex):
        s=s+struct.pack("ff", t[i]-Ts, y[i])
    f.write(s) 
    f.close()
    return (index, lastindex)



(a,b) = extract_nth_sequence_from_end(1, 'p2.bin')
print(a,b)
(a,b) = extract_nth_sequence_from_end(2, 'p1.bin')
print(a,b)

fig, ax1 = plt.subplots()
ax1.plot(l, y, 'b-', label='Downstream Pressure')
ax1.plot(l, t, 'r-', label='index')

ax1.set_xlabel('Approx Time (s)')
ax1.set_ylabel('PSI')
plt.title('Pump #1 Downstream RT Pressure')
plt.show()
