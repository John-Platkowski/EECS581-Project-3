import pygame
import random
from minigame import Minigame

#placeholder
def generateSequence(difficulty, seed):
    return ["red", "green", "blue", "yellow", "red", "blue"][:(3 + difficulty)]

#Trey - 11/20/2026
#Simon says game
class Simon(Minigame):
    title = "Simon Says"
    instructions = "Watch the sequence and repeat it!"

    def __init__(self, game, difficulty, seed):
        super().__init__(game, difficulty, seed)
        self.colors = ["red", "green", "blue", "yellow"]
        self.sequence = generateSequence(difficulty, seed)
        self.state = "showing"
        self.position = 0
        self.timer = 0.6
        self.curColor = None
        self.buttons = {
            "red":    pygame.Rect(250, 80, 140, 120),
            "green":  pygame.Rect(410, 80, 140, 120),
            "blue":   pygame.Rect(250, 210, 140, 120),
            "yellow": pygame.Rect(410, 210, 140, 120),
        }
        self.dim = {"red": (120, 30, 30),
                    "green": (30, 120, 30),
                    "blue": (30, 30, 120),
                    "yellow": (120, 120, 30)}
        self.bright = {"red": (255, 60, 60),
                       "green": (60, 255, 60),
                       "blue": (60, 60, 255),
                       "yellow": (255, 255, 60)}


    def handleEvent(self, event):
        if self.state != "input":
            return
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        clicked = None
        for name, rect in self.buttons.items():
            if rect.collidepoint(event.pos):
                clicked = name
        if clicked is None:
            return
        if clicked == self.sequence[self.position]:
            self.position += 1
            self.result.score = self.position
            if self.position == len(self.sequence):
                self.state = "done"
                self.finish(True)
        else:
            self.state = "done"
            self.finish(False)

    def update(self, dt):
        if self.state == "showing":
            self.timer -= dt
            if self.timer > 0:
                pass
            else:
                if (self.position < len(self.sequence)):
                    if self.curColor is None:
                        self.curColor = self.sequence[self.position]
                        self.position += 1
                        self.timer = 0.6
                    else:
                        self.curColor = None
                        self.timer = 0.3
                else:
                    self.curColor = None
                    self.position = 0
                    self.state = "input"


    def draw(self, surface):
        surface.fill((30, 30, 50))

        for name, rect in self.buttons.items():
            if name == self.curColor:
                drawColor = self.bright[name]
            else:
                drawColor = self.dim[name]
            pygame.draw.rect(surface, drawColor, rect)

        self.gameInfo.draw(surface, self.game.session)
