from player import Player
from network import Server
from rps import RPS
from maze import Maze
from reaction import Reaction
from minesweeper import Minesweeper
import random
from GameResult import GameResult

# Lena Palmieri - 11/6/2026

# This class manages the game sessions
class Session:
    def __init__(self):
        self.connection = None
        self.players = []
        self.minigames = [] #list with random order of event games
        self.server = ""
        self.difficulty = 1
        self.roundNumber = 0
        self.single = False
        self.gameMode = ""

        self.pendingResults = {}
        self.lastResults = {}
        self.isHost = False


        # Trey - 11/6/2026
        # Names of every minigame that can be selected for a section

        # Joshua - 11/19/2026
        #moved to be hash that is the list of classes. 
        self.minigame_classes = {
            "RPS": RPS,
            "Maze": Maze,
            "Reaction": Reaction,
            "Minesweeper": Minesweeper
        }

    # Add players to the session
    def addPlayer(self, player):
        self.players.append(player)

    # Start a new session
    def start(self):
        self.players = []
        self.roundNumber = 1
        self.minigames = []
        self.clearResults()

        player1 = Player("Player 1", 0, 3)
        self.addPlayer(player1)

        if not self.single:
            player2 = Player("Player 2", 1, 3)
            self.addPlayer(player2)

    def isSingle(self):
        return self.single

    # Advance to the next round
    def nextRound(self):
        if self.roundNumber < 6:
            self.roundNumber += 1
            return True
        
        return False

    # Check whether the session has finished
    def isOver(self):
        return self.roundNumber >= 6

    # Set the selected game mode
    def setGameMode(self, gameMode):
        self.gameMode = gameMode
        self.single = (gameMode == "single_player")

    # John Platkowski - 11/8/2026
    # Creates an online session by opening a server for the other player to join
    def host(self):
        self.server = Server()

    #Tyler Oswald - 11/13/2026
    #Sends a message to other player session
    def send(self, message):
        if self.connection:
            self.connection.send(message)

    # Trey - 11/6/2026 & joshua - 11/19/2026
    # Randomly select the minigame for the current section and return its name
    def pickMinigame(self):
        if not self.minigames:
            self.minigames = random.sample(
                list(self.minigame_classes.keys()),
                len(self.minigame_classes)
            )
        return self.minigames.pop()


    #Joshua & Nickan 11/19/2026
    #handles the results of a game
    def processResults(self, result_a, result_b):
        if result_a < result_b:
            self.players[0].loseLife()
        elif result_b < result_a:
            self.players[1].loseLife()

        #Jack Larson 11/20/2026 Networked lives
        self.send({
            "type": "set_lives",
            "player": 0,
            "value": self.players[0].lives
        })
        self.send({
            "type": "set_lives",
            "player": 1,
            "value": self.players[1].lives
        })

        if any(player.lives <= 0 for player in self.players):
            return False

        return self.nextRound()

    def recordResult(self, player, result):
        if isinstance(result, dict):
            result = GameResult(**result)
        self.pendingResults[player] = result
        self.lastResults[player] = result
        
    #Jack Larson 11/20/2026 Networked lives
    def setLives(self, player, lives):
        self.players[player].lives = lives

    def hasAllResults(self):
        return all(player in self.pendingResults for player in range(len(self.players)))

    def clearResults(self):
        self.pendingResults = {}