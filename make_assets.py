import math
import os
import random
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
S = 4  # supersample factor for smooth edges
random.seed(7)
np.random.seed(7)


def mk(*parts):
    p = os.path.join(OUT, *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


# ---------------------------------------------------------------- drawing
def new(size):
    img = Image.new("RGBA", (size * S, size * S), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def done(img, size):
    return img.resize((size, size), Image.LANCZOS)


def sc(v):
    return int(round(v * S))


def circle(d, cx, cy, r, fill=None, outline=None, w=1):
    d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)], fill=fill,
              outline=outline, width=sc(w) if outline else 0)


def rrect(d, x0, y0, x1, y1, r, fill=None, outline=None, w=1):
    d.rounded_rectangle([sc(x0), sc(y0), sc(x1), sc(y1)], radius=sc(r), fill=fill,
                        outline=outline, width=sc(w) if outline else 0)


def poly(d, pts, fill=None, outline=None, w=1):
    pp = [(sc(x), sc(y)) for x, y in pts]
    d.polygon(pp, fill=fill)
    if outline:
        d.line(pp + [pp[0], pp[1]], fill=outline, width=sc(w), joint="curve")


def line(d, pts, fill, w=1):
    d.line([(sc(x), sc(y)) for x, y in pts], fill=fill, width=sc(w), joint="curve")


def hexagon(cx, cy, r, rot=0):
    return [(cx + r * math.cos(math.radians(60 * i + rot)),
             cy + r * math.sin(math.radians(60 * i + rot))) for i in range(6)]


DARK = (24, 26, 36, 255)

# ---------------------------------------------------------------- towers (60px)
T = 60


def tower_base(d, accent):
    rrect(d, 3, 3, 57, 57, 8, (44, 48, 62, 255), (20, 22, 30, 255), 2)
    rrect(d, 7, 7, 53, 53, 5, (58, 63, 80, 255))
    for x, y in [(10, 10), (50, 10), (10, 50), (50, 50)]:
        circle(d, x, y, 2.5, accent)


def tower_cannon():
    img, d = new(T)
    tower_base(d, (200, 200, 215, 255))
    rrect(d, 25, 5, 35, 32, 3, (96, 104, 118, 255), DARK, 1.5)
    rrect(d, 23, 5, 37, 11, 2, (70, 76, 90, 255), DARK, 1.5)
    circle(d, 30, 33, 15, (150, 160, 176, 255), DARK, 2)
    circle(d, 30, 33, 8, (110, 118, 132, 255), DARK, 1.5)
    circle(d, 27, 30, 2.5, (210, 216, 228, 255))
    return done(img, T)


def tower_fire():
    img, d = new(T)
    tower_base(d, (255, 120, 50, 255))
    rrect(d, 25, 8, 35, 32, 3, (130, 52, 40, 255), DARK, 1.5)
    circle(d, 30, 33, 15, (190, 60, 40, 255), DARK, 2)
    circle(d, 30, 33, 9, (255, 140, 50, 255))
    circle(d, 30, 33, 4, (255, 232, 130, 255))
    poly(d, [(30, 0), (37, 9), (33, 12), (30, 6), (27, 12), (23, 9)], (255, 175, 50, 255), (140, 50, 10, 255), 1)
    return done(img, T)


def tower_ice():
    img, d = new(T)
    tower_base(d, (120, 210, 255, 255))
    ol = (20, 70, 110, 255)
    poly(d, [(12, 33), (17, 24), (22, 33), (17, 44)], (150, 225, 255, 255), ol, 1.5)
    poly(d, [(38, 33), (43, 24), (48, 33), (43, 44)], (150, 225, 255, 255), ol, 1.5)
    poly(d, [(30, 7), (43, 30), (30, 54), (17, 30)], (130, 215, 255, 255), ol, 2)
    poly(d, [(30, 9), (41, 30), (30, 30)], (205, 242, 255, 255))
    poly(d, [(30, 30), (41, 30), (30, 52)], (80, 172, 222, 255))
    return done(img, T)


