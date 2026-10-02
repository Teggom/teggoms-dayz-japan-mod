#!/usr/bin/env python3
"""CA1 self-test of tools/assemble_config.py + tools/cfgdiff.py on a COPY of the furniture fragments (scratch dir;
the real src tree is never touched):
  1. the copy assembles to the same classes as src/JP/furniture/config.cpp (cfgdiff 0)
  2. a duplicate class with the SAME body in a second fragment is kept once
  3. a duplicate class with a DIFFERENT body fails loudly (AssembleError) and writes nothing
  4. cfgdiff reports a dropped class and a changed body (it is not blind)
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "tools"))
import assemble_config as ASM  # noqa: E402
import cfgdiff  # noqa: E402

TMP = os.path.join(HERE, "_build", "selftest")
shutil.rmtree(TMP, ignore_errors=True)
os.makedirs(os.path.join(TMP, "_frags"))
real = ASM.src_dir("jp_furniture")
for f in os.listdir(os.path.join(real, "_frags")):
    shutil.copyfile(os.path.join(real, "_frags", f), os.path.join(TMP, "_frags", f))
ASM.src_dir = lambda pbo: TMP
ok = True

r = ASM.assemble("jp_furniture", verbose=False)
d = cfgdiff.diff(cfgdiff.load(os.path.join(real, "config.cpp")), cfgdiff.load(os.path.join(TMP, "config.cpp")))
print("1 copy assembles to the real config: %d classes, %d differences" % (r["classes"], len(d)))
ok &= not d

b3a = json.load(open(os.path.join(TMP, "_frags", "B3a.json"), encoding="utf-8"))
same = dict(b3a, builder="ZZsame", order=99, classes=b3a["classes"][:2], models=b3a["models"][:2])
open(os.path.join(TMP, "_frags", "ZZsame.json"), "wb").write(json.dumps(same).encode("utf-8"))
r2 = ASM.assemble("jp_furniture", verbose=False)
print("2 same-body duplicate kept once: %d classes (was %d)" % (r2["classes"], r["classes"]))
ok &= r2["classes"] == r["classes"]

before = open(os.path.join(TMP, "config.cpp"), "rb").read()
bad = dict(same, builder="ZZbad")
bad["classes"] = [dict(b3a["classes"][0], body=b3a["classes"][0]["body"] + ["scope=2;"])]
open(os.path.join(TMP, "_frags", "ZZbad.json"), "wb").write(json.dumps(bad).encode("utf-8"))
try:
    ASM.assemble("jp_furniture", verbose=False)
    print("3 FAIL: a conflicting duplicate was accepted")
    ok = False
except ASM.AssembleError as e:
    unchanged = open(os.path.join(TMP, "config.cpp"), "rb").read() == before
    print("3 conflicting duplicate -> AssembleError (%s...), config.cpp untouched: %s" % (str(e)[:110], unchanged))
    ok &= unchanged
os.remove(os.path.join(TMP, "_frags", "ZZbad.json"))
os.remove(os.path.join(TMP, "_frags", "ZZsame.json"))

t = open(os.path.join(TMP, "config.cpp"), "rb").read().decode("utf-8")
i = t.index("\tclass StaticObj_JP_F_")
j = t.index("};\n", i) + 3
t2 = t[:i] + t[j:]                                       # drop the first class
t2 = t2.replace("scope=1;", "scope=2;", 1)                 # change one body
d = cfgdiff.diff(cfgdiff.parse(t), cfgdiff.parse(t2))
print("4 cfgdiff on a dropped class + a changed body: %d differences: %s" % (len(d), d))
ok &= len(d) == 2
print("SELFTEST", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
