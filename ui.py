import pygame
import config

#config,height,width are the diesion of the screen of the game window
#backimage is the grass image in in the samller scale usign transform and scale function we have changed
#back is the scale of the screen we have to use the image to decoreate 
#blit changes the backgournd in the backgroudn the two for loops help in it the paramter of the blit function
#is the per unit background at what coordinate we have to repalce it 

def background_maker(bac_image,width,height,tiles):
    unit_back = pygame.transform.scale(bac_image,(tiles,tiles))#scallling the image
    
    back = pygame.Surface((width,height))#defining where we have to scale aply the bckgournd
    
    for x in range(0,width,tiles):
        for y in range(0,height,tiles):
            back.blit(unit_back,(x,y))
    return back #it return the whole background at once i have to only return the funvtion in the main file       

#i want to create a path dialgonal and vertaicl ones where the enemy can follow and gather and after a certain area they can move freely and target the nearest tower

#today i have complate the background and wayoints where the enmey would allign and move towards the tower 

def path_maker_horizontl(path_image,width,height,tiles):
    unit_back = pygame.transform.scale(path_image,(tiles,tiles))

    path = pygame.Surface((width,height),pygame.SRCALPHA)

    for x in range(200,width,30):
        for y in range(0,height,30):
            path.blit(unit_back,(x,y))
    return path