def tower_arcane():
    img, d = new(T)
    tower_base(d, (190, 110, 255, 255))
    circle(d, 30, 30, 17, (110, 50, 170, 255), (30, 15, 60, 255), 2)
    circle(d, 30, 30, 12, None, (225, 175, 255, 255), 2)
    circle(d, 30, 30, 7, (225, 185, 255, 255))
    circle(d, 30, 30, 3.5, (255, 255, 255, 255))
    for a in range(0, 360, 90):
        circle(d, 30 + 22 * math.cos(math.radians(a + 45)), 30 + 22 * math.sin(math.radians(a + 45)), 2.2,
               (225, 175, 255, 255))
    return done(img, T)


# ---------------------------------------------------------------- enemies
def enemy_grunt():
    E = 48
    img, d = new(E)
    circle(d, 16, 42, 4.5, (60, 140, 62, 255), (28, 70, 32, 255), 1.5)
    circle(d, 32, 42, 4.5, (60, 140, 62, 255), (28, 70, 32, 255), 1.5)
    circle(d, 24, 26, 17, (96, 190, 90, 255), (28, 70, 32, 255), 2)
    circle(d, 18, 22, 5.5, (255, 255, 255, 255), (28, 70, 32, 255), 1)
    circle(d, 31, 22, 5.5, (255, 255, 255, 255), (28, 70, 32, 255), 1)
    circle(d, 19, 23, 2.4, (10, 10, 10, 255))
    circle(d, 32, 23, 2.4, (10, 10, 10, 255))
    rrect(d, 19, 33, 29, 35.5, 1, (28, 70, 32, 255))
    return done(img, E)


def enemy_fast():
    E = 48
    img, d = new(E)
    for y in (17, 25, 33):
        line(d, [(2, y), (11, y)], (255, 232, 150, 190), 2)
    circle(d, 26, 25, 13, (250, 205, 60, 255), (120, 80, 10, 255), 2)
    circle(d, 22, 23, 4, (255, 255, 255, 255), (120, 80, 10, 255), 1)
    circle(d, 32, 23, 4, (255, 255, 255, 255), (120, 80, 10, 255), 1)
    circle(d, 23, 24, 1.8, (10, 10, 10, 255))
    circle(d, 33, 24, 1.8, (10, 10, 10, 255))
    line(d, [(17, 16), (25, 20)], (90, 50, 5, 255), 2)
    line(d, [(37, 16), (29, 20)], (90, 50, 5, 255), 2)
    return done(img, E)


def enemy_tank():
    E = 48
    img, d = new(E)
    poly(d, hexagon(24, 24, 22, 30), (120, 128, 150, 255), (36, 40, 56, 255), 2)
    poly(d, hexagon(24, 24, 15, 30), (92, 100, 124, 255), (36, 40, 56, 255), 1.5)
    for p in hexagon(24, 24, 18.5, 0):
        circle(d, p[0], p[1], 1.6, (190, 196, 214, 255))
    rrect(d, 12, 20, 36, 28, 2, (30, 34, 46, 255))
    rrect(d, 15, 22, 21, 26, 1, (255, 90, 70, 255))
    rrect(d, 27, 22, 33, 26, 1, (255, 90, 70, 255))
    return done(img, E)


def enemy_boss():
    E = 64
    img, d = new(E)
    circle(d, 32, 37, 23, (150, 70, 200, 255), (50, 20, 80, 255), 3)
    for pts in ([(13, 24), (17, 5), (25, 19)], [(25, 19), (32, 1), (39, 19)], [(39, 19), (47, 5), (51, 24)]):
        poly(d, pts, (255, 205, 60, 255), (120, 80, 10, 255), 1.5)
    circle(d, 23, 34, 6.5, (255, 255, 255, 255), (50, 20, 80, 255), 1.5)
    circle(d, 41, 34, 6.5, (255, 255, 255, 255), (50, 20, 80, 255), 1.5)
    circle(d, 24, 35, 2.8, (200, 30, 30, 255))
    circle(d, 40, 35, 2.8, (200, 30, 30, 255))
    rrect(d, 21, 46, 43, 52, 2, (40, 14, 60, 255))
    for x in (24, 30, 36):
        rrect(d, x, 46, x + 4, 49.5, 0.5, (255, 255, 255, 255))
    return done(img, E)


