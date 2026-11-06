import pygame
from screens import *
from session import Session

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
            "menu": MainMenu(self, self.startGame),
            "t1": TestScreen1(self),
            "t2": TestScreen2(self)
        }
        self.current = self.screens["menu"]
        self.running = True

    #This method is used to switch between different screens
    def switchScreen(self, name):
        self.current = self.screens[name]

    #this starts a game
    def startGame(self, gameMode):
        self.session.setGameMode(gameMode)
        self.session.start()
        self.switchScreen("t1")
        
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
