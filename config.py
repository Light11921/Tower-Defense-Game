import pygame 
import math
import random

screen_width = 960
screen_height = 540
FPS = 60
tiles = 30 # -- It is the sall block which divided the eniter screen in block of dimension 30x30 for now it is for grasses 

#i make another wavepoint for diff enemries as it feels better
#from this the enmery just go thriugh the exact point and to reach the other point they walk in the straight line


SPAWN_REGIONS = [
    [(0, 200),   (0, 150)],     # top-left corner
    [(760, 959), (0, 150)],     # top-right corner
    [(0, 200),   (390, 539)],   # bottom-left corner
    [(760, 959), (390, 539)],   # bottom-right corner
    [(380, 580), (0, 40)],      # top-middle strip
]

def region_decideer():
    ren_rag = random.choice(SPAWN_REGIONS)
    (x_min,x_max),(y_min,y_max) = ren_rag
    return random.randint(x_min,x_max), random.randint(y_min,y_max)


wavepoint = [
    (50,50), #spawn point
    (200,50), #point 1
    (200,screen_height//2), #point 2
    (screen_width//2,screen_height//2), #point 3
]

#name of the particaluar tower cost range damage dealt firerate damatype 
TOWERS = {
    "cannon": {"cost": 50, "range": 150, "damage": 10, "fire_rate": 1.0, "damage_type": "physical"},
    "fire":   {"cost": 75, "range": 120, "damage": 8,  "fire_rate": 1.5, "damage_type": "fire"},
    "ice":    {"cost": 75, "range": 130, "damage": 5,  "fire_rate": 1.2, "damage_type": "ice"},
    "arcane": {"cost": 150, "range": 160, "damage": 12, "fire_rate": 0.8, "damage_type": "true"},
}

#type of enemy there mx health speed and reward--after slying then how much coin you will get to purchase something 
ENEMIES = {
    "grunt": {"health": 50,  "speed": 80,  "reward": 10},
    "fast":  {"health": 30,  "speed": 140, "reward": 12},
    "tank":  {"health": 200, "speed": 45,  "reward": 25},
    "boss":  {"health": 800, "speed": 40,  "reward": 100},
}































