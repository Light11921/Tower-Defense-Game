import config
import pygame

#here view_w,view_h are the dimesions of the game visble on the window currently
#-- world_w,world_h are the dimesins of the whole game where everthing is build 

class Camera :
    def __init__(self,view_w,view_h,world_w,world_h,zoom_min = 0.5,zoom_max = 2.0):
        self.view_w,self.view_h = view_w,view_h
        self.world_w,self.world_h = world_w,world_h

        #the smaller the value bigger the zoom --zoomout then the number should be less then 1 and btw 0
        #zoomin the value should be gretoer than one 
        self.min_zoom = max(zoom_min,view_w/world_w,view_h/world_h)#it will chose the max btw the ratio and the defalut zoom_min

        self.zoom_max = zoom_max
        self.zoom = max(1.0,self.min_zoom)
        
        self.x = (world_w - view_w/self.zoom)/2
        self.y = (world_h - view_h/self.zoom)/2
     
        self.dragging = False#to trigger if the user is graggint he screen
        self.pan_speed = 700#the number of pixles the screen will move when someone drag the scrren ar the window

    def world_screen(self,wx,wy):
        return (wx - self.x) * self.zoom,(wy - self.y) * self.zoom

    def screen_world(self,sx,sy):
        return sx/self.zoom + self.x,sy/self.zoom +self.y
  
    def clamp(self):
        max_x = self.world_w - self.view_w/self.zoom
        max_y = self.world_h - self.view_h/self.zoom

        self.x = min(max(self.x,0),max_x)
        self.y = min(max(self.y,0),max_y)

    def zoom_at(self,screen_pos,factor):

        sx,sy = screen_pos
        wx,wy = self.screen_world(sx,sy)
        self.zoom = min(max(self.zoom*factor,self.min_zoom),self.zoom_max)

        self.x = wx -sx/self.zoom
        self.y = wy - sy/self.zoom
        self.clamp()

    def pan(self,dx_screen,dy_screen):

        self.x -= dx_screen/self.zoom
        self.y -= dy_screen/self.zoom
        self.clamp()

    def handle_event(self, e):
        if e.type == pygame.MOUSEWHEEL:
            self.zoom_at(pygame.mouse.get_pos(), 1.1 ** e.y)
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button in (2,3):
            self.dragging = True
        elif e.type == pygame.MOUSEBUTTONUP and e.button in (2,3):
            self.dragging = False
        elif e.type == pygame.MOUSEMOTION and self.dragging:
            self.pan(*e.rel) 

    def update(self,dt):
        keys = pygame.key.get_pressed()
        step = self.pan_speed*dt
        
        dx = (keys[pygame.K_LEFT] or keys[pygame.K_a]) - (keys[pygame.K_RIGHT] or keys[pygame.K_d])
        dy = (keys[pygame.K_UP] or keys[pygame.K_w]) - (keys[pygame.K_DOWN] or keys[pygame.K_s])

        if dx or dy :
            self.pan(dx*step,dy*step)         

            