def shield(color):
    E = 48
    img, d = new(E)
    circle(d, 24, 24, 22, color[:3] + (45,), color[:3] + (235,), 2.5)
    return done(img, E)


# ---------------------------------------------------------------- tiles (60px, drawn 1x)
def noise_tile(base, speck_a, speck_b, n):
    img = Image.new("RGBA", (T, T), base)
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = random.randint(0, T - 3), random.randint(0, T - 3)
        w, h = random.randint(2, 4), random.randint(1, 3)
        d.ellipse([x, y, x + w, y + h], fill=random.choice([speck_a, speck_b]))
    return img, d


def tile_grass(seed):
    random.seed(seed)
    img, d = noise_tile((74, 140, 70, 255), (62, 122, 60, 255), (92, 160, 86, 255), 90)
    for _ in range(3):
        x, y = random.randint(4, T - 6), random.randint(4, T - 6)
        d.ellipse([x, y, x + 3, y + 3], fill=random.choice([(250, 250, 250, 255), (250, 220, 90, 255)]))
    return img


def tile_path():
    random.seed(5)
    img, d = noise_tile((176, 142, 96, 255), (150, 118, 76, 255), (200, 168, 120, 255), 80)
    for _ in range(5):
        x, y = random.randint(3, T - 8), random.randint(3, T - 8)
        d.ellipse([x, y, x + random.randint(3, 6), y + random.randint(2, 4)], fill=(128, 118, 108, 255))
    return img


def tile_overlay(ok):
    img, d = new(T)
    col = (80, 220, 100) if ok else (230, 70, 70)
    rrect(d, 2, 2, 58, 58, 6, col + (80,), col + (230,), 2)
    if not ok:
        line(d, [(18, 18), (42, 42)], (230, 70, 70, 240), 4)
        line(d, [(42, 18), (18, 42)], (230, 70, 70, 240), 4)
    return done(img, T)


def tile_base():
    img, d = new(T)
    rrect(d, 8, 16, 52, 56, 3, (140, 146, 162, 255), DARK, 2)
    for x in (8, 20, 32, 44):
        rrect(d, x, 8, x + 8, 18, 1, (140, 146, 162, 255), DARK, 1.5)
    rrect(d, 23, 34, 37, 56, 7, (40, 34, 50, 255), DARK, 1.5)
    line(d, [(30, 8), (30, -4)], (110, 80, 50, 255), 2)
    poly(d, [(30, 1), (44, 6), (30, 11)], (230, 70, 70, 255))
    for x, y in [(14, 28), (46, 28), (14, 44), (46, 44)]:
        rrect(d, x - 3, y - 3, x + 3, y + 3, 1, (100, 106, 122, 255))
    return done(img, T)


def tile_spawn():
    img, d = new(T)
    circle(d, 30, 30, 26, (50, 18, 80, 255))
    circle(d, 30, 30, 20, (110, 50, 170, 255))
    circle(d, 30, 30, 13, (190, 120, 255, 255))
    circle(d, 30, 30, 6, (20, 6, 36, 255))
    return done(img, T)


# ---------------------------------------------------------------- bullets, icons, fx
def bullet(kind):
    B = 16
    img, d = new(B)
    if kind == "cannon":
        circle(d, 8, 8, 6.5, (70, 74, 84, 255), DARK, 1)
        circle(d, 6, 6, 2, (175, 182, 196, 255))
    elif kind == "fire":
        circle(d, 8, 8, 6.5, (255, 140, 40, 255), (150, 50, 10, 255), 1)
        circle(d, 8, 8, 3.5, (255, 225, 110, 255))
    elif kind == "ice":
        poly(d, [(8, 0.5), (12.5, 8), (8, 15.5), (3.5, 8)], (140, 225, 255, 255), (40, 110, 160, 255), 1)
    else:
        circle(d, 8, 8, 6.5, (170, 90, 240, 255), (60, 20, 100, 255), 1)
        circle(d, 8, 8, 3, (245, 210, 255, 255))
    return done(img, B)


