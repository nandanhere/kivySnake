from gameConfig import GameConfig      
from Cell import Cell
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.audio import Sound, SoundLoader
from kivy.utils import platform

global maxx,maxy,minx,miny
sizee = Window.size #type:ignore
maxx ,maxy = sizee[0],sizee[1]
minx,miny = maxx * .1 , maxy * .1

# sounds
# requirements = python3,kivy,ffpyplayer - add in .spec


ateadonut = SoundLoader.load('assets/ateadonut.wav'); ateadonut.volume = 0.5        #type: ignore
atepoison = SoundLoader.load('assets/atepoison.wav');
startgame = SoundLoader.load('assets/startgame.wav'); startgame.volume = 0.5        #type: ignore
died = SoundLoader.load('assets/died.wav'); died.volume =  0.5                      #type: ignore
gotahighscore = SoundLoader.load('assets/gotahighscore.wav')
oneup = SoundLoader.load('assets/oneup.wav')

kv = Builder.load_file('GameWidget.kv')
class GameWidget(Widget):
    def __init__(self,labelWidget,config,**kwargs):
        super().__init__(**kwargs)
        global label
        label = labelWidget
# keyboard controls----------
        if platform == 'android':
            self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self) #type:ignore
            self._keyboard.bind(on_key_down=self._on_key_down,) #type:ignore
