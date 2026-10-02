import sys,numpy as np
sys.path.insert(0,r"D:\DayZ-Server_AI-20260907-MultiMap\japan_dev\spikes\FX7")
import entrycheck as E
rows,_=E.placements()
r=[r for r in rows if sys.argv[1] in r["stem"]][0]
x0,x1,z0,z1=map(float,sys.argv[2:6])
WX,WZ,tg,h,D=E.walkmap((x0,x1,z0,z1),rows)
seat=r["pos"][1]
for j in range(h.shape[1]-1,-1,-1):
    print("%.1f "%WZ[0,j]+" ".join(("###" if D[i,j] else "%3d"%round((h[i,j]-seat)*100)) for i in range(h.shape[0])))
print("x from",x0)
