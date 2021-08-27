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
import os,webbrowser
import sys
# for android -----------------
# from android.permissions import request_permissions, Permission
# from android.storage import primary_external_storage_path
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
        download_dir_path = os.path.join(dir, 'Download')
        addr = download_dir_path + "/scores.json"
        pass
    else:
        a = sys.path[0]
        addr = a + '/scores.json'
    return addr
class MainWindow(Screen):
    pass
class SecondWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initialisation of values in the game--------
        store = JsonStore(addr)
        config = GameConfig()
        config.STATE = 'PAUSED' #type: ignore
        config.STORE = store  #type:ignore
        if store.exists("HIGH_SCORE"):
            scores = store.get('HIGH_SCORE')
            config.HIGH_SCORE = scores['HIGH_SCORE']
        else:
            store['HIGH_SCORE'] = {"HIGH_SCORE":1000}
            config.HIGH_SCORE = 1000 #type:ignore
        # ---------------------------------
        boxLayout  = BoxLayout()
        boxLayout.orientation = "vertical"
        label =  ScoreLabel()
        label.highScore = config.HIGH_SCORE #type:ignore
        boxLayout.add_widget(label)
        game = GameWidget(label,config)
        boxLayout.add_widget(game)
        game.size_hint = (1,.85)
        label.size_hint = (1,.15)
        self.add_widget(boxLayout)
class WindowManager(ScreenManager):
    pass 

class SnakeApp(App):
    def build(self):
        global addr
        addr = getAddr()
        kv = Builder.load_file("main.kv")
        return kv

if __name__ == "__main__":
    app = SnakeApp()
    app.run()