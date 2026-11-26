import pygame
import main

class Territory:
    def __init__(self,center_tile,radius,cols,rows):
        cx,cy = center_tile#dimension of the central tower in terms of tiles 30x30--for one tile
        self.cols,self.rows = cols,rows #size of the rows and colums in tiles 960/60 
        self.rx,self.ry = radius#rx is for the x axis and ry is for the y-axis well the screen is a rectangle with an ratio 16:9 so i intent to make the barrier to be a recatngle as well
        self.left,self.top = cx - self.rx,cy - self.ry#left-- -x direction top-- +y direction
        self.right,self.bottom = cx + self.rx,cy + self.ry#right-- +x direction bottom-- -y direction
        self._clamp()

    def _clamp(self):
        self.left = max(self.left,0)
        self.top = max(self.top,0)
        self.right = min(self.right,self.cols -1)
        self.bottom = min(self.bottom,self.rows -1) 

    def contains(self,col,row):
        return self.left <= col <= self.right and self.top <= row <= self.bottom

    def expand(self,rx,ry = (1,1)):#this rx and ry are diff they are the x and y that will add according to the players need
        self.top -= rx
        self.left -= ry
        self.bottom += rx
        self.right += ry
        self._clamp()

    def is_full(self):
        return (self.left == 0 and self.top == 0
                    and self.right == self.cols -1 and self.bottom == self.rows -1)

    def pixel_rect(self,titles):
        return (self.left*titles,self.top*titles,(self.right- self.left +1)*titles,(self.bottom - self.top +1)*titles)




