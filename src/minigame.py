import pygame
from screens import Screen
from GameResult import GameResult

#Trey - 11/6/2026
#Base class for all minigames. set self.finished = True when the game ends.
class Minigame(Screen):
    #John Platkowski - 11/8/2026
    #Shown on the instruction screen before the minigame starts
    title = "Minigame"
    instructions = ""

    def __init__(self, game, difficulty, seed):
        super().__init__(game)
        self.difficulty = difficulty
        self.seed = seed
        self.result = GameResult()
        self.finished = False
        self.startTime = 0

    #a getter function for the result of the game
    def getResult(self):
        return self.result

    #John Platkowski - 11/8/2026
    #Called when the countdown ends and the minigame starts accepting input
    def start(self):
        self.startTime = pygame.time.get_ticks()

    #John Platkowski - 11/8/2026
    #Ends the minigame and player finish time, timed minigames should call this
    def finish(self, completed=True):
        self.finished = True
        self.result.completed = completed
        if completed:
            self.result.time = (pygame.time.get_ticks() - self.startTime) / 1000