LIGHT = (235, 238, 245, 255)
OUTL = (30, 34, 44, 255)


def icon(kind):
    I = 32
    img, d = new(I)
    if kind == "coin":
        circle(d, 16, 16, 13, (250, 200, 50, 255), (150, 100, 10, 255), 2)
        circle(d, 16, 16, 8, None, (200, 150, 20, 255), 2)
    elif kind == "heart":
        for col, g in (((120, 20, 40, 255), 1.6), ((230, 60, 80, 255), 0)):
            circle(d, 11, 12, 7 + g, col)
            circle(d, 21, 12, 7 + g, col)
            poly(d, [(4 - g, 14.5), (28 + g, 14.5), (16, 29 + g)], col)
    elif kind == "wave":
        rrect(d, 7, 3, 10, 29, 1, (110, 80, 50, 255))
        poly(d, [(10, 4), (27, 11), (10, 18)], (255, 120, 60, 255), (140, 50, 10, 255), 1.5)
    elif kind == "play":
        poly(d, [(9, 5), (9, 27), (27, 16)], LIGHT, OUTL, 2)
    elif kind == "pause":
        rrect(d, 8, 5, 14, 27, 1.5, LIGHT, OUTL, 1.5)
        rrect(d, 18, 5, 24, 27, 1.5, LIGHT, OUTL, 1.5)
    else:  # fast forward
        poly(d, [(3, 6), (3, 26), (16, 16)], LIGHT, OUTL, 1.5)
        poly(d, [(16, 6), (16, 26), (29, 16)], LIGHT, OUTL, 1.5)
    return done(img, I)


def explosion(i, n=6):
    X = 64
    img, d = new(X)
    t = i / (n - 1)
    r = 8 + t * 22
    a = int(255 * (1 - t * 0.85))
    circle(d, 32, 32, r, (255, 120, 30, a))
    circle(d, 32, 32, r * 0.68, (255, 200, 70, a))
    circle(d, 32, 32, r * 0.32, (255, 250, 205, a))
    rnd = random.Random(i)
    for k in range(8):
        ang = k * math.pi / 4 + rnd.uniform(-0.2, 0.2)
        dist = r * rnd.uniform(1.05, 1.35)
        circle(d, 32 + dist * math.cos(ang), 32 + dist * math.sin(ang), max(1.0, 3.4 - t * 2.4),
               (255, 190, 60, a))
    return done(img, X)


def make_images():
    sprites = {
        ("towers", "cannon"): tower_cannon(), ("towers", "fire"): tower_fire(),
        ("towers", "ice"): tower_ice(), ("towers", "arcane"): tower_arcane(),
        ("enemies", "grunt"): enemy_grunt(), ("enemies", "fast"): enemy_fast(),
        ("enemies", "tank"): enemy_tank(), ("enemies", "boss"): enemy_boss(),
        ("enemies", "shield_physical"): shield((200, 200, 215)),
        ("enemies", "shield_fire"): shield((255, 110, 50)),
        ("enemies", "shield_ice"): shield((110, 210, 255)),
        ("tiles", "grass1"): tile_grass(1), ("tiles", "grass2"): tile_grass(2),
        ("tiles", "path"): tile_path(),
        ("tiles", "build_ok"): tile_overlay(True), ("tiles", "build_bad"): tile_overlay(False),
        ("tiles", "base"): tile_base(), ("tiles", "spawn"): tile_spawn(),
    }
    for k in ("cannon", "fire", "ice", "arcane"):
        sprites[("fx", "bullet_" + k)] = bullet(k)
    for k in ("coin", "heart", "wave", "play", "pause", "fast"):
        sprites[("ui", k)] = icon(k)
    for i in range(6):
        sprites[("fx", f"explosion_{i}")] = explosion(i)
    for (folder, name), im in sprites.items():
        im.save(mk(folder, name + ".png"))
    return sprites


