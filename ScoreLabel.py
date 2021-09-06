import webbrowser
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

class ScoreLabel(FloatLayout):
    def __init__(self,score=0,chances=5,**kwargs):
        super().__init__(**kwargs)
    def on_release(self):
        if self.state == 'EASTEREGG':#type:ignore
            self.state = "PAUSED"
            webbrowser.open('https://www.youtube.com/watch?v=KMU0tzLwhbE')
        if self.state == "PLAY":
            self.state = "PAUSED"
    def updateText(self):
        text = ""
        if self.state == "HIGHSCORE":
            pass
        if self.state == "PLAY":
            text = "Score:{}\n [b]Chances[/b]:{}\n [i]High Score : {}[/i]".format(self.score,self.chances,self.highScore) #type:ignore
        elif self.state == "DEAD":#type:ignore
            text = "[b][color=#FF0000]YOU ARE DEAD!!!\n HIGH SCORE:{}[/color][/b]".format(self.highScore)#type:ignore
        elif self.state == "EASTEREGG":#type:ignore
            text = "[b][color=#00FF00]EASTER EGG!! CLICK ON ME[/b]!!!!\n High Score : {}[/color]".format(self.highScore) #type:ignore
        for child in self.children:
            child.text = text
            child.background_color = (0,0,0,1) if self.state == "DEAD" else (0,1,1,1) if self.state == "EASTEREGG" else child.background_color


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
            