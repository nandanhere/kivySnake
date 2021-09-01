__version__ = "1.0.0"
#todo : add some ui elements with kivymd for an example
#todo : fix initial crash on android due to permissions.
import os,sys
from random import randint
from gameConfig import GameConfig
from kivy.config import Config
from GameWidget import GameWidget
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from ScoreLabel import ScoreLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDIconButton
from kivy.uix.screenmanager import Screen, ScreenManager,FadeTransition
from kivymd.uix.boxlayout import MDBoxLayout


# for android ----------
if platform == 'android':
    from android.permissions import request_permissions, Permission             #type: ignore
    from android.storage import primary_external_storage_path                   #type: ignore
    from android import loadingscreen
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
class Main(Screen):
    pass
class OptionsScreen(Screen):
        pass
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initialisation of values in the game--------
        store = JsonStore(addr)
        config = GameConfig()
        config.STATE = 'PAUSED'                                                                              #type: ignore
        config.STORE = store                                                                                  #type:ignore
        if store.exists("HIGH_SCORE"):
            scores = store.get('HIGH_SCORE')
            config.HIGH_SCORE = scores['HIGH_SCORE']
        else:
            store['HIGH_SCORE'] = {"HIGH_SCORE":1000}
            config.HIGH_SCORE = 1000                                                                        #type:ignore
        # ---------------------------------
        boxLayout  = MDBoxLayout()
        boxLayout.md_bg_color = (0,0,0,1) 
        boxLayout.orientation = "vertical"
        label =  ScoreLabel()
        label.highScore = config.HIGH_SCORE #type:ignore
        boxLayout.add_widget(label)
        game = GameWidget(label,config)
        boxLayout.add_widget(game)
        game.size_hint = (1,.85)
        label.size_hint = (1,.15)
        self.add_widget(boxLayout)


class SnakeApp(MDApp):
    def build(self):
        global addr
        addr = getAddr()
        kv = Builder.load_file("main.kv")

        return kv

if __name__ == "__main__":
    app = SnakeApp()
    app.run()