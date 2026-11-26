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
    for x in range(0,world_w,titles):
        for y in range(0,world_h,titles):
            world.blit(grass,(x,y))

    grass2 = pygame.transform.scale(images["grass2"],(titles,titles))
    for _ in range((world_w//titles)*(world_h//titles)//2):
        world.blit(grass2,(random.randrange(0,world_w,titles),random.randrange(0,world_h,titles)))

    base = pygame.transform.scale(images["base"],(titles*2,titles*2))
    world.blit(base,base.get_rect(center = (world_w//2,world_h//2))) 
   
    return world

def make_overlay(images,land,world_w,world_h,titles):
    overlay = pygame.Surface((world_w,world_h),pygame.SRCALPHA)
    overlay.fill((0,0,0,120))
    x,y,w,h = land.pixel_rect(titles)
    rect = pygame.Rect(land.pixel_rect(titles))
    overlay.fill((0,0,0,0),rect)

    piece = pygame.transform.scale(images,(titles,titles))
    side = pygame.transform.rotate(piece,90)

    for px in range(x,x+w,titles):
        overlay.blit(piece,(px,y))
        overlay.blit(piece,(px,y+h-titles))
    for py in range(y+titles,y+h-titles,titles):
        overlay.blit(side,(x,py))
        overlay.blit(side,(x + w -titles,py)) 

    return overlay       




