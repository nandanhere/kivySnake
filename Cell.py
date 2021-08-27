from random import randint
from gameConfig import GameConfig
from kivy.uix.widget import Widget

class Cell(Widget):
    def __init__(self,pos=(0,0),size=(50,50),type='BODY',direction='none' ,**kwargs):
        super().__init__(**kwargs)
        self.size = size   # As you can see, we can change self.size which is "size" property of a rectangle
        self.pos = pos
        self.type = type
    def update(self,direction):
        for i in self.canvas.get_group('rectangle'): # type:ignore
            i.source = 'assets/{}.png'.format(direction)
    def respawnFood(self,minx,miny,maxx,maxy):
        diff = GameConfig.FOOD_SIZE[0] 
        self.pos = (randint(int(minx + diff),int(maxx - diff)),randint(int(miny + diff),int(maxy - diff)))

# NOTE THE TYPES OF CELLS:
# FOOD,TAINTED,BODY,BODY1,DEAD,DEAD1