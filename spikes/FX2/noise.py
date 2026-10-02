"""FX2: binarize byte-noise -> HEAD. The prop builders' binarize rewrites every ODOL under src/JP/<area> with float
noise in thousands of bytes, so noise cannot be told from a change by a diff count. FX2 keeps the ODOLs of the models
it really changed (KEEP regexes: the p3d stems FX2 rebuilt with new geometry) and restores every other modified
tracked *.p3d under the given folders to HEAD (README rule 3; PRODUCTION_PLAN pitfall).

  python spikes/FX2/noise.py [--dry] <folder> ...
"""
import re
import subprocess
import sys

KEEP = [
    # B3b / W2 site props (jp_site)
    r"jp_s_stone_jizo_", r"jp_s_jizo_hut_", r"jp_s_stele_(koshin|relief_panel|ab_tipped)\.",
    r"jp_s_grave_stones_(boat_halo|boat_halo_child|jizo_child|ab_boat_halo_sunk)\.",
    r"jp_s_torii_wood_.*rope", r"jp_s_torii_stone_.*rope", r"jp_s_shimenawa_len_",
    # W2F furniture (jp_furniture)
    r"jp_f_dais_", r"jp_f_kagura_masks\.", r"jp_f_waniguchi\.", r"jp_f_suzu_rope", r"jp_f_bonsho_",
    r"jp_f_ema_rail\.", r"jp_f_saisen_bako_", r"jp_f_shimenawa_hang\.",
]


def main(argv):
    dry = "--dry" in argv
    dirs = [a for a in argv if not a.startswith("--")]
    out = subprocess.run(["git", "status", "--porcelain", "--"] + dirs, capture_output=True, text=True).stdout
    keep, noise = [], []
    for ln in out.splitlines():
        if not ln.startswith(" M") or not ln.endswith(".p3d"):
            continue
        f = ln[3:].strip()
        (keep if any(re.search(k, f.rsplit("/", 1)[-1]) for k in KEEP) else noise).append(f)
    for f in keep:
        print("KEEP  " + f)
    print("kept %d changed ODOLs; noise: %d files%s" % (len(keep), len(noise), " (dry run)" if dry else " restored"))
    if noise and not dry:
        for i in range(0, len(noise), 100):
            subprocess.run(["git", "checkout", "--"] + noise[i:i + 100], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
