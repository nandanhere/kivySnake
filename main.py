__version__ = "1.0.1"
#todo : add some ui elements with kivymd for an example
import os,sys

from kivy import config
from kivy.core import window
os.environ["KIVY_TEXT"] = "pil"
from gameConfig import GameConfig
from GameWidget import GameWidget
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from ScoreLabel import ScoreLabel
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout

global gameConfig
gameConfig = None
# for android ----------
if platform == 'android':
    from android.permissions import request_permissions, Permission             #type: ignore
    from android.storage import primary_external_storage_path                   #type: ignore
    from android import loadingscreen                                           #type: ignore
    loadingscreen.hide_loading_screen()
# for android-------
global addr,store
addr = ""
def getAddr():
    global addr
    if platform == 'android':
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE])
        # remember to add to the build.spec file during the android build
            #android.permissions = Permission.WRITE_EXTERNAL_STORAGE
            #android.permissions = Permission.READ_EXTERNAL_STORAGE
        dir = primary_external_storage_path()
        download_dir_path = os.path.join(dir, 'Download')                           #type: ignore
        addr = download_dir_path + "/scores.json"
        pass
    else:
        # following code will check if there is a directory called .kivySnake in the HOME directory of the user. this is done so that when we package the app
        #  as a standalone executable, in case the app runs in read only mode, it wont be able to access any file inside itself/
        path = os.path.join( os.path.expanduser('~')) + "/.kivySnake"               #type: ignore
        if not os.path.isdir(path):                                                  #type: ignore
            os.makedirs(path)                                                         #type: ignore
        addr = path + "/scores.json"
    return addr
class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def goBack(self):
        curr = self.current
        if curr == 'options' or curr == 'game':
            gameConfig.STATE = "PAUSED"
            self.transition.direction = 'down' if self.transition.direction == 'up' else "left"
            self.current = 'main'
            return True
        else:
            return False
class Main(Screen):
    pass

class OptionsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.gameConfig = gameConfig
    def selectedControls(self,choice):
        currSettings = gameConfig.STORE["SETTINGS"]
        if choice == "CW":
            currSettings['CONTROLS'] = gameConfig.CONTROLS = "CLOCKWISE"
            self.ids.acwbutton.text_color = get_color_from_hex("#808080")
            self.ids.cwbutton.text_color = get_color_from_hex("#FFFFFF")

        elif choice == "ACW":
            currSettings['CONTROLS'] = gameConfig.CONTROLS = "ANTICLOCKWISE"
            self.ids.cwbutton.text_color = get_color_from_hex("#808080")
            self.ids.acwbutton.text_color = get_color_from_hex("#FFFFFF")
        gameConfig.STORE["SETTINGS"] = currSettings
    
  
class GameScreen(Screen):
    def __init__(self, **kwargs):
        global gameConfig
        super().__init__(**kwargs)
        boxLayout  = MDBoxLayout()
        boxLayout.md_bg_color = (0,0,0,1) 
        boxLayout.orientation = "vertical"
        label =  ScoreLabel()
        label.highScore = gameConfig.HIGH_SCORE #type:ignore
        boxLayout.add_widget(label)
        game = GameWidget(label,gameConfig)
        boxLayout.add_widget(game)
        game.size_hint = (1,.85)
        label.size_hint = (1,.15)
        self.add_widget(boxLayout)


class SnakeApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.Android_back_click)

    def build(self):
        global addr,gameConfig
        addr = getAddr()
        # initialisation of values in the game--------
        store = JsonStore(addr)
        gameConfig = GameConfig()
        gameConfig.STATE = 'PAUSED'                                                                              #type: ignore
        gameConfig.STORE = store                                                                                  #type:ignore
        if store.exists("HIGH_SCORE") and store.exists("SETTINGS"):
            scores = store.get('HIGH_SCORE')
            gameSettings = store.get('SETTINGS')
            gameConfig.HIGH_SCORE = scores['HIGH_SCORE']
            gameConfig.SOUND = gameSettings['SOUND']
            gameConfig.DIFFICULTY = gameSettings['DIFFICULTY']
            gameConfig.CONTROLS = gameSettings['CONTROLS']

        else:
            store['HIGH_SCORE'] = {"HIGH_SCORE":1000}
            store['SETTINGS'] = {'SOUND' : 'ON','DIFFICULTY':"EASY","CONTROLS":'CLOCKWISE'}
            gameConfig.CONTROLS = "CLOCKWISE"
            gameConfig.DIFFICULTY = "EASY"                                                                       #type:ignore
            gameConfig.HIGH_SCORE = 1000                                                                        #type:ignore
        # ---------------------------------

        self.kv = Builder.load_file("main.kv")
        return self.kv
    #todo : implement back button somehow
    def Android_back_click(self,Screen,key,*largs):
        if key == 27:
            print("back button pressed lol")
            value = self.kv.goBack()
            return value


if __name__ == "__main__":
    app = SnakeApp()
    app.run()