# ---------------------------------------------------------------- sound
SR = 44100


def tt(dur):
    return np.arange(int(SR * dur)) / SR


def osc(freq, kind="sine"):
    ph = np.cumsum(freq) / SR
    if kind == "square":
        return np.sign(np.sin(2 * np.pi * ph))
    if kind == "saw":
        return 2 * (ph % 1) - 1
    if kind == "tri":
        return 2 * np.abs(2 * (ph % 1) - 1) - 1
    return np.sin(2 * np.pi * ph)


def sweep(f0, f1, dur, kind="sine"):
    x = tt(dur)
    return osc(f0 * (f1 / f0) ** (x / dur), kind)


def env(n, a=0.004, k=8.0):
    x = np.arange(n) / SR
    return np.minimum(1, x / a) * np.exp(-x * k)


def noise(n):
    return np.random.uniform(-1, 1, n)


def lowpass(x, win):
    return np.convolve(x, np.ones(win) / win, mode="same")


def note(f, dur, kind="square", k=6.0, vol=0.3, a=0.004):
    n = int(SR * dur)
    return osc(np.full(n, float(f)), kind) * env(n, a, k) * vol


def mix(total, parts):
    out = np.zeros(int(SR * total))
    for off, sig in parts:
        i = int(SR * off)
        j = min(len(out), i + len(sig))
        out[i:j] += sig[: j - i]
    return out


def save(name, x, folder="sounds"):
    x = np.asarray(x, dtype=float)
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.8
    wav_path = mk(folder, name + ".wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    ogg_path = mk(folder, name + ".ogg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path, "-c:a", "libvorbis", "-q:a", "4",
                    ogg_path], check=True)
    os.remove(wav_path)


def make_sounds():
    n = int(SR * 0.3)
    save("shoot_cannon", sweep(200, 50, 0.3) * env(n, 0.002, 9) + lowpass(noise(n), 40) * env(n, 0.001, 25) * 0.6)

    d = 0.4
    n = int(SR * d)
    x = np.arange(n) / SR
    save("shoot_fire", lowpass(noise(n), 30) * np.sin(np.pi * x / d) ** 0.8)

    n = int(SR * 0.22)
    save("shoot_ice", (sweep(2200, 900, 0.22) + 0.3 * sweep(4400, 1800, 0.22)) * env(n, 0.002, 10))

    x = tt(0.25)
    f = 500 + 300 * np.sin(2 * np.pi * 30 * x)
    save("shoot_arcane", osc(f, "square") * 0.5 * env(len(x), 0.002, 9))

    n = int(SR * 0.08)
    save("hit", lowpass(noise(n), 8) * env(n, 0.001, 40) + 0.4 * note(300, 0.08, "sine", 35, 1.0))

    n = int(SR * 0.3)
    save("enemy_die", sweep(520, 90, 0.3, "square") * env(n, 0.002, 7) * 0.5 + lowpass(noise(n), 6) * env(n, 0.001, 15) * 0.4)

    n = int(SR * 0.14)
    thud1 = sweep(260, 120, 0.14) * env(n, 0.002, 18)
    thud2 = sweep(400, 200, 0.14) * env(n, 0.002, 18)
    save("place_tower", mix(0.3, [(0, thud1), (0.09, thud2), (0, lowpass(noise(n), 5) * env(n, 0.001, 50) * 0.5)]))

    save("sell", mix(0.4, [(0, note(988, 0.1, "square", 12)), (0.09, note(1319, 0.25, "square", 9))]))

    notes = [261.6, 329.6, 392.0, 523.3]
    parts = [(i * 0.14, note(f, 0.16, "saw", 6, 0.3)) for i, f in enumerate(notes[:3])]
    parts.append((3 * 0.14, note(notes[3], 0.6, "saw", 3, 0.3)))
    save("wave_start", mix(1.1, parts))

    x = tt(0.45)
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 18 * x)
    save("life_lost", osc(np.full(len(x), 110.0), "saw") * trem * env(len(x), 0.004, 4) * 0.6
         + sweep(160, 70, 0.45, "square") * env(len(x), 0.004, 5) * 0.3)

    save("adapt_alert", mix(0.9, [(i * 0.2, note(f, 0.18, "saw", 5, 0.3)) for i, f in enumerate([523, 415, 330])]
                              + [(0.45, note(165, 0.4, "sine", 4, 0.4))]))

    save("game_over", mix(2.2, [(0, note(220, 0.5, "saw", 3, 0.3)), (0.3, note(174.6, 0.5, "saw", 3, 0.3)),
                                (0.6, note(146.8, 0.5, "saw", 3, 0.3)), (0.9, note(110, 1.2, "saw", 2.5, 0.35))]))

    save("victory", mix(1.4, [(0, note(523.3, 0.14, "square", 6)), (0.12, note(659.3, 0.14, "square", 6)),
                              (0.24, note(784, 0.14, "square", 6)), (0.36, note(1046.5, 0.9, "square", 3))]))

    save("click", note(1200, 0.04, "square", 60, 0.4))


