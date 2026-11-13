import pygame
import math
from gameinfo import GameInfo
from network import getIP
from network import Client

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

# Simple minigame selector for testing individual games
class TestScreen1(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.titleFont = pygame.font.Font(None, 56)
        self.buttonFont = pygame.font.Font(None, 36)

        self.minigameNames = ["RPS", "Maze"]
        # Create one button for each registered minigame
        self.buttons = {}
        for i, name in enumerate(self.minigameNames):
            self.buttons[name] = pygame.Rect(250, 120 + i * 70, 300, 55)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for name, button in self.buttons.items():
                if button.collidepoint(event.pos):
                    self.game.startMinigame(name)

    def draw(self, surface):
        surface.fill((30, 30, 50))

        title = self.titleFont.render(
            "Select a Minigame", True, (255, 255, 255)
        )
        surface.blit(title, title.get_rect(center=(400, 65)))

        for name, button in self.buttons.items():
            pygame.draw.rect(surface, (50, 100, 200), button)

            text = self.buttonFont.render(
                name, True, (255, 255, 255)
            )
            surface.blit(text, text.get_rect(center=button.center))



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

        self.singleButton = pygame.Rect(250, 120, 300, 70)
        self.hostButton = pygame.Rect(250, 210, 300, 70)
        self.joinButton = pygame.Rect(250, 300, 300, 70)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.singleButton.collidepoint(event.pos):
                self.startGameCallback("single_player")

            elif self.hostButton.collidepoint(event.pos):
                self.startGameCallback("host")

            elif self.joinButton.collidepoint(event.pos):
                self.game.switchScreen("join")

    def draw(self, surface):
        surface.fill((30, 30, 50))

        title = self.titleFont.render(
            "Jackbox Ripoff", True, (255, 255, 255)
        )
        surface.blit(title, (250, 50))

        pygame.draw.rect(surface, (50, 100, 200), self.singleButton)
        pygame.draw.rect(surface, (50, 100, 200), self.hostButton)
        pygame.draw.rect(surface, (50, 100, 200), self.joinButton)

        singleText = self.buttonFont.render(
            "Single Player", True, (255, 255, 255)
        )
        hostText = self.buttonFont.render(
            "Host Game", True, (255, 255, 255)
        )
        joinText = self.buttonFont.render(
            "Join Game", True, (255, 255, 255)
        )

        surface.blit(singleText, (300, 140))
        surface.blit(hostText, (320, 230))
        surface.blit(joinText, (320, 320))



#John Platkowski - 11/8/2026
#Shows the selected minigame's instructions and counts down before it starts
class InstructionScreen(Screen):
    def __init__(self, game, minigame):
        super().__init__(game)
        self.minigame = minigame
        self.timeLeft = 5
        self.titleFont = pygame.font.Font(None, 64)
        self.textFont = pygame.font.Font(None, 32)

    def update(self, dt):
        self.timeLeft -= dt
        if self.timeLeft <= 0:
            self.minigame.start()
            self.switchScreen("minigame")

    def draw(self, surface):
        surface.fill((30, 30, 50))
        title = self.titleFont.render(self.minigame.title, True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(400, 80)))

        y = 160
        for line in self.minigame.instructions.split("\n"):
            text = self.textFont.render(line, True, (255, 255, 255))
            surface.blit(text, text.get_rect(center=(400, y)))
            y += 35

        countdown = self.titleFont.render("Starting in " + str(math.ceil(self.timeLeft)), True, (255, 220, 0))
        surface.blit(countdown, countdown.get_rect(center=(400, 320)))


#John Platkowski - 11/8/2026
#Waits for the other player to join the online session this player created
class HostScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 48)
        self.sID = getIP()

    def update(self, dt):
        if self.game.session.server.accept():
            self.switchScreen("t2")

    def draw(self, surface):
        surface.fill((30, 30, 50))
        text = self.font.render("Waiting for an opponent...", True, (255, 255, 255))
        surface.blit(text, text.get_rect(center=(400, 200)))

        #Trey - 11/13/2026
        #show the id text
        idText = self.font.render("Session ID: " + self.sID, True, (255, 255, 255))
        surface.blit(idText, idText.get_rect(center=(400, 260)))

#Trey - 11/13/2026
#Screen to handle joining an online session
class JoinScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 48)
        self.sessionID = ""
        self.error = ""

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.sessionID = self.sessionID[:-1]
                self.error = ""
            elif event.key == pygame.K_RETURN:
                client = Client(self.sessionID)
                if client.connect():
                    self.game.session.client = client
                    self.switchScreen("t2")
                else:
                    self.error = "Connection failed"
            elif event.unicode in "0123456789.":
                self.sessionID += event.unicode
                self.error= ""

    def draw(self, surface):
        surface.fill((30, 30, 50))

        prompt = self.font.render("Enter session ID:", True, (255, 255, 255))
        surface.blit(prompt, prompt.get_rect(center=(400, 160)))
        typed = self.font.render(self.sessionID, True, (255, 255, 255))
        surface.blit(typed, typed.get_rect(center=(400, 220)))
        if self.error != "":
            errorText = self.font.render(self.error, True, (255, 80, 80))
            surface.blit(errorText, errorText.get_rect(center=(400, 280)))
