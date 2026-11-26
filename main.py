import pygame
import assets
import config
import camera
import ui
import territory

class Game():
    def __init__(self):
        #all the value should be used from here only as it will be easy and checking scenerio 
        self.width = config.screen_width#width of the screen
        self.height = config.screen_height#height of the screen
        self.ac_width = config.width_act#actul world wdith 
        self.ac_height = config.height_act#actual world height
        self.fps = config.FPS#fps for the game
        self.tiles = config.tiles#per unit block for the game so to divided it properly

        pygame.init()
        self.running = True#all the events work when it is trure and when its is false then the game stops
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()#maintain the frame rate trough out the game and also use to decide the enemeis movement it return the time in milisec so divided it by 1000
        self.image = assets.load_images()#list of all the imgaes just use it like slef.images['name of the file']
        
        self.cam = camera.Camera(self.width,self.height,self.ac_width,self.ac_height)#camera function to control zoming and movng the screen
        
        self.world_bg = ui.build_world(self.image,self.ac_width,self.ac_height,self.tiles)#world backgound the green pathes of land
        

        cols = self.ac_width//self.tiles#it is dividing the whole in column so 960/60 which is wider 
        rows = self.ac_height//self.tiles#it is dividing the whole in row hr-- horizontal rows 
        castle_tile = (cols//2,rows//2)#the location at which the main base will be located but in terms of the gird 
        self.land = territory.Territory(castle_tile,(16,9),cols,rows)

        self.overlay = ui.make_overlay(self.image["build_bad"],self.land,self.ac_width,self.ac_height,self.tiles)


    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            self.cam.handle_event(e)

    def update(self,dt):
        self.cam.update(dt)

    def draw(self):
        self.screen.fill((0,0,0))
        ui.draw_background(self.cam,self.screen,self.world_bg)
        ui.draw_background(self.cam,self.screen,self.overlay)
        
        pygame.display.flip()

    def run(self):
        while self.running :
            dt = self.clock.tick(self.fps)/1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    Game().run()       
        
           
            





        