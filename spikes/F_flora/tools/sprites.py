"""sprites.py - read an atlas PNG and describe each 2x2 cell's sprite: its opaque UV bounding box and anchor, so
cards can be cropped to what is actually drawn (less overdraw) and positioned by the twig base."""
import os

import numpy as np
from PIL import Image

from common import WORK_TEX


class SpriteInfo:
    def __init__(self, cell, bbox_uv, anchor_uv, cell_metres):
        self.cell = cell
        self.u0, self.v0, self.u1, self.v1 = bbox_uv
        self.au, self.av = anchor_uv
        self.m_per_uv = cell_metres / 0.5          # a cell is 0.5 UV wide and `cell_metres` wide in the world

    def size_m(self):
        return (self.u1 - self.u0) * self.m_per_uv, (self.v1 - self.v0) * self.m_per_uv

    def corners_local(self, scale=1.0):
        """Card corners in sprite-local metres, anchor at (0, 0): x right (= +u), y up (= -v).
        Returns [(x, y, u, v)] for the four corners in order TL, TR, BR, BL."""
        k = self.m_per_uv * scale
        out = []
        for u, v in ((self.u0, self.v0), (self.u1, self.v0), (self.u1, self.v1), (self.u0, self.v1)):
            out.append(((u - self.au) * k, (self.av - v) * k, u, v))
        return out


def load_atlas(name, anchors, cell_metres, pad_px=6):
    """anchors: 4 anchor points (u, v) in atlas UV, one per cell (cells: 0 TL, 1 TR, 2 BL, 3 BR)."""
    im = Image.open(os.path.join(WORK_TEX, name + ".png"))
    a = np.asarray(im)[..., 3]
    h, w = a.shape
    infos = []
    for c in range(4):
        x0, y0 = (c % 2) * w // 2, (c // 2) * h // 2
        sub = a[y0:y0 + h // 2, x0:x0 + w // 2] > 40
        ys, xs = np.nonzero(sub)
        bx0, bx1 = max(0, xs.min() - pad_px) + x0, min(w // 2, xs.max() + 1 + pad_px) + x0
        by0, by1 = max(0, ys.min() - pad_px) + y0, min(h // 2, ys.max() + 1 + pad_px) + y0
        infos.append(SpriteInfo(c, (bx0 / w, by0 / h, bx1 / w, by1 / h), anchors[c], cell_metres))
    return infos
