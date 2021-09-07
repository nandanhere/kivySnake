
class GameConfig:
    DEFAULT_SIZE = (50,50)
    FOOD_SIZE = (60,60)
    MARGIN = 4
    DEAD_CELL = (1,0,0,1)
    DIFFICULTY = "EASY"
    DLIST = ['EASY','MEDIUM','HARD']
    RESET_COUNT = 3
    CHANCES = 5
    FOOD_AMT = 10
    HIGH_SCORE = 0
    STATE = "PAUSED"
    CONTROLS = "CLOCKWISE"
    STORE = None
    SOUND = 'ON'
    def __init__(self) -> None:
        pass

# NOTE THE STATES:
# PAUSE,PLAY, DEAD, EASTEREGG