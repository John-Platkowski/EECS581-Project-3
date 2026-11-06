
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