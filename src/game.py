import pygame
from screens import *
from session import Session
import random

#Nickan Safi 11/6/2026
#Added handling for results

#Trey Timko - 11/6/2026
#Maps each minigame name from Session.pickMinigame() to a class
minigame_classes = {}

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

        #This dictionary stores all of the screens we can switch between
        self.screens = {
            "t1": TestScreen1(self),
            "t2": TestScreen2(self)
        }

        #Set the starting screen
        self.current = self.screens["t1"]
        self.running = True

    #This method is used to switch between different screens
    def switchScreen(self, name):
        self.current = self.screens[name]

    #Trey Timko - 11/6/2026
    #function that takes the selected minigame and starts it
    def startMinigame(self):
        name = self.session.pickMinigame()
        minigameClass = minigame_classes[name]
        minigame = minigameClass(self, self.session.difficulty, random.randint(0, 99999))
        self.screens["minigame"] = minigame
        self.switchScreen("minigame")

    #This method runs the main game loop
    def run(self):
        while self.running:
            #Set the game to run at 60 FPS 
            dt = self.clock.tick(60) / 1000

            #Iterate over all the events we need to process
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current.handleEvent(event)

            #Update the current screen
            self.current.update(dt)

            #Draw the current screen
            self.current.draw(self.surface)
            pygame.display.flip()

        pygame.quit()

    def handle(result_a, result_b, player_a, player_b):
        #Nickan Safi 11/6/2026
        if result_a < result_b:
            player_a.loseLife()
        if result_b < result_a:
            player_b.loseLife()
        if result_b == result_a:
            pass