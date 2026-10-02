"""FX7 contact sheet: research/production/contact_sheets/fx7_fixes.jpg.

Row 1 the checkpoint guardhouse entry: the walk-surface profile across the inspection front and the kitchen door,
before (measured by entrycheck's walk map on the W3D build, 2026-10-02) and after (re-measured on the FX7 build).
Row 2 the cargo scale: W3D before (std, _ab), FX7 after (std, _ab). Rows 3-4 the four 3c-2 rock / earth objects,
W3C2 before and FX7 after (same 3/4 view).

  python spikes/FX7/sheet_fx7.py
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
R = os.path.join(HERE, "renders")
OUT = os.path.join(DEV, "research", "production", "contact_sheets", "fx7_fixes.jpg")
CW, CH = 480, 360

# walk-surface heights over the first sample (m) every 0.2 m north from the road (z 866.6 / 867.8); the sample at
# z 868.6 fell in the 1 cm seam between the veranda boards and the kamachi beam (0.09) and is drawn at the floor
FRONT_Z = [866.6 + 0.2 * k for k in range(18)]
FRONT_BEFORE = [0.16] * 7 + [0.57, 0.70, 0.84, 0.93, 0.93, 0.93, 0.93, 0.93, 1.08, 1.08, 1.08]
FRONT_AFTER = [0.16] * 5 + [0.30, 0.43, 0.57, 0.70, 0.84, 0.93, 0.93, 0.93, 0.93, 0.93, 1.08, 1.08, 1.08]
DOOR_Z = [867.8 + 0.2 * k for k in range(7)]
DOOR_BEFORE = [0.13, 0.13, 0.13, 0.10, 0.45, 0.50, 0.50]
DOOR_AFTER = [0.14, 0.18, 0.32, 0.45, 0.51, 0.51, 0.51]


def chart(title, z, before, after):
    """A step plot drawn with PIL (no matplotlib here): before red, after blue, a 0.30 m step-up scale bar."""
    im = Image.new("RGB", (CW, CH), "white")
    d = ImageDraw.Draw(im)
    L, Rr, T_, B_ = 50, CW - 15, 40, CH - 40
    y0, y1 = -0.05, 1.15
    z0, z1 = z[0] - 0.1, z[-1] + 0.1

    def P(zz, yy):
        return L + (zz - z0) / (z1 - z0) * (Rr - L), B_ - (yy - y0) / (y1 - y0) * (B_ - T_)
    for yy in (0.0, 0.3, 0.6, 0.9):
        d.line([P(z0, yy), P(z1, yy)], fill=(225, 225, 225))
        d.text((8, P(z0, yy)[1] - 6), "%.1f m" % yy, fill=(90, 90, 90))
    for ys, col in ((before, (176, 58, 46)), (after, (31, 111, 139))):
        pts = []
        for i, (zz, yy) in enumerate(zip(z, ys)):
            a_ = zz - 0.1
            b_ = zz + 0.1
            pts += [P(a_, yy), P(b_, yy)]
        d.line(pts, fill=col, width=3)
    d.text((L, 8), title, fill=(0, 0, 0))
    d.text((L, 22), "red = before (W3D), blue = after (FX7); walk surface over the road, every 0.2 m north",
           fill=(60, 60, 60))
    xs = Rr - 30
    d.line([(xs, P(z0, 0.0)[1]), (xs, P(z0, 0.30)[1])], fill=(0, 0, 0), width=2)
    d.text((xs - 70, P(z0, 0.15)[1] - 6), "0.30 step", fill=(0, 0, 0))
    d.text((L, B_ + 8), "road (south)  ->  gravel court  ->  steps  ->  veranda / doma (north)", fill=(60, 60, 60))
    return im


def tile(path, label):
    im = Image.open(path).convert("RGB").resize((CW, CH)) if os.path.exists(path) else Image.new("RGB", (CW, CH),
                                                                                                    "white")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, CW, 18), fill=(255, 255, 255))
    d.text((6, 3), label, fill=(0, 0, 0))
    return im


def main():
    rows = [
        [chart("Guardhouse inspection front (x 757.6): the 0.41 lip from the gravel (old ramp foot)", FRONT_Z, FRONT_BEFORE,
               FRONT_AFTER),
         chart("Guardhouse kitchen door (x 751.6 / 752.7): the 0.35 lip", DOOR_Z, DOOR_BEFORE, DOOR_AFTER),
         tile(os.path.join(DEV, "spikes", "W3D", "renders", "fam_gv_bansho_sekisho.png"),
              "guardhouse shell (W3D render; FX7 adds the court steps in the furnished variant)")],
        [tile(os.path.join(R, "before_kanme_hakari.png"), "BEFORE jp_f_kanme_hakari (read as a gallows)"),
         tile(os.path.join(R, "fx7_kanme_hakari.png"), "AFTER jp_f_kanme_hakari: tripod, bale hanging, graduated beam"),
         tile(os.path.join(R, "fx7_kanme_hakari_ab.png"), "AFTER jp_f_kanme_hakari_ab: beam, weight, bale down")],
    ]
    for lab, keys in (("BEFORE", "before_"), ("AFTER", "fx7_")):
        rows.append([tile(os.path.join(R, keys + k + ".png"), "%s %s" % (lab, n)) for k, n in (
            ("ishiba", "Land_JP_Ishiba (quarry)"), ("mabu", "Land_JP_Mabu (mine adit)"))])
        rows.append([tile(os.path.join(R, keys + k + ".png"), "%s %s" % (lab, n)) for k, n in (
            ("ishibaigama", "Land_JP_Ishibai_Gama (lime kiln)"), ("noborigama", "Land_JP_Noborigama (climbing kiln)"))])
    W = 3 * CW
    sheet = Image.new("RGB", (W, CH * len(rows) + 30), "white")
    ImageDraw.Draw(sheet).text((8, 8), "FX7 fixes (2026-10-02): checkpoint entry, cargo scale, 3c-2 rock / earth masses",
                               fill=(0, 0, 0))
    for r, row in enumerate(rows):
        for c, im in enumerate(row):
            sheet.paste(im, (c * CW, 30 + r * CH))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sheet.save(OUT, quality=85)
    print("wrote", OUT, sheet.size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
