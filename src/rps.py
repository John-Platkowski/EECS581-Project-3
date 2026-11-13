#John Platkowski - November 8, 2026
#Implements Rock Paper Scissors and a precedent for loading assets
import os
import random
import pygame
from minigame import Minigame

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

#Returns 1 on victory, -1 on loss, 0 on tie
def rpsOutcome(choice, other):
    if choice == other:
        return 0
    if choice == "rock" and other == "scissors":
        return 1
    if choice == "paper" and other == "rock":
        return 1
    if choice == "scissors" and other == "paper":
        return 1
    return -1

#Loads a sprite from the assets folder and scales it 4x
def loadImage(fileName):
    image = pygame.image.load(os.path.join(ASSETS, fileName))
    return pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))


class RPS(Minigame):
    title = "Rock Paper Scissors"
    instructions = "Click rock, paper, or scissors to make your pick."

    def __init__(self, game, difficulty, seed):
        super().__init__(game, difficulty, seed)
        self.font = pygame.font.Font(None, 48)
        self.choice = None
        self.opponentChoice = None
        self.outcome = None
        self.rockImage = loadImage("rock.png")
        self.paperImage = loadImage("paper.png")
        self.scissorsImage = loadImage("scissors.png")
        self.rockHighlighted = loadImage("rock_highlighted.png")
        self.paperHighlighted = loadImage("paper_highlighted.png")
        self.scissorsHighlighted = loadImage("scissors_highlighted.png")
        self.rockButton = self.rockImage.get_rect(center=(200, 200))
        self.paperButton = self.paperImage.get_rect(center=(400, 200))
        self.scissorsButton = self.scissorsImage.get_rect(center=(600, 200))

    def handleEvent(self, event):
        if self.choice is None and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rockButton.collidepoint(event.pos):
                self.pick("rock")
            elif self.paperButton.collidepoint(event.pos):
                self.pick("paper")
            elif self.scissorsButton.collidepoint(event.pos):
                self.pick("scissors")

    #Locks in the player's choice and determines the round outcome
    def pick(self, choice):
        self.choice = choice
        if self.game.session.isSingle():
            self.opponentChoice = random.Random(self.seed).choice(["rock", "paper", "scissors"])
        else:
            self.game.session.send({"type": "rps_choice", "choice": choice})

        self.determineWin()
    #Tyler Oswald - 11/13/2026 
    #Handle incoming messages from other player
    def handleNetMessage(self, message):
        if message.get("type") == "rps_choice":
            self.opponentChoice = message.get("choice")
            self.determineWin()

    #Determines a winner from both the opponent and player choices
    #Moved code from pick to here
    def determineWin(self):
        if self.choice is None or self.opponentChoice is None:
            return
        self.outcome = rpsOutcome(self.choice, self.opponentChoice)
        #Normalize results
        self.result.completed = True
        self.result.score = 1 if self.outcome == 1 else 0
        self.finished = True

    def draw(self, surface):
        surface.fill((30, 30, 50))

        if self.choice is None:
            #Highlight the choice under the mouse
            self.drawText(surface, "Pick one!", (400, 60))
            mouse = pygame.mouse.get_pos()
            self.drawChoice(surface, "rock", (200, 200), self.rockButton.collidepoint(mouse))
            self.drawChoice(surface, "paper", (400, 200), self.paperButton.collidepoint(mouse))
            self.drawChoice(surface, "scissors", (600, 200), self.scissorsButton.collidepoint(mouse))
        else:
            if self.opponentChoice is None:
                self.drawText(surface, "Waiting for opponent...", (400, 200))
                return
            #Show both picks side by side with the outcome below
            self.drawText(surface, "You", (200, 60))
            self.drawText(surface, "Opponent", (600, 60))
            self.drawChoice(surface, self.choice, (200, 200), True)
            self.drawText(surface, "vs", (400, 200))
            self.drawChoice(surface, self.opponentChoice, (600, 200), False)
            if self.outcome == 1:
                self.drawText(surface, "You win!", (400, 340))
            elif self.outcome == 0:
                self.drawText(surface, "It's a tie!", (400, 340))
            else:
                self.drawText(surface, "You lose!", (400, 340))

    #Draws a choice's sprite centered on a point, using the highlighted sprite if highlighted is True
    def drawChoice(self, surface, choice, center, highlighted):
        if choice == "rock":
            image = self.rockHighlighted if highlighted else self.rockImage
        elif choice == "paper":
            image = self.paperHighlighted if highlighted else self.paperImage
        else:
            image = self.scissorsHighlighted if highlighted else self.scissorsImage
        surface.blit(image, image.get_rect(center=center))

    #Draws white text centered on a point
    def drawText(self, surface, text, center):
        rendered = self.font.render(text, True, (255, 255, 255))
        surface.blit(rendered, rendered.get_rect(center=center))
