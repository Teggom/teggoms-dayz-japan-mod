#!/bin/sh
# build + peek every statue (or the given ones) and stack them -> _build/peekall.png
cd "$(dirname "$0")"
N="${@:-nyorai_jo nyorai_semui kannon jizo jizo_stone jizo_child komainu_a_a komainu_a_un komainu_b_a komainu_b_un kitsune_key kitsune_jewel}"
python statues.py $N || exit 1
for n in $N; do python peek.py $n 0 --views front,q,side >/dev/null || exit 1; done
python - $N <<'PY'
import sys
from PIL import Image, ImageDraw
ims=[]
for n in sys.argv[1:]:
    im=Image.open('renders/peek_%s_l0.png'%n); im.thumbnail((900,370)); d=ImageDraw.Draw(im); d.text((5,5),n,fill=(255,255,0)); ims.append(im)
cols=2; W=max(i.width for i in ims); H=max(i.height for i in ims)
S=Image.new('RGB',(cols*W,((len(ims)+1)//cols)*H),(60,60,60))
for i,im in enumerate(ims): S.paste(im,((i%cols)*W,(i//cols)*H))
S.save('_build/peekall.png')
print(S.size)
PY
