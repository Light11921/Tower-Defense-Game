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

        #money and wave update
        self.money = 1000
        self.wave_won = False
        self.expansion_mode = False#to start the expansion mode press e
        self.ex_number = 1000
        self.drag_side = None
        
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
            
            elif e.type == pygame.KEYDOWN:
                print("expansion mode:",self.expansion_mode)
                expansion_cost_TB = 50#expession cost for bottom and top 
                expansion_cost_RL = 30#expenssion cost for right and left  

                if e.key == pygame.K_e:
                    self.expansion_mode = not self.expansion_mode
                    #display an entry in the expansion mode
                elif self.expansion_mode:
                    sides = {pygame.K_1: "top",pygame.K_2:"bottom",pygame.K_3:"right",pygame.K_4:"left"}
                    chosen_side = sides.get(e.key) 

                    #will have to add a constarint of the expansion wiht money
                    if chosen_side:
                        amount = 5
                        tiles_gained = self.land.gain(chosen_side,amount)
                        print("gian:",tiles_gained,self.ex_number)
                        print("land l,t,r,b:", self.land.left,self.land.top,self.land.right,self.land.bottom,"i world cols,rowws",self.land.cols,self.land.rows)
                        if tiles_gained > 0 and self.ex_number >= tiles_gained:
                        
                            self.land.expand(chosen_side,amount)
                            self.ex_number -= tiles_gained    

                            self.overlay = ui.make_overlay(self.image["build_bad"],self.land,self.ac_width,self.ac_height,self.tiles)

                            self.expansion_mode = False
            
            self.cam.handle_event(e)


    def update(self,dt):
        self.cam.update(dt)

    def draw(self):
        self.screen.fill((0,0,0))
        ui.draw_background(self.cam,self.screen,self.world_bg)
        ui.draw_background(self.cam,self.screen,self.overlay)

        if hasattr(self,"selected_tile") and self.selected_tile:
            col,row = self.selected_tile
            ui.draw_tile_highlight(self.overlay,col,row,self.tiles,color = (225,225,0))
        
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
        
           
            





        