import math 
import pygame
import random
import config

#i am thinking of moving it and writing in the character file as it is not realted to waves 
class Enemy:
    def __init__(self,waypoints,speed,hp,hp_m,radius,color):
        self.waypoints = waypoints #wavepoints is from the config file waypoints a list
        self.current_windex = 0
        self.x,self.y = waypoints[0]
        self.speed = speed
        self.speed = 2.0
        self.reached_end = False

        #unique stats for each enemy type i'll decide them later
        self.health = hp
        self.health_max = hp_m
        self.radius = radius 
        self.color = color
        

    #the  waypoints is the list in the config file it has the list of coordinates where the spawn 
    #enemy would move around the selfx,y are the current coordinates to reach 
    def update(self):#it is the fucntion to guide the enmey to the tower where it is placed according to the wave points defined
        if self.reached_end:
            return      

        target_x,target_y = self.waypoints[self.current_windex]
        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.hypot(dx,dy)

        if distance <  self.speed :
            self.x,self.y = target_x,target_y
            self.current_windex += 1
            if self.current_windex >= len(self.waypoints):
                self.reached_end = True

        else:
            self.x += (dx/distance)*self.speed
            self.y += (dy/distance)*self.speed

    def draw(self,surface):#the draw a tempory enemy for figuring out things i creates a cirlvcle which moves accors according to the wavepoints instructed +
        pygame.draw.circle(surface,self.color,((int(self.x)),(int(self.y))),self.radius)

class FastEnemy(Enemy):
    def __init__(self, waypoints):
        super().__init__(waypoints, speed = 3.5, hp = 60,hp_m=60, radius = 8, color = (225,220,50))      

class Spawner:
    def __init__(self):
        self.wave = 0
        self
        




        