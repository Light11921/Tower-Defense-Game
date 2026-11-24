import pygame
import assets
import config
import camera
import ui


class Game():
    def __init__(self):
        self.width = config.screen_width
        self.height = config.screen_height
        self.ac_width = config.width_act
        self.ac_height = config.height_act
        self.fps = config.FPS
        self.tiles = config.tiles
       
        
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        self.image = assets.load_images()
        self.cam = camera.Camera(self.width,self.height,self.ac_width,self.ac_height)
        self.world_bg = ui.build_world(self.image,self.ac_width,self.ac_height,self.tiles)

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
        
           
            





        