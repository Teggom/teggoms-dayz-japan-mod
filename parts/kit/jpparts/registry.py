"""Every part variant the kit builds, in the lead's priority order (walls/frame, openings, foundations, roofs, rest).
(part id, variant, builder(variant) -> Part)."""
from . import frame, walls

ALL = []


def reg(pid, variants, fn):
    for v in variants:
        ALL.append((pid, v, fn))


# ---- 2. walls, framing, posts
reg("jp_p_frame_post", ["_planed", "_adzed"], frame.part_post)
reg("jp_p_frame_beam", ["_sawn", "_log"], frame.part_beam)
reg("jp_p_wall_shinkabe", ["_arakabe", "_nakanuri", "_shikkui", "_kokabe_ranma"], walls.part_shinkabe)
reg("jp_p_wall_okabe", ["_kura", "_nuriya"], walls.part_okabe)
reg("jp_p_wall_board_vertical", ["_battened", "_plain"], walls.part_board_vertical)
reg("jp_p_wall_koshiita", ["_h060", "_h090"], walls.part_koshiita)
reg("jp_p_wall_gable", ["_thatch", "_tile", "_board", "_kura"], walls.part_gable)
reg("jp_p_wall_shitami", ["_house", "_kura"], walls.part_shitami)
reg("jp_p_wall_namako", ["_imo", "_shihan"], walls.part_namako)
reg("jp_p_wall_udatsu", ["_sode", "_hon"], walls.part_udatsu)
reg("jp_p_frame_dashigeta", ["_std", "_upper_front"], frame.part_dashigeta)

from . import openings, found
openings.register(reg)
found.register(reg)
from . import roofparts
roofparts.register(reg)
# ---- B2 (2026-09-29): missing parts, wave 1
from . import koyagumi
koyagumi.register(reg)
from . import party
party.register(reg)
from . import stall
stall.register(reg)
from . import stair
stair.register(reg)
from . import halfdoor
halfdoor.register(reg)
from . import pits
pits.register(reg)
# ---- W2P1 (2026-10-01): village-grade shrine + temple parts (parts/W2P1_NOTES.md)
from . import koran
koran.register(reg)
try:
    from . import trim
    trim.register(reg)
except ImportError:
    pass

# render hints for the contact sheets (context parts: [name, yaw, [x, y, z]])
RENDER_HINTS = {
    "jp_p_trim_grime_wall": {"ctx_plain": True, "context": [["jp_p_wall_shinkabe_shikkui", 0.0, [0, 0, 0]],
                                         ["jp_p_frame_post_planed", 0.0, [0, 0, 0]],
                                         ["jp_p_frame_post_planed", 0.0, [1.82, 0, 0]]], "view": "3q_low"},
    "jp_p_trim_grime_post": {"ctx_plain": True, "context": [["jp_p_frame_post_planed", 0.0, [0, 0, 0]]],
                             "view": "3q_low"},
    "jp_p_roof_ishioki_battens_stoneset8": {"context": [["jp_p_roof_ishioki_field_std", 0.0, [0, 0, 0]]]},
    "jp_p_roof_ishioki_battens_sparse": {"context": [["jp_p_roof_ishioki_field_std", 0.0, [0, 0, 0]]]},
    "jp_p_roof_sangawara_verge_L": {"context": [["jp_p_roof_sangawara_field_std", 0.0, [0.13, 0, 0]]]},
    "jp_p_roof_sangawara_verge_R": {"context": [["jp_p_roof_sangawara_field_std", 0.0, [-0.13, 0, 0]]]},
    "jp_p_roof_sangawara_eave_tomoe": {"context": [["jp_p_roof_sangawara_field_std", 0.0, [0, 0, 0]]]},
    "jp_p_roof_sangawara_eave_plain": {"context": [["jp_p_roof_sangawara_field_std", 0.0, [0, 0, 0]]]},
    "jp_p_roof_sangawara_eave_lod1_strip": {"context": [["jp_p_roof_sangawara_field_std", 0.0, [0, 0, 0]]]},
    "jp_p_roof_hafu_tile": {"view": "side"}, "jp_p_roof_hafu_board": {"view": "side"},
    "jp_p_roof_hafu_thatch": {"view": "side"},
    "jp_p_roof_eave_soffit_tile": {"view": "under", "no_ground": True, "drop": False},
    "jp_p_roof_eave_soffit_board": {"view": "under", "no_ground": True, "drop": False},
    "jp_p_roof_eave_soffit_thatch": {"view": "under", "no_ground": True, "drop": False},
    # B2 parts
    "jp_p_stair_box": {"view": "back"},
    "jp_p_roof_party_end_kawara": {"view": "3q_left", "drop": True},
    "jp_p_roof_party_end_board": {"view": "3q_left", "drop": True},
    "jp_p_roof_seam_cap_kawara": {"view": "3q_left", "drop": True,
                                  "context": [["jp_p_roof_party_end_kawara", 0.0, [0.0, 0.0, 0.0]],
                                              ["jp_p_roof_party_end_kawara", 180.0, [-0.128, 0.0, -5.46]]]},
    "jp_p_roof_seam_cap_board": {"view": "3q_left", "drop": True,
                                 "context": [["jp_p_roof_party_end_board", 0.0, [0.0, 0.0, 0.0]],
                                             ["jp_p_roof_party_end_board", 180.0, [-0.128, 0.0, -5.46]]]},
    "jp_p_roof_corner_tile": {"view": "3q_left", "drop": True,
                              "context": [["jp_p_roof_hisashi_tile", 0.0, [0.0, 0.0, 0.0]],
                                          ["jp_p_roof_hisashi_tile", 90.0, [0.0, 0.0, -3.64]]]},
    "jp_p_roof_corner_board": {"view": "3q_left", "drop": True,
                               "context": [["jp_p_roof_hisashi_board", 0.0, [0.0, 0.0, 0.0]],
                                           ["jp_p_roof_hisashi_board", 90.0, [0.0, 0.0, -3.64]]]},
    "jp_p_roof_corner_skirt": {"view": "3q_left", "drop": True,
                               "context": [["jp_p_roof_hisashi_skirt", 0.0, [0.0, 0.0, 0.0]],
                                           ["jp_p_roof_hisashi_skirt", 90.0, [0.0, 0.0, -3.64]]]},
}