#  keyboard controls
        self.config = config
        self.head = Cell(pos=(maxx // 2,maxy / 2),size=GameConfig.DEFAULT_SIZE)
        self.head.update('up')
        self.add_widget(self.head)
        self.snakeList = []
        self.snakeList.append(self.head)
        self.foodList = []
        for i in range(GameConfig.FOOD_AMT):
            type = 'FOOD' if i < GameConfig.FOOD_AMT *.75  else 'TAINTED'
            food = Cell(size=GameConfig.FOOD_SIZE,type=type) #type:ignore
            food.respawnFood(minx,miny,maxx,maxy)
            self.add_widget(food)
            self.foodList.append(food)
        Clock.schedule_interval(self.move_step,0)
    
    def reset_game(self):
        hs = label.highScore
        self.clear_widgets()
        self.config.__init__()
        label.__init__()
        self.config.HIGH_SCORE = label.highScore = hs
        self.config.STATE = label.state = "PLAY"
        Clock.idle
        self.__init__(labelWidget=label,config=self.config)


    def increment_score(self):
        label.updateScore(label.score + 100)
        if label.score % 5000 == 0 : 
            self.config.CHANCES += 1
            label.chances += 1
            oneup.play()                                                                    #type: ignore
        if label.score > self.config.HIGH_SCORE:
                if self.config.STATE == label.state == 'PLAY': gotahighscore.play()         #type: ignore
                self.config.HIGH_SCORE = label.score
                label.highScore = label.score
                label.state = 'EASTEREGG'
                self.config.STORE['HIGH_SCORE'] = {"HIGH_SCORE":label.score}


    def on_touch_down(self, touch):
        global label
        if label.state == "PAUSED" or self.config.STATE == 'PAUSED':
            label.state = "PLAY"
            self.config.STATE = "PLAY"
            startgame.play()                                                                #type: ignore

        if label.state == "DEAD" or self.config.STATE == 'DEAD':
            self.config.RESET_COUNT -= 1

        directions = ['up','right','down','left','w','d','s','a','spacebar']
        ind = (directions.index(self.keyPressed) + 1) % 4
        self.keyPressed = directions[ind]
        self.head.update(self.keyPressed)
        self.speedup = True
    def on_touch_up(self, touch):
        self.speedup = False
# for keyboard Controls ---------------
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down) #type:ignore
        self._keyboard = None

    def _on_key_down(self,keyboard,keycode,text,modifiers):
        directions = ['up','right','down','left','w','d','s','a']
        if label.state == "PAUSED" or self.config.STATE == "PAUSED":
                label.state = "PLAY"
                self.config.STATE = "PLAY"
                startgame.play()                                                            #type: ignore

        if label.state == "DEAD":
            self.config.RESET_COUNT -= 1
        keyPressed = keycode[1]
        if keyPressed in directions:
            ind = (directions.index(keyPressed)) % 4
            self.keyPressed = directions[ind]
            self.head.update(self.keyPressed)
#DEBUG ---------- 
        elif keyPressed == "spacebar":
            self.keyPressed = keyPressed
# DEBUG------------
# ------------------------------

    def move_head(self,currentx,currenty,step_size):
        newx,newy = currentx,currenty
        direction = self.keyPressed
        if "up" == direction:
            a = ((step_size + newy) % maxy)
            newy =  a if a > miny else miny
        elif  "down" == direction :
            newy = (newy - step_size) % maxy if newy > miny else maxy
        elif 'left' == direction:
            newx = (newx - step_size) % maxx  
        elif 'right' == direction:
            newx = (step_size + newx) % maxx  
        # DEBUG ONLY------
        elif "spacebar" == direction:
            self.config.STATE = 'DEAD'
            label.state = "DEAD"
            for i in range(len(self.snakeList)):
                self.snakeList[i].type = "DEAD" if i % 2 == 0 else 'DEAD1'

        #DEBUG ONLY ------
        if len(self.snakeList) > 1:
            self.diff = max(abs(newx - self.snakeList[1].pos[0]), abs(newy - self.snakeList[1].pos[1]))
        self.head.pos = (newx,newy)
    def food_movement_and_collision(self,currentx,currenty):
        for food in self.foodList:
            if collides(self.head.pos,food.pos,self.snakeList[0].size,food.size):
                if food.type == 'TAINTED':
                    label.getHit()
                    atepoison.play()                                                        #type: ignore
                    if label.chances == 0:
                        self.config.STATE = 'DEAD'
                        label.state = "DEAD"
                        died.play()                                                         #type: ignore
                        for i in range(len(self.snakeList)):
                            self.snakeList[i].type = "DEAD" if i % 2 == 0 else 'DEAD1'
                else:
                    self.increment_score()
                    ateadonut.play()                                                        #type: ignore
                    type = "BODY" if len(self.snakeList) % 2 == 0 else 'BODY1'
                    sb = Cell(pos=(currentx,currenty),type=type) #type:ignore
                    self.snakeList.append(sb)
                    self.add_widget(sb)
                    if len(self.snakeList) % 5 == 0:
                        for i in range(int(self.config.FOOD_AMT *.75), self.config.FOOD_AMT):
                            self.foodList[i].respawnFood(minx,miny,maxx,maxy)
                food.respawnFood(minx,miny,maxx,maxy)

    def move_step(self,deltatime):
        global label,maxx,maxy,minx,miny
        if label.state == 'PAUSED' or self.config.STATE == 'PAUSED':return
        if self.config.STATE == 'DEAD':
            if self.config.RESET_COUNT == 0:
                self.config.RESET_COUNT = 3
                self.reset_game()
                #  the false here tells the scheduled clock to stop executing the move_step function.
                return False
            else: return
        if self.diff > 40:
            for i in range(len(self.snakeList) - 1 ,0 ,-1):
                self.snakeList[i].pos = self.snakeList[i - 1].pos
        sizee = Window.size #type:ignore
        maxx ,maxy = sizee[0],sizee[1]
        minx,miny = .15 * maxx,.15 * maxy
        step_size = 400 * deltatime if self.speedup else 200 * deltatime
        currentx = self.snakeList[0].pos[0]   
        currenty = self.snakeList[0].pos[1]
        self.move_head(currentx,currenty,step_size)
        self.food_movement_and_collision(currentx,currenty,)
        
def collides(pos1,pos2,size1,size2):
    # returns true if collide else false
    r1x,r1y = pos1[0],pos1[1]
    r2x,r2y = pos2[0],pos2[1]
    r1w,r1h = size1[0],size1[1]
    r2w,r2h = size2[0],size2[1]
    return (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y)
