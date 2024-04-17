import matplotlib.pyplot as plt
import sys
import struct
import math

skipGraph = True
if(len(sys.argv)>1):
    fname=sys.argv[1]
    if(len(sys.argv)==3):
        skipGraph = False
else:
    print("Usage python3 motor.py filename [ to just process] ")
    print("Usage python3 motor.py filename graph  [ to process and graph ] ")
    sys.exit(-1)

BASE=22.0

f=open(fname, 'r')
a=f.readlines()
f.close()
T=[]
T2=[]
V=[]
W=[]
F=[]
Fraw=[]
U=[]
L=[]
D=[]
S=[]
E=[]
t=0.0
upper = 0.0
lower = 0.0
lastat0=0.0
for a0 in a:
#    try:
     if(1):
        dt=1.0
        s=a0.split(' ')
        print(s)
        at0=float(s[1][1:-1])
        if(len(T2)):
            dt=at0-lastat0
        else:
            dt=0.0
        lastat0=at0

        t0=s[5].split("=")[1][:-1]
        x=s[6].split("/")
        v0=float(x[0])
        f0=float(x[2][:-1])
        y=s[7]
        t=t+(float(t0)/1000000.0)
        print(at0, t0, v0, f0) 
        T.append(t)
        #T2.append(float(t0)/1000)
        V.append(float(v0))
        F.append(float(f0)+BASE)
        Fraw.append(float(f0))
        D.append(float(v0)/(float(t0)/1000000.0))


        lower0=s[10]
        print(s[12], len(s[12]))
        upper0=s[12][:-1]
        print(upper0, lower0)
        lower0=float(lower0)
        upper0=float(upper0)
        if(upper0 > 0.0):
            upper=upper0
            lower=lower0
        upper=0.45
        L.append(lower0+BASE)
        slope = float(s[8][:-1])
        S.append(BASE+slope*1000.0)
        if(dt<100.0):
            T2.append(dt) # in ms
        else:
            T2.append(100.0)
        err = float(s[13][:-5])*150.0
        E.append((err+BASE+float(v0))*0.5)
        w = s[14][:-5]
        W.append(float(w))
        print("Lower", lower)
        #E.append(err+BASE)
    #except:
    #    print("Error !")
    #    pass

Fstd=[]
gotp=False
gotz=False
sumsq=0.0
for f in Fraw:
    if(not gotp):
        if(f>15.0):
            gotp=True
    else:
        if(not gotz):
            if(f == 0.0):
                gotz = True
    if(gotp and gotz):
        Fstd.append(f)   
        sumsq=sumsq+(f*f)

#MS=sumsq/len(Fstd)
#RMS=math.sqrt(MS)

#print("STD/RMS = %3.3f, LOWER/UPPER = %3.3f %3.3f" % (RMS, lower, upper))  
            
def extract_nth_sequence_from_end(N, fn):
    i=len(T)-1
    index = 0
    lastindex = i+1
    while(N):
        while(i>1):   
           #print(T,T2)
           if(T2[i] >=100.0):
               index = i   
               i=i-1
               break 
           i=i-1
        N=N-1
        if(N>0):
           lastindex = index-1
 
    f=open(fn, 'wb')
    Ts=T[index]
    s=b""
    print("len", len(T), len(T2),  lastindex, index)
    for i in range(index, lastindex+1):
        #print("i=", i)
        s=s+struct.pack("fff", T[i]-Ts, V[i], F[i])
    f.write(s) 
    f.close()
    return (index, lastindex)


(a,b) = extract_nth_sequence_from_end(2, 's2.bin')
print(a,b)
print(len(T), T[a], T[b-1], T2[a])


(a,b) = extract_nth_sequence_from_end(3, "s1.bin")
print(a,b)
print(len(T), T[a], T[b-1], T2[a])




if(skipGraph):
   sys.exit(0)
fig, ax1 = plt.subplots()
ax1.plot(T, V, 'b-', label='PWM')
ax1.plot(T, F,  color='magenta', label='Occlusion')
#ax1.plot(T, S,  color='cyan', label='Slope')
ax1.plot(T, W, 'y-', label='Upstream')
E2=[];
E2.append(BASE);
E2.append(BASE);
E2.append(BASE);
E2.append(BASE);
E2.append(BASE);
E2.append(BASE);
E2.append(BASE);
E2.append(BASE);
E2.append(BASE);
i=0
while(len(E2)<len(E)):
    sum=50000.0
    for k in range(9):
        if(E[i+k]<sum):
            sum=E[i+k]; 
    E2.append(sum)
    i=i+1
#ax1.plot(T, E,  color='magenta', label='Err')
ax1.plot(T, E2,  color='black', label='Err')
for a in V:
    U.append(BASE+upper)
# Adding title
plt.title('Motor Drive/Occlusion Signals')

# Adding labels
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Various')

ax2 = ax1.twinx()  
#ax2.plot(T, T2, 'ro-', label='time delay')
#ax2.plot(T, D, color="red", label='pause')
ax1.plot(T, U, color="black")
ax1.plot(T, L, color="black")
ax1.legend()
#ax2.legend()

f=open('data.bin','wb')
d=[]
for i in range(len(T)):
    e=struct.pack("ff", T[i], V[i])
    f.write(e)
   
f.close() 
# Display the plot
plt.show()
