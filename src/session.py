import random

# Lena - 11/6/2026
# This class manages the game sessions
class Session:
    def __init__(self):
        self.players = []
        self.minigames = [] #list with random order of event games
        self.server = ""
        self.difficulty = 1
        self.roundNumber = 0
        self.single = False
        # Trey - 11/6/2026
        # Names of every minigame that can be selected for a section
        self.minigame_names = ["RPS", "Reaction", "Maze", "Simon", "DDR", "Minesweeper", "Pizza"]

    # Add players to the session
    def addPlayer(self, player):
        self.players.append(player)

    # Start a new session
    def start(self):
        self.roundNumber = 1
        if (len(self.players) == 1):
            self.single = True

    def isSingle(self):
        return self.single

    # Advance to the next round
    def nextRound(self):
        if self.currentRound < 6:
            self.currentRound += 1
        else:
            self.isOver()

    # Check whether the session has finished
    def isOver(self):
        return self.currentRound >= 6

    # Trey - 11/6/2026
    # Randomly select the minigame for the current section and return its name
    def pickMinigame(self):
        if not self.minigames:
            self.minigames = random.sample(self.minigame_names, len(self.minigame_names))
        return self.minigames.pop()
