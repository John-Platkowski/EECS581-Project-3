from player import Player
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
        self.gameMode = ""

    # Add players to the session
    def addPlayer(self, player):
        self.players.append(player)

    # Start a new session
    def start(self):
        self.players = []
        self.roundNumber = 1

        player1 = Player()
        player1.userName = "Player 1"
        player1.userID = 0
        player1.lives = 3
        self.addPlayer(player1)

        if not self.single:
            player2 = Player()
            player2.userName = "Player 2"
            player2.userID = 1
            player2.lives = 3
            self.addPlayer(player2)

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

    # Set the selected game mode
    def setGameMode(self, gameMode):
        self.gameMode = gameMode
        self.single = (gameMode == "single_player")