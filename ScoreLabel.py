from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
import webbrowser

class ScoreLabel(FloatLayout):
    def __init__(self,score=0,chances=5,**kwargs):
        super().__init__(**kwargs)
    def on_release(self):
        if self.state == 'EASTEREGG':#type:ignore
            webbrowser.open('https://github.com/nandanhere')
        if self.state == "PLAY":
            self.state = "PAUSED"




    def updateText(self):
        text = ""
        if self.state == "PLAY":
            text = "Score:{}\n [b]Chances[/b]:{}\n High Score : {}".format(self.score,self.chances,self.highScore) #type:ignore
        elif self.state == "DEAD":#type:ignore
            text = "YOU ARE DEAD!!!\n HIGH SCORE:{}".format(self.highScore)#type:ignore
        elif self.state == "EASTEREGG":#type:ignore
            text = "EASTER EGG!!!!\n High Score : {}".format(self.highScore) #type:ignore
        for child in self.children:
            child.text = text


    def updateScore(self,score):
        self.score = score
        self.updateText()
        
    def getHit(self,):
        self.chances -= 1
        if self.chances == 0:
            self.state = "DEAD"
        self.updateText()

    def reset(self):
        self.chances = 5
            