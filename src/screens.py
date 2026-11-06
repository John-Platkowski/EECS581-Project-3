import pygame

#Tyler Oswald - 11/5/2026
#This is a base class that other screens can inherit from
class Screen:
    def __init__(self, game):
        self.game = game

    #This function can be called to switch to a new screen
    def switchScreen(self, screenName):
        self.game.switchScreen(screenName)

    #These methods should be overridden in the child class
    def handleEvent(self, event): 
        pass
    def update(self, dt): 
        pass
    def draw(self, surface): 
        pass


#These two test classes were just used to make sure that screen switching works
#Feel free to delete them or repurpose them into actual screens
class TestScreen1(Screen):
    def handleEvent(self, event):
        #Pressing any key changes to the other test screen
        if event.type == pygame.KEYDOWN:
            self.switchScreen("t2")

    def draw(self, surface):
        surface.fill((255, 0, 0))


class TestScreen2(Screen):
    #Pressing any key changes to the other test screen
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.switchScreen("t1")

    def draw(self, surface):
        surface.fill((0, 0, 255))

#Prologue Comment
#Module: screens.py
#Description: Implements the main menu screen, allowing players to
#             select between single-player and online multiplayer.
#Input: Pygame mouse events and the game start callback.
#Output: Displays the main menu and communicates the selected game mode.
#
#Authors:
#   Joshua Lin
#Creation Date:
#   November 6, 2026
class MainMenu(Screen):
    def __init__(self, game, startGameCallback):
        self.game = game
        self.startGameCallback = startGameCallback
        self.titleFont = pygame.font.Font(None, 64)
        self.buttonFont = pygame.font.Font(None, 40)

        self.singleButton = pygame.Rect(250, 150, 300, 70)
        self.onlineButton = pygame.Rect(250, 250, 300, 70)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.singleButton.collidepoint(event.pos):
                self.startGameCallback("single_player")

            elif self.onlineButton.collidepoint(event.pos):
                self.startGameCallback("online_1v1")

    def draw(self, surface):
        surface.fill((30, 30, 50))

        title = self.titleFont.render(
            "Jackbox Ripoff", True, (255, 255, 255)
        )
        surface.blit(title, (250, 50))

        pygame.draw.rect(surface, (50, 100, 200), self.singleButton)
        pygame.draw.rect(surface, (50, 100, 200), self.onlineButton)

        singleText = self.buttonFont.render(
            "Single Player", True, (255, 255, 255)
        )
        onlineText = self.buttonFont.render(
            "Online 1v1", True, (255, 255, 255)
        )

        surface.blit(singleText, (300, 170))
        surface.blit(onlineText, (320, 270))