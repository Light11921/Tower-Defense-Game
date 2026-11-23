import pygame
import waves



class FastEnemy(waves.Enemy):
    def __init__(self, waypoints):
        super().__init__(waypoints, speed = 3.5, hp = 60,hp_m=60, radius = 8, color = (225,220,50))












