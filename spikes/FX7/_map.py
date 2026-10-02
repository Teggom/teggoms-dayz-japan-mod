import sys,numpy as np
sys.path.insert(0,r"D:\DayZ-Server_AI-20260907-MultiMap\japan_dev\spikes\FX7")
import entrycheck as E
rows,_=E.placements()
r=[r for r in rows if sys.argv[1] in r["stem"]][0]
b=r["wbb"];m=1.0
WX,WZ,tg,h,D=E.walkmap((b[0]-m,b[1]+m,b[2]-m,b[3]+m),rows)
seat=r["pos"][1]
print(r["stem"],"seat",round(seat,2),"yaw",r["yaw"],"x",round(b[0]-m,1),"z top",round(b[3]+m,1))
ch="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for j in range(h.shape[1]-1,-1,-2):
    line=""
    for i in range(0,h.shape[0],2):
        if D[i,j]: line+="#"
        else:
            v=h[i,j]-seat
            line+= "." if v<-0.02 else ch[min(35,int(round(v*20)))]
    print(line)
