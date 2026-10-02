import os, sys
DEV = r"D:\DayZ-Server_AI-20260907-MultiMap\japan_dev"
sys.path.insert(0, os.path.join(DEV, "spikes", "SH1"))
import terrain_sh1 as T
x0, x1, z0, z1, st = [float(a) for a in sys.argv[1:6]]
xs = []
x = x0
while x <= x1 + 1e-6:
    xs.append(x); x += st
print("z/x " + " ".join("%5d" % x for x in xs))
z = z1
while z >= z0 - 1e-6:
    print("%4d " % z + " ".join("%5.1f" % T.ground(x, z) for x in xs))
    z -= st
print("trees in box:", sum(1 for t in T.trees() if x0 <= float(t[0]) <= x1 and z0 <= float(t[1]) <= z1))
