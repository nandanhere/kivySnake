# kivySnake
### Snake game  made with Kivy and python
<hr>
This Repo can be used as an example for replacing pygame with kivy to make certain games. Since pygame does not currently support smartphones , and as Kivy uses OpenGL for graphics which is faster and better in contrast to the pygame engine.

## Features
- Sounds implemented with kivysound
- Store high scores with JsonStore
- Examples of using .kv files with the .py files for each class (some documentation needed here)

## Installation
- After cloning the repo, make sure you install kivy by running the following:  
    `pip install kivy` 
## Android installation:
[Click here to Go to a collab Link to convert your Kivy application to an android apk](https://colab.research.google.com/gist/kaustubhgupta/0d06ea84760f65888a2488bac9922c25/kivyapp-to-apk.ipynb#scrollTo=tLbircO10N0a)<br>
Since the Game stores high score information , you will require permissions to store and read data. Also, for sounds to work you will have to add ffpyplayer in the Build requirements in the .spec file, and wav in the included external file types list<br>
In the buildozer.spec file , add the following:

    requirements = python3,kivy,ffpyplayer
    #android.permissions = Permission.WRITE_EXTERNAL_STORAGE
    #android.permissions = Permission.READ_EXTERNAL_STORAGE
    source.include_exts = py,png,jpg,kv,atlas,wav
To prevent assets from causing problems try putting them in the same directory as main.py and change the addresses accordingly

## Using [Cross Platform Python GUI](https://github.com/maltfield/cross-platform-python-gui)
- Branch and Clone the repository to a folder
- In the src subdirectory, clear the folder and add all the kivysnake code including assets into it.
- Change all references of "helloWorld" in the build folder's files (in KivySnake's case we convert helloWorld to kivySnake in each and every file in [cross-platform-python-gui/build](https://github.com/maltfield/cross-platform-python-gui/tree/master/build) )
- Push to your branch. The workflows will generate the releases for each platform. (mac, linux and windows)
## To be done
- Main menu (to be done with kivymd to integrate material design)
<hr>

thanks to [@maltfield](https://github.com/maltfield) for the cppgui repo and kivy team for the platform