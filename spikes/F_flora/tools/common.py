"""Shared paths and helpers for the F (flora) spike tools."""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)                                   # japan_dev/spikes/F_flora
DEV = os.path.dirname(os.path.dirname(SPIKE))                   # japan_dev
DATA = os.path.join(DEV, "data", "F")                           # downloads + regenerable intermediates (git-ignored)
WORK = os.path.join(DATA, "work")                               # generated intermediates (PNG, OBJ, JSON, MLOD masters)
WORK_TEX = os.path.join(WORK, "tex")
WORK_MESH = os.path.join(WORK, "mesh")
RENDERS = os.path.join(SPIKE, "renders")
SRC = os.path.join(DEV, "src", "JP", "plants")                  # = P:\JP\plants
ADDONS = os.path.join(os.path.dirname(DEV), "@Japan", "addons")
TOOLS_BIN = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin"
IMAGE_TO_PAA = os.path.join(TOOLS_BIN, "ImageToPAA", "ImageToPAA.exe")
BINARIZE = os.path.join(TOOLS_BIN, "Binarize", "binarize.exe")
CFGCONVERT = os.path.join(TOOLS_BIN, "CfgConvert", "CfgConvert.exe")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"

# P:-relative folders (what goes inside p3ds / rvmats / config)
P_TREE = "JP\\plants\\tree"
P_BAMBOO = "JP\\plants\\bamboo"
P_ITEMS = "JP\\plants\\items"

for d in (WORK, WORK_TEX, WORK_MESH, RENDERS):
    os.makedirs(d, exist_ok=True)


def src_dir(p_rel):
    """P:-relative folder -> absolute folder under src/JP/plants."""
    assert p_rel.lower().startswith("jp\\plants")
    tail = p_rel[len("JP\\plants"):].lstrip("\\")
    d = os.path.join(SRC, *tail.split("\\")) if tail else SRC
    os.makedirs(d, exist_ok=True)
    return d


def write_text(path, text):
    """LF-only text write (binary mode, per the README rule)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.replace("\r\n", "\n").encode("ascii"))


def to_paa(png, paa):
    """ImageToPAA png -> paa. Raises if the paa did not appear."""
    if os.path.exists(paa):
        os.remove(paa)
    r = subprocess.run([IMAGE_TO_PAA, png, paa], capture_output=True, text=True, errors="replace")
    if not os.path.isfile(paa):
        raise SystemExit("ImageToPAA failed for %s:\n%s" % (png, r.stdout + r.stderr))
    return paa
