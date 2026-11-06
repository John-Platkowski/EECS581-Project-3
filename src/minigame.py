from screens import Screen
from GameResult import GameResult

#Trey - 11/6/2026
#Base class for all minigames. set self.finished = True when the game ends.
class Minigame(Screen):
    def __init__(self, game, difficulty, seed):
        super().__init__(game)
        self.difficulty = difficulty
        self.seed = seed
        self.result = GameResult()
        self.finished = False
    
    #a getter function for the result of the game
    def getResult(self):
        return self.result
