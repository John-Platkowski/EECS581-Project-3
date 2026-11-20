import pygame
import math
from gameinfo import GameInfo
from network import getIP
from network import Client

#Nickan Safi 11/20/2026
#Change text depending on whether the game has finished

#Tyler Oswald - 11/5/2026
#This is a base class that other screens can inherit from
class Screen:
    def __init__(self, game):
        self.game = game
        self.start_time = 0

        self.enter_duration = 500
        self.wait_duration = 2300
        self.exit_duration = 500
    

    #These methods should be overridden in the child class
    def handleEvent(self, event): 
        pass
    def handleNetMessage(self, message):
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

        self.minigameNames = ["RPS", "Maze", "Reaction", "Minesweeper", "Pizza Cutting"]
        self.minigameNames = list(game.session.minigame_classes.keys())
        # Create one button for each registered minigame
        self.buttons = {}
        for i, name in enumerate(self.minigameNames):
            self.buttons[name] = pygame.Rect(200+(i%2)*210, 120 + (i//2) * 50, 190, 35)

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
            self.game.startTransition("Pizza Cutting", 2, "t1")

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
        super().__init__(game)
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
        self.gameInfo = GameInfo()
        self.timeLeft = 5
        self.titleFont = pygame.font.Font(None, 64)
        self.textFont = pygame.font.Font(None, 32)

        self.virtual_surface = pygame.Surface((800, 400))

        self.max_zoom = 1.5
        self.phase = "enter"
        self.phase_start = pygame.time.get_ticks()

    #Lena Palmieri - 11/12/2026
    #Updates timings for all phases of the animation
    def update(self, dt):
        elapsed = pygame.time.get_ticks() - self.phase_start

        if self.phase == "enter":
            if elapsed >= self.enter_duration:
                self.phase = "wait"
                self.phase_start = pygame.time.get_ticks()

        elif self.phase == "wait":
            self.timeLeft -= dt

            if self.timeLeft <= 0:
                self.phase = "exit"
                self.phase_start = pygame.time.get_ticks()

        elif self.phase == "exit":
            if elapsed >= self.exit_duration:
                self.minigame.start()
                self.game.switchScreen("minigame")

    #Lena Palmieri - 11/12/2026
    #Adjusts the zoom settings for all the phases
    def get_zoom(self):
        elapsed = pygame.time.get_ticks() - self.phase_start

        if self.phase == "enter":
            progress = min(elapsed / self.enter_duration, 1.0)
            return self.max_zoom - (self.max_zoom - 1.0) * progress

        elif self.phase == "wait":
            return 1.0

        elif self.phase == "exit":
            progress = min(elapsed / self.exit_duration, 1.0)
            return 1.0 + (self.max_zoom - 1.0) * progress

        return 1.0

    def draw(self, surface):
        self.virtual_surface.fill((30, 30, 50))
        title = self.titleFont.render(self.minigame.title, True, (255, 255, 255))
        self.virtual_surface.blit(title, title.get_rect(center=(400, 80)))

        y = 160
        for line in self.minigame.instructions.split("\n"):
            text = self.textFont.render(line, True, (255, 255, 255))
            self.virtual_surface.blit(text, text.get_rect(center=(400, y)))
            y += 35

        countdown = self.titleFont.render("Starting in " + str(math.ceil(self.timeLeft)), True, (255, 220, 0))
        self.virtual_surface.blit(countdown, countdown.get_rect(center=(400, 320)))

        #Lena Palmieri - 11/12/2026
        #Calculates the zoom features

        screenWidth, screenHeight = surface.get_size()

        scale = self.get_zoom()

        scaledWidth = int(screenWidth * scale)
        scaledHeight = int(screenHeight * scale)

        scaled_surface = pygame.transform.smoothscale(self.virtual_surface, (scaledWidth, scaledHeight))

        x = (surface.get_width() - scaledWidth) // 2
        y = (surface.get_height() - scaledHeight) // 2

        surface.fill((0, 0, 0))
        surface.blit(scaled_surface, (x, y))

        #Draw game info
        self.gameInfo.draw(surface, self.game.session)


#Jack Larson 11/20/2026
#Heavily taken from instructions, replaces information with round result information
#for a few seconds before moving to the actual instructions
#Also intentionally breaks some zoom features so that the zoom intro plays
#and then then outro plays during instructions

#Nickan Safi 11/20/2026
#Get text values from the game
class ResultsScreen(InstructionScreen):
    def __init__(self, game, minigame):
        super().__init__(game, minigame)
        self.timeLeft = 3
        self.added = False
        
    #Lena Palmieri - 11/12/2026
    #Updates timings for all phases of the animation
    def update(self, dt):
        elapsed = pygame.time.get_ticks() - self.phase_start
        if self.game.roundFinished and not self.added:
            self.timeLeft += 3
            self.added = True

        if self.phase == "enter":
            if elapsed >= self.enter_duration:
                self.phase = "wait"
                self.phase_start = pygame.time.get_ticks()

        elif self.phase == "wait":
            self.timeLeft -= dt

            if self.timeLeft <= 0 and not self.game.roundFinished:
                self.game.switchScreen("instructions")

    def draw(self, surface):
        self.virtual_surface.fill((30, 30, 50))

        titleText = ("Round " + str(self.game.session.roundNumber)) if not self.game.roundFinished else ("Finished " + self.minigame.title)

        title = self.titleFont.render(titleText, True, (255, 255, 255))
        self.virtual_surface.blit(title, title.get_rect(center=(400, 80)))

        resultsText = ("Progress: " + str(self.minigame.result.progress) + "\nScore: " + str(self.minigame.result.score) + "\nTime: " + str(self.minigame.result.score)) if self.game.roundFinished else ("Get Ready!")
        

        if len(self.game.session.lastResults) > 0:
            player = 0 if self.game.session.isHost else 1
            resultA = self.game.session.lastResults[player]
            resultB = self.game.session.lastResults[1-player]

            resultsText = ""
            
            if resultA < resultB:
                resultsText += "ROUND LOST"
            elif resultB < resultA:
                resultsText += "ROUND WON"
            else:
                resultsText += "ROUND TIED"

            resultsText += "\nLIVES LEFT: " + str(self.game.session.players[player].lives)
            resultsText += " VS " + str(self.game.session.players[1-player].lives)

            if resultA.completed != resultB.completed:
                resultsText += "\nYou Finished: " + str(resultA.completed)
                resultsText += "\nOpponent Finished: " + str(resultB.completed)
            elif resultA.score != resultB.score:
                resultsText += "\nYour Score: " + str(resultA.score)
                resultsText += "\nOpponent's Score: " + str(resultB.score)
            elif resultA.progress != resultB.progress:
                resultsText += "\nYour Progress: " + str(round(resultA.progress*100))
                resultsText += "\nOpponent's Progress: " + str(round(resultB.progress*100))
            elif resultA.time != resultB.time:
                resultsText += "\nYour Time: " + str(resultA.time)
                resultsText += "\nOpponent's Time: " + str(resultB.time)
        

        y = 130
        for line in resultsText.split("\n"):
            text = self.textFont.render(line, True, (255, 255, 255))
            self.virtual_surface.blit(text, text.get_rect(center=(400, y)))
            y += 35

        countdown = self.titleFont.render("Advancing in " + str(math.ceil(self.timeLeft)), True, (255, 220, 0))
        self.virtual_surface.blit(countdown, countdown.get_rect(center=(400, 320)))

        #Lena Palmieri - 11/12/2026
        #Calculates the zoom features

        screenWidth, screenHeight = surface.get_size()

        scale = self.get_zoom()

        scaledWidth = int(screenWidth * scale)
        scaledHeight = int(screenHeight * scale)

        scaled_surface = pygame.transform.smoothscale(self.virtual_surface, (scaledWidth, scaledHeight))

        x = (surface.get_width() - scaledWidth) // 2
        y = (surface.get_height() - scaledHeight) // 2

        surface.fill((0, 0, 0))
        surface.blit(scaled_surface, (x, y))

        #Draw game info
        self.gameInfo.draw(surface, self.game.session)



#John Platkowski - 11/8/2026
#Waits for the other player to join the online session this player created
class HostScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 48)
        self.sID = getIP()

    def update(self, dt):
        if self.game.session.server.accept():
            self.game.session.connection = self.game.session.server.connection
            self.game.session.isHost = True
            self.game.session.start()
            self.game.startHostMinigame()

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
        self.waiting = False

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.sessionID = self.sessionID[:-1]
                self.error = ""
            elif event.key == pygame.K_RETURN:
                client = Client(self.sessionID)
                if client.connect():
                    self.game.session.client = client
                    self.game.session.connection = client.connection
                    self.game.session.isHost = False
                    self.game.session.start()
                    self.waiting = True
                else:
                    self.error = "Connection failed"
            elif event.unicode in "0123456789.":
                self.sessionID += event.unicode
                self.error= ""

    def draw(self, surface):
        surface.fill((30, 30, 50))

        if self.waiting:
            text = self.font.render(
                "Connected! Waiting for host...",
                True,
                (255, 255, 255)
            )
            surface.blit(text, text.get_rect(center=(400, 200)))
            return

        prompt = self.font.render("Enter session ID:", True, (255, 255, 255))
        surface.blit(prompt, prompt.get_rect(center=(400, 160)))

        typed = self.font.render(self.sessionID, True, (255, 255, 255))
        surface.blit(typed, typed.get_rect(center=(400, 220)))

        if self.error != "":
            errorText = self.font.render(self.error, True, (255, 80, 80))
            surface.blit(errorText, errorText.get_rect(center=(400, 280)))

#Lena Palmieri - 11/5/2026
#Displays the minigame name and round number when transitioning between screens
class TransitionScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.SysFont(None, 64)
        self.info_font = pygame.font.SysFont(None, 40)

        self.virtual_surface = pygame.Surface((800, 400))

        self.phase = "enter"
        self.max_zoom = 1.5

        self.start_time = 0
        self.enter_transition = 500
        self.animation = 1000
        self.end_transition = 500

        self.game_name = ""
        self.round_number = 1

    def on_enter(self, game_name, round_number, next_screen):
        self.game_name = game_name
        self.round_number = round_number
        self.next_screen = next_screen

        self.phase = "enter"
        self.phase_start = pygame.time.get_ticks()

    def update(self, dt):
        elapsed = pygame.time.get_ticks() - self.phase_start

        if self.phase == "enter":
            if elapsed >= self.enter_duration:
                self.phase = "wait"
                self.phase_start = pygame.time.get_ticks()

        elif self.phase == "wait":
            if elapsed >= self.wait_duration:
                self.phase = "exit"
                self.phase_start = pygame.time.get_ticks()

        elif self.phase == "exit":
            if elapsed >= self.exit_duration:
                self.game.switchScreen(self.next_screen)

    def get_zoom(self):
        elapsed = pygame.time.get_ticks() - self.phase_start

        if self.phase == "enter":
            progress = min(elapsed / self.enter_duration, 1.0)
            return self.max_zoom - (self.max_zoom - 1.0) * progress

        elif self.phase == "wait":
            return 1.0

        elif self.phase == "exit":
            progress = min(elapsed / self.exit_duration, 1.0)
            return 1.0 + (self.max_zoom - 1.0) * progress

        return 1.0

    def draw(self, surface):
        self.virtual_surface.fill((25, 25, 25))

        title = self.title_font.render(
            self.game_name, True, (255, 255, 255)
        )

        round_text = self.info_font.render(
            f"Round {self.round_number}", True, (200, 200, 200)
        )

        self.virtual_surface.blit(
            title, title.get_rect(center=(400, 160))
        )

        self.virtual_surface.blit(
            round_text, round_text.get_rect(center=(400, 230))
        )

        # Get current zoom
        scale = self.get_zoom()

        width = int(800 * scale)
        height = int(400 * scale)

        scaled_surface = pygame.transform.smoothscale(
            self.virtual_surface, (width, height)
        )

        # Center the scaled surface
        x = (surface.get_width() - width) // 2
        y = (surface.get_height() - height) // 2

        surface.fill((0, 0, 0))
        surface.blit(scaled_surface, (x, y))