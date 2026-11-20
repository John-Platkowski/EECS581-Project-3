import pygame
from screens import *
from session import Session
from rps import RPS
from maze import Maze
from reaction import Reaction
from minesweeper import Minesweeper
from pizzacutting import PizzaCutting
from simon import Simon
import random

#Nickan Safi 11/6/2026
#Added handling for results

    
#Trey Timko - 11/6/2026
#Maps each minigame name from Session.pickMinigame() to a class
#Jack Larson 11/20/2026
#Removed duplication of this map



#Tyler Oswald - 11/5/2026
#This class controls the main game loop
class Game:
    def __init__(self):
        pygame.init()
        #Create the main game window 
        self.surface = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()


        #Starts a new single player/multiplayer session
        self.session = Session()
        self.roundFinished = False

        #pause before processing next minigame
        self.roundDelay = 0
        self.nextMinigame = None
        self.nextSeed = None

        #This dictionary stores all of the screens we can switch between
        self.screens = {
            "menu": MainMenu(self, self.startGame),
            "t1": TestScreen1(self),
            "t2": TestScreen2(self),
            "host": HostScreen(self),
            "transition": TransitionScreen(self),
            "join": JoinScreen(self),
        }
        self.current = self.screens["menu"]
        self.running = True

    def switchScreen(self, screenName):
        self.current = self.screens[screenName]

    # Switches between the different screens with a transition that displays the game name and current round
    def startTransition(self, game_name, round_number, next_screen):
        transition = self.screens["transition"]

        transition.on_enter(game_name, round_number, next_screen)
        self.switchScreen("transition")

    #this starts a game
    def startGame(self, gameMode):
        self.session.setGameMode(gameMode)
        self.session.start()
        if gameMode == "single_player":
            self.switchScreen("t1")
        else:
            #John Platkowski - 11/8/2026
            #Open a server and wait for the other player before continuing
            self.session.host()
            self.switchScreen("host")
        
    #Trey Timko - 11/6/2026 & Joshua - 11/19/2026
    #function that takes the selected minigame and starts it
    def startMinigame(self, name=None, seed = None):
        if name is None:
            name = self.session.pickMinigame()

        if seed is None:
            seed = random.randint(0, 99999)

        minigameClass = self.session.minigame_classes[name]
        minigame = minigameClass(self, self.session.difficulty, seed)
        self.screens["minigame"] = minigame

        self.roundFinished = False

        #Jack Larson - 11/20/2026
        #Interjects the round status screen
        self.screens["results"] = ResultsScreen(self, minigame)
        self.switchScreen("results")


        #John Platkowski - 11/8/2026
        #Show the instructions and countdown first, which then switches to the minigame
        self.screens["instructions"] = InstructionScreen(self, minigame)
        
        #self.switchScreen("instructions")

    def startHostMinigame(self):
        name = self.session.pickMinigame()
        seed = random.randint(0, 99999)

        self.session.send({
            "type": "next_minigame",
            "name": name,
            "seed": seed,
            "round": self.session.roundNumber
        })

        self.startMinigame(name, seed)

    #this schedules the next minigame
    def scheduleNextMinigame(self, name=None, seed=None):
        self.nextMinigame = name
        self.nextSeed = seed
        self.roundDelay = 3

    def updateRoundDelay(self, dt):
        if self.roundDelay <= 0:
            return

        self.roundDelay -= dt

        if self.roundDelay <= 0:
            self.roundDelay = 0

            name = self.nextMinigame
            seed = self.nextSeed

            self.nextMinigame = None
            self.nextSeed = None

            self.startMinigame(name, seed)
            self.roundFinished = False

    # Joshua - 11/19/2026
    # Handles progression after a minigame finishes
    def finishRound(self):
        if self.roundFinished:
            return

        if self.session.isSingle():
            self.roundFinished = True

            if not self.session.nextRound():
                self.switchScreen("menu")
                return

            self.scheduleNextMinigame()
            return

        if not self.session.isHost:
            return

        if not self.session.hasAllResults():
            return

        self.roundFinished = True
        results = self.session.pendingResults

        if not self.session.processResults(results[0], results[1]):
            self.session.clearResults()
            self.session.send({"type": "game_over"})
            self.switchScreen("menu")
            return

        self.session.clearResults()

        minigameName = self.session.pickMinigame()
        seed = random.randint(0, 99999)

        self.session.send({
            "type": "next_minigame",
            "name": minigameName,
            "seed": seed,
            "round": self.session.roundNumber
        })

        self.scheduleNextMinigame(minigameName, seed)

    def run(self):
        while self.running:
            # Set the game to run at 60 FPS
            dt = self.clock.tick(60) / 1000

            # Iterate over all the events we need to process
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current.handleEvent(event)

            # Handle incoming network messages
            if self.session.connection:
                for message in self.session.connection.getMessages():
                    if message["type"] == "next_minigame":
                        self.session.roundNumber = message["round"]

                        if message["round"] == 1:
                            self.startMinigame(message["name"], message["seed"])
                        else:
                            self.scheduleNextMinigame(message["name"], message["seed"])

                    elif message["type"] == "result":
                        self.session.recordResult(message["player"], message["value"])

                    elif message["type"] == "set_lives":
                        self.session.setLives(message["player"], message["value"])

                    else:
                        self.current.handleNetMessage(message)

            # Update the current screen
            self.current.update(dt)

            # Check whether the current minigame has finished
            if self.current == self.screens.get("minigame"):
                if self.current.finished:
                    self.finishRound()

            self.updateRoundDelay(dt)

            # Draw the current screen
            self.current.draw(self.surface)
            pygame.display.flip()

        pygame.quit()