def make_music():
    bpm = 100
    beat = 60 / bpm
    chords = [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (261.6, 329.6, 392.0), (196.0, 246.9, 293.7)]
    bar = beat * 4
    total = bar * len(chords)
    parts = []
    eighth = beat / 2
    pattern = [0, 1, 2, 1, 0, 1, 2, 1]
    for b, ch in enumerate(chords):
        off = b * bar
        parts.append((off, note(ch[0] / 2, beat * 2, "sine", 3, 0.35)))
        parts.append((off + beat * 2, note(ch[0] / 2, beat * 2, "sine", 3, 0.3)))
        for i, p in enumerate(pattern):
            parts.append((off + i * eighth, note(ch[p] * 2, eighth, "square", 7, 0.12)))
            hat_n = int(SR * 0.05)
            hat = (noise(hat_n) - lowpass(noise(hat_n), 8)) * env(hat_n, 0.001, 60) * 0.08
            if i % 2 == 1:
                parts.append((off + i * eighth, hat))
    save("theme", mix(total, parts), folder="music")


# ---------------------------------------------------------------- loader + readme
LOADER = '''import os

import pygame

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def load_images():
    """Call after pygame.display.set_mode(). Returns {name: Surface}, e.g. images["cannon"]."""
    images = {}
    for folder, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".png"):
                path = os.path.join(folder, f)
                images[os.path.splitext(f)[0]] = pygame.image.load(path).convert_alpha()
    return images


def load_sounds():
    """Returns {name: Sound}, e.g. sounds["shoot_fire"].play()."""
    sounds = {}
    sdir = os.path.join(ROOT, "sounds")
    for f in os.listdir(sdir):
        if f.endswith(".ogg"):
            sounds[os.path.splitext(f)[0]] = pygame.mixer.Sound(os.path.join(sdir, f))
    return sounds


def play_music(volume=0.4):
    pygame.mixer.music.load(os.path.join(ROOT, "music", "theme.ogg"))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
'''


def contact_sheet(sprites):
    order = [k for k in sprites if k[0] in ("towers", "enemies", "tiles", "ui")] + \
            [k for k in sprites if k[0] == "fx"]
    cell, cols = 84, 9
    rows = math.ceil(len(order) / cols)
    sheet = Image.new("RGBA", (cols * cell, rows * cell), (34, 38, 50, 255))
    for i, k in enumerate(order):
        im = sprites[k]
        x, y = (i % cols) * cell + (cell - im.width) // 2, (i // cols) * cell + (cell - im.height) // 2
        sheet.alpha_composite(im, (x, y))
    sheet.save(os.path.join(os.path.dirname(OUT), "contact_sheet.png"))


if __name__ == "__main__":
    sprites = make_images()
    make_sounds()
    make_music()
    with open(os.path.join(os.path.dirname(OUT), "assets.py"), "w") as f:
        f.write(LOADER)
    contact_sheet(sprites)
    print("done")
