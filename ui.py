import pygame
import assets
import math
import random
#config,height,width are the diesion of the screen of the game window
#backimage is the grass image in in the samller scale usign transform and scale function we have changed
#back is the scale of the screen we have to use the image to decoreate 
#blit changes the backgournd in the backgroudn the two for loops help in it the paramter of the blit function
#is the per unit background at what coordinate we have to repalce it 

def draw_background(cam,screen,world_surface):
    world_rect = world_surface.get_rect()

    view = pygame.Rect(int(cam.x),int(cam.y),math.ceil(cam.view_w/cam.zoom) + 2, math.ceil(cam.view_h/cam.zoom) + 2).clip(world_rect)
    
    piece = world_surface.subsurface(view)
    size = (math.ceil(view.w * cam.zoom),math.ceil(view.h*cam.zoom)) 
    scaled = pygame.transform.scale(piece,size)
    screen.blit(scaled,((view.x - cam.x) * cam.zoom,(view.y - cam.y) * cam.zoom))   

def draw_sprite(cam,screen,image,world_pos):

    w = max(1,round(image.get_width()*cam.zoom))
    h = max(1,round(image.get_height()*cam.zoom))

    scaled = pygame.transform.scale(image,(w,h))
    sx,sy = cam.world_screen(*world_pos)
    screen.blit(scaled,(sx -w/2,sy - h/2))

def build_world(images,world_w,world_h,titles,waypoints = 1):
    grass = pygame.transform.scale(images["grass1"],(titles,titles))
    world = pygame.Surface((world_w,world_h))
    for x in (0,world_w,titles):
        for y in (0,world_h,titles):
            world.blit(grass,(x,y))

    grass2 = pygame.transform.scale(images["grass2"],(titles,titles))
    for _ in range((world_w//titles)*(world_h//titles)//2):
        world.blit(grass2,(random.randrange(0,world_w,titles),random.randrange(0,world_h,titles)))

    base = pygame.transform.scale(images["arcane"],(titles,titles))
    world.blit(base,base.get_rect(center = (world_w//2,world_h//2)))
    return world
