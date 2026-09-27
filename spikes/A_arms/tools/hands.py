"""Where a vanilla IK pose (.anm, the 4th argument of AddItemInHandsProfileIK) puts the two hands, in the
ITEM's model frame. Uses the Pokemon project's read-only player tools (anm_decode, player_fk, xob parser)
by import only - nothing there is modified.

Proven model (pokemon_dev/tools/player_anim/make_hold_pose.py docstring, checked on all vanilla heavy and
two-handed poses to 1 mm):  item = newR * RightHand_Dummy,  newL = item * LeftHandIKTarget.
So in item space:  right wrist = inv(RightHand_Dummy),  left wrist = LeftHandIKTarget.
Fingers: FK from each wrist with the pose's finger rotations and the .xob bind offsets.

For poses without LeftHandIKTarget (the bows: no hand IK) the left hand comes from a locomotion clip:
item = clipRightHand * RightHand_Dummy, left wrist = inv(item) * clipLeftHand.
"""
import os
import sys

PA = r"D:\DayZ-Server_AI-20260907-MultiMap\pokemon_dev\tools\player_anim"
sys.path.insert(0, PA)
from anm_decode import read_anm, sample  # noqa: E402
from player_fk import load_skeleton, local_pose, world_pose, xf_mul, xf_inv, qrot  # noqa: E402

_BONES = None


def bones():
    global _BONES
    if _BONES is None:
        _BONES = load_skeleton()
    return _BONES


def tracks(anm):
    return {t["name"]: (tuple(sample(t["t"], 0) or (0, 0, 0)), tuple(sample(t["q"], 0) or (0, 0, 0, 1)))
            for t in anm["tracks"]}


def finger_chain(grip_anm, wrist, side):
    """{bone: (t,q)} for one hand in the frame `wrist` lives in"""
    b = bones()
    loc = local_pose(b, grip_anm)
    by_name = {x["name"]: x for x in b}
    hand = side + "Hand"
    out = {hand: wrist}
    names = [x["name"] for x in b if x["name"].startswith(hand) and x["name"] != hand
             and "Dummy" not in x["name"] and "IK" not in x["name"] and "Origin" not in x["name"]]
    for n in names:
        chain = []
        x = by_name[n]
        while x["name"] != hand:
            chain.append(x["name"])
            x = b[x["parent"]]
        xf = wrist
        for c in reversed(chain):
            xf = xf_mul(xf, loc[c])
        out[n] = xf
    return out


def hand_segments(fw, side):
    b = bones()
    by_name = {x["name"]: x for x in b}
    segs = []
    for n, xf in fw.items():
        if n == side + "Hand":
            continue
        pn = b[by_name[n]["parent"]]["name"]
        if pn in fw:
            segs.append((fw[pn][0], xf[0]))
    return segs


def hands_in_item(ik_path, clip_path=None, clip_frame=0):
    """returns dict: right/left wrist (t,q) in item frame, finger dicts, segments"""
    a = read_anm(ik_path)
    T = tracks(a)
    D = T["RightHand_Dummy"]
    right = xf_inv(D)
    if "LeftHandIKTarget" in T:
        left = T["LeftHandIKTarget"]
        src = "LeftHandIKTarget"
    else:
        if not clip_path:
            raise ValueError("pose has no LeftHandIKTarget: give a locomotion clip")
        c = read_anm(clip_path)
        W = world_pose(bones(), local_pose(bones(), c, clip_frame))
        item = xf_mul(W["RightHand"], D)
        left = xf_mul(xf_inv(item), W["LeftHand"])
        src = "clip " + os.path.basename(clip_path)
    fr = finger_chain(a, right, "Right")
    fl = finger_chain(a, left, "Left")
    return {"right": right, "left": left, "fr": fr, "fl": fl, "left_source": src,
            "segs_r": hand_segments(fr, "Right"), "segs_l": hand_segments(fl, "Left")}


def palm_centre(fingers, side):
    """mean of the middle-finger knuckle and the wrist, pushed slightly toward the finger pads:
    roughly where a grip axis passes through the closed hand"""
    w = fingers[side + "Hand"][0]
    m1 = fingers[side + "HandMiddle1"][0]
    m3 = fingers.get(side + "HandMiddle3", fingers[side + "HandMiddle1"])[0]
    i1 = fingers[side + "HandIndex1"][0]
    p1 = fingers[side + "HandPinky1"][0]
    # the grip passes between the knuckle line and the curled finger tips
    k = [(i1[j] + p1[j] + m1[j]) / 3 for j in range(3)]
    return [(k[j] * 0.5 + m3[j] * 0.35 + w[j] * 0.15) for j in range(3)]


if __name__ == "__main__":
    h = hands_in_item(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    for s in ("right", "left"):
        print(s, "wrist", tuple(round(c, 4) for c in h[s][0]))
    print("right palm", [round(c, 3) for c in palm_centre(h["fr"], "Right")])
    print("left palm", [round(c, 3) for c in palm_centre(h["fl"], "Left")], h["left_source"])
