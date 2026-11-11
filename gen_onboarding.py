from PIL import Image, ImageDraw, ImageFont
import math, random

BG  = (17, 22, 26)
INK = (244, 245, 242)

def font(sz, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

def mix(c, t, f):
    return tuple(int(a + (b - a) * f) for a, b in zip(c, t))

# ---------- page cover : 1500 x 500, chain-of-access mesh ----------
W, H = 1500, 500
AC = (70, 150, 125)
rnd = random.Random(11)
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
dim, mid = mix(AC, BG, 0.78), mix(AC, BG, 0.46)

# mesh field
pts = [(rnd.randint(30, W - 30), rnd.randint(50, H - 50)) for _ in range(24)]
for i, a in enumerate(pts):
    for b in pts[i + 1:]:
        if math.dist(a, b) < 300:
            d.line([a, b], fill=dim, width=1)
for p in pts:
    d.rectangle([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], outline=mid, width=2)

# the five-stage chain, drawn as linked nodes across the lower third
stages = ["ID", "VPN", "GIT", "LFS", "UE5"]
n = len(stages)
y = H - 118
x0, x1 = 150, W - 150
step = (x1 - x0) / (n - 1)
f_tag = font(17, True)
for i in range(n - 1):
    d.line([(x0 + i * step + 34, y), (x0 + (i + 1) * step - 34, y)], fill=mix(AC, BG, 0.35), width=3)
for i, s in enumerate(stages):
    cx = x0 + i * step
    d.ellipse([cx - 30, y - 30, cx + 30, y + 30], fill=BG, outline=AC, width=3)
    tw = d.textlength(s, font=f_tag)
    d.text((cx - tw / 2, y - 9), s, font=f_tag, fill=INK)

# centred scrim so type survives cover cropping
scrim = Image.new("L", (W, H), 0)
sd = ImageDraw.Draw(scrim)
for x in range(W):
    f = max(0.0, 1 - abs(x - W // 2) / 620.0)
    sd.line([(x, 0), (x, H - 200)], fill=int(236 * (f ** 1.2)))
img.paste(Image.new("RGB", (W, H), BG), (0, 0), scrim)
d = ImageDraw.Draw(img)

f_eye, f_title, f_sub = font(21), font(66, True), font(24)
cxm = W // 2
eye = "DOMIN8  ·  NEW STARTER"
tw = d.textlength(eye, font=f_eye)
d.text((cxm - tw / 2, 96), eye, font=f_eye, fill=mix(INK, BG, 0.52))
lab = "PROJECT ONBOARDING"
lw = d.textlength(lab, font=f_title)
d.text((cxm - lw / 2, 134), lab, font=f_title, fill=INK)
d.rectangle([cxm - 46, 222, cxm + 46, 228], fill=AC)
sub = "laptop to Unreal, in five steps"
sw = d.textlength(sub, font=f_sub)
d.text((cxm - sw / 2, 250), sub, font=f_sub, fill=mix(INK, BG, 0.42))
img.save("onboarding.png", optimize=True)
print("onboarding.png")

# ---------- step banners : 1400 x 170 ----------
STEPS = [
    ("01", "ACCOUNTS & VPN",  "onboarding-step-1", (90, 140, 200),  "nodes"),
    ("02", "GIT & GITLAB",    "onboarding-step-2", (214, 168, 70),  "branch"),
    ("03", "CLONE THE REPO",  "onboarding-step-3", (70, 150, 125),  "stack"),
    ("04", "UNREAL ENGINE",   "onboarding-step-4", (150, 115, 190), "cubes"),
    ("05", "DAY TO DAY",      "onboarding-step-5", (120, 150, 140), "pulse"),
]
BW, BH = 1400, 170
for num, name, slug, ac, motif in STEPS:
    r = random.Random(sum(ord(c) for c in slug))
    im = Image.new("RGB", (BW, BH), BG)
    dd = ImageDraw.Draw(im)
    dm, md = mix(ac, BG, 0.80), mix(ac, BG, 0.52)
    if motif == "nodes":
        p = [(r.randint(700, BW - 30), r.randint(25, BH - 25)) for _ in range(14)]
        for i, a in enumerate(p):
            for b in p[i + 1:]:
                if math.dist(a, b) < 180: dd.line([a, b], fill=dm, width=1)
        for q in p: dd.ellipse([q[0] - 4, q[1] - 4, q[0] + 4, q[1] + 4], fill=md)
    elif motif == "branch":
        base = BH // 2
        dd.line([(700, base), (BW - 40, base)], fill=md, width=3)
        for i in range(4):
            sx = 780 + i * 150
            off = 46 if i % 2 == 0 else -46
            dd.line([(sx, base), (sx + 44, base + off)], fill=dm, width=2)
            dd.line([(sx + 44, base + off), (sx + 150, base + off)], fill=dm, width=2)
            dd.ellipse([sx + 146, base + off - 5, sx + 156, base + off + 5], fill=md)
    elif motif == "stack":
        for i in range(6):
            x = 740 + i * 108
            h = 26 + (i % 3) * 30
            dd.rectangle([x, BH // 2 - h, x + 72, BH // 2 + h], outline=dm if i % 2 else md, width=2)
    elif motif == "cubes":
        for i in range(5):
            x, s = 760 + i * 128, 34 + (i % 2) * 16
            cy = BH // 2
            dd.polygon([(x, cy - s), (x + s, cy), (x, cy + s), (x - s, cy)], outline=dm if i % 2 else md)
    elif motif == "pulse":
        pts = [(x, BH // 2 + math.sin((x - 700) / 46.0) * 34 * math.sin((x - 700) / 320.0)) for x in range(700, BW - 20, 5)]
        dd.line(pts, fill=md, width=2)
    # left scrim for type
    sc = Image.new("L", (BW, BH), 0)
    sdd = ImageDraw.Draw(sc)
    for x in range(BW):
        f = max(0.0, 1 - max(0, x - 40) / 660.0)
        sdd.line([(x, 0), (x, BH)], fill=int(242 * (f ** 0.85)))
    im.paste(Image.new("RGB", (BW, BH), BG), (0, 0), sc)
    dd = ImageDraw.Draw(im)
    f_n, f_l = font(58, True), font(32, True)
    dd.text((54, 50), num, font=f_n, fill=ac)
    dd.rectangle([140, 56, 144, 118], fill=mix(ac, BG, 0.45))
    dd.text((170, 68), name, font=f_l, fill=INK)
    im.save(f"{slug}.png", optimize=True)
    print(slug)
