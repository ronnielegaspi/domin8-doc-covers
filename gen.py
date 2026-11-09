from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1500, 560
BG = (17, 22, 26)
INK = (244, 245, 242)

AREAS = [
    ("Character",            "character",            (90, 140, 200), "contour"),
    ("Weapons",              "weapons",              (214, 168, 70), "ballistic"),
    ("Special Equipment",    "special-equipment",    (150, 115, 80), "scatter"),
    ("Vehicles",             "vehicles",             (200, 110, 55), "tracks"),
    ("Unmanned",             "unmanned",             (150, 115, 190), "orbit"),
    ("AI",                   "ai",                   (200, 105, 150), "network"),
    ("EW",                   "ew",                   (194, 90, 43),  "radial"),
    ("Scenario & Instructor","scenario-instructor",  (70, 150, 125), "grid"),
    ("Environment",          "environment",          (120, 135, 130), "terrain"),
    ("Online & Net",         "online-net",           (140, 110, 90), "mesh"),
    ("UI & Controls",        "ui-controls",          (110, 160, 175), "panels"),
    ("Audio",                "audio",                (170, 170, 110), "wave"),
    ("Telemetry & AAR",      "telemetry-aar",        (95, 170, 150), "plot"),
]

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

def draw_motif(d, kind, ac, rnd):
    dim = mix(ac, BG, 0.74)
    mid = mix(ac, BG, 0.50)
    if kind == "contour":
        for i in range(14):
            y0 = 90 + i * 34
            pts = [(x, y0 + math.sin(x / 150.0 + i * 0.6) * 22 + math.sin(x / 47.0) * 6) for x in range(0, W + 10, 10)]
            d.line(pts, fill=dim if i % 3 else mid, width=2)
    elif kind == "ballistic":
        for i in range(9):
            x0, y0 = -40, 430 - i * 14
            pts = [(x, y0 - (x / 1500.0) * (120 + i * 26) + ((x / 1500.0) ** 2) * (150 + i * 30)) for x in range(0, W + 10, 12)]
            d.line(pts, fill=dim if i % 2 else mid, width=2)
    elif kind == "scatter":
        for _ in range(120):
            x, y = rnd.randint(40, W - 40), rnd.randint(70, H - 70)
            r = rnd.choice([3, 4, 6, 9])
            d.ellipse([x - r, y - r, x + r, y + r], outline=dim if r < 6 else mid, width=2)
    elif kind == "tracks":
        for i in range(10):
            y = 100 + i * 42
            for x in range(0, W, 46):
                d.line([(x, y), (x + 26, y)], fill=dim if i % 2 else mid, width=4)
    elif kind == "orbit":
        cx, cy = W - 360, H // 2
        for i in range(7):
            r = 60 + i * 46
            d.ellipse([cx - r, cy - r * 0.42, cx + r, cy + r * 0.42], outline=dim if i % 2 else mid, width=2)
    elif kind == "network":
        nodes = [(rnd.randint(60, W - 60), rnd.randint(80, H - 80)) for _ in range(26)]
        for i, a in enumerate(nodes):
            for b in nodes[i + 1:]:
                if math.dist(a, b) < 230:
                    d.line([a, b], fill=dim, width=1)
        for n in nodes:
            d.ellipse([n[0] - 4, n[1] - 4, n[0] + 4, n[1] + 4], fill=mid)
    elif kind == "radial":
        cx, cy = W - 300, H // 2
        for a in range(0, 360, 6):
            r1, r2 = 70, 70 + (190 if (a // 6) % 4 == 0 else 120)
            ra = math.radians(a)
            d.line([(cx + r1 * math.cos(ra), cy + r1 * math.sin(ra) * 0.55),
                    (cx + r2 * math.cos(ra), cy + r2 * math.sin(ra) * 0.55)], fill=dim, width=2)
        for r in (110, 180, 250):
            d.ellipse([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], outline=mid, width=2)
    elif kind == "grid":
        for x in range(0, W + 1, 60): d.line([(x, 60), (x, H - 60)], fill=dim, width=1)
        for y in range(60, H - 59, 60): d.line([(0, y), (W, y)], fill=dim, width=1)
        for _ in range(7):
            gx, gy = rnd.randrange(0, W - 120, 60), rnd.randrange(60, H - 180, 60)
            d.rectangle([gx, gy, gx + 120, gy + 120], outline=mid, width=3)
    elif kind == "terrain":
        for i in range(11):
            base = 150 + i * 36
            pts = [(x, base + math.sin(x / 210.0 + i) * 34 + math.sin(x / 70.0 + i * 2) * 11) for x in range(0, W + 10, 8)]
            d.line(pts, fill=dim if i % 2 else mid, width=2)
    elif kind == "mesh":
        pts = [(rnd.randint(40, W - 40), rnd.randint(70, H - 70)) for _ in range(20)]
        for i, a in enumerate(pts):
            for b in pts[i + 1:]:
                if math.dist(a, b) < 300:
                    d.line([a, b], fill=dim, width=1)
        for p in pts:
            d.rectangle([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], outline=mid, width=2)
    elif kind == "panels":
        x = 60
        while x < W - 60:
            w = rnd.choice([110, 170, 240])
            h = rnd.choice([90, 150, 210])
            y = rnd.choice([110, 190, 260])
            d.rectangle([x, y, x + w, y + h], outline=dim, width=2)
            d.line([(x + 12, y + 18), (x + w - 12, y + 18)], fill=mid, width=2)
            x += w + 26
    elif kind == "wave":
        for i in range(5):
            amp = 30 + i * 22
            pts = [(x, H // 2 + math.sin(x / (40.0 + i * 16)) * amp * math.sin(x / 600.0)) for x in range(0, W + 6, 6)]
            d.line(pts, fill=dim if i % 2 else mid, width=2)
    elif kind == "plot":
        d.line([(90, H - 120), (W - 90, H - 120)], fill=mid, width=2)
        d.line([(90, 90), (90, H - 120)], fill=mid, width=2)
        for s in range(4):
            y = H - 140
            pts = []
            for x in range(90, W - 90, 18):
                y += rnd.randint(-16, 14) - s
                y = max(110, min(H - 130, y))
                pts.append((x, y))
            d.line(pts, fill=dim if s % 2 else mid, width=2)

for name, slug, ac, kind in AREAS:
    rnd = random.Random(sum(ord(c) for c in slug))
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_motif(d, kind, ac, rnd)
    # centred scrim so type survives gallery-card cropping
    scrim = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(scrim)
    cxm = W // 2
    for x in range(W):
        f = max(0.0, 1 - abs(x - cxm) / 560.0)
        sd.line([(x, 0), (x, H)], fill=int(232 * (f ** 1.25)))
    img.paste(Image.new("RGB", (W, H), BG), (0, 0), scrim)
    d = ImageDraw.Draw(img)
    f_eyebrow, f_title = font(21), font(62, True)
    eyebrow = "DOMIN8  ·  SYSTEM DOCUMENTATION"
    tw = d.textlength(eyebrow, font=f_eyebrow)
    d.text((cxm - tw / 2, 212), eyebrow, font=f_eyebrow, fill=mix(INK, BG, 0.52))
    label = name.upper()
    f_t = f_title
    lw = d.textlength(label, font=f_t)
    if lw > W - 320:
        f_t = font(46, True)
        lw = d.textlength(label, font=f_t)
    d.text((cxm - lw / 2, 252), label, font=f_t, fill=INK)
    d.rectangle([cxm - 46, 338, cxm + 46, 344], fill=ac)
    img.save(f"{slug}.png", optimize=True)
    print(slug)
