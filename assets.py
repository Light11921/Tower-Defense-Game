import os

import pygame

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def load_images():
    """Call after pygame.display.set_mode(). Returns {name: Surface}, e.g. images["cannon"]."""
    images = {}
    for folder, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".png"):
                name = os.path.splitext(f)[0]
                if os.path.basename(folder) == "ui":
                    name = "ui_" + name  #ui_coin,UI_haert and all the icons
                path = os.path.join(folder, f)
                images[name] = pygame.image.load(path).convert_alpha()
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
