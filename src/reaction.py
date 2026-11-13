# Lena Palmieri - 11/13/2026
# Implements the Reaction minigame for singleplayer
# Spawns a square which the player must click in order for a reaction to be recorded
# Records the player's best time 

import pygame
import random
import time
from minigame import Minigame


class Reaction(Minigame):
    title = "Reaction"
    instructions = "Click the green square as quickly as possible!"

    def __init__(self, game, difficulty, seed):
        super().__init__(game, difficulty, seed)

        self.squareSize = 200
        self.font = pygame.font.Font(None, 36)
        self.largeFont = pygame.font.Font(None, 48)

        self.totalRounds = 15
        self.currentRound = 1

        self.bestTime = None
        self.currentTime = None
        self.successes = 0
        self.failures = 0

        self.state = "waiting"
        self.waitTimer = 15.0
        self.resultTimer = 0.0
        self.timeoutTimer = 8.0

        self.square = pygame.Rect(0, 0, self.squareSize, self.squareSize)
        self.startTime = None
        self.lastResult = ""

    def start(self):
        self.currentRound = 1
        self.reactionTimes = []
        self.bestTime = None
        self.currentTime = None
        self.successes = 0
        self.failures = 0

        self.startRound()

    def startRound(self):
        self.state = "waiting"
        self.waitTimer = 15.0
        self.resultTimer = 0.0
        self.timeoutTimer = 8.0
        self.startTime = None
        self.currentTime = None
        self.lastResult = ""

    def spawnSquare(self):
        #easy difficulty the square stays in one spot

        width, height = self.game.surface.get_size()

        # Define the center region (middle 50% of screen)
        regionWidth = width * 0.5
        regionHeight = height * 0.5

        self.square.x = width // 2 - (self.squareSize / 2)
        self.square.y = height // 2 - (self.squareSize / 2)

    def finishRound(self, result):
        self.lastResult = result
        self.state = "result"
        self.resultTimer = 5.0
        self.startTime = None

    def recordTime(self):
        reactionTime = (time.perf_counter() - self.startTime) * 1000
        self.currentTime = reactionTime

        self.successes += 1

        if self.bestTime is None or reactionTime < self.bestTime:
            self.bestTime = reactionTime

        self.finishRound(f"Reaction Time: {reactionTime:.2f} ms")

    def handleEvent(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if self.state == "waiting":
            self.failures += 1
            self.finishRound("Too Early!")

        elif self.state == "ready":
            if self.square.collidepoint(event.pos):
                self.recordTime()
            else:
                self.failures += 1
                self.finishRound("Missed the Square!")

    def update(self, dt):
        if self.state == "waiting":
            self.waitTimer -= dt

            if self.waitTimer <= 0:
                self.spawnSquare()
                self.state = "ready"
                self.startTime = time.perf_counter()
                self.timeoutTimer = 8.0

        elif self.state == "ready":
            self.timeoutTimer -= dt

            if self.timeoutTimer <= 0:
                self.failures += 1
                self.finishRound("Too Slow! Time's Up!")

        elif self.state == "result":
            self.resultTimer -= dt

            if self.resultTimer <= 0:
                if self.currentRound < self.totalRounds:
                    self.currentRound += 1
                    self.startRound()
                else:
                    self.state = "game_over"

    def draw(self, surface):
        surface.fill((30, 30, 50))

        # Round counter
        roundText = self.font.render(
            f"Round {self.currentRound}/{self.totalRounds}",
            True,
            (255, 255, 255)
        )
        surface.blit(roundText, (20, 20))

        # Current time
        currentDisplay = (
            f"{self.currentTime:.2f} ms"
            if self.currentTime is not None
            else "--:--"
        )

        currentText = self.font.render(
            f"Current Time: {currentDisplay}",
            True,
            (255, 255, 255)
        )
        surface.blit(currentText, (20, 65))

        # Best time
        bestDisplay = (
            f"{self.bestTime:.2f} ms"
            if self.bestTime is not None
            else "--:--"
        )

        bestText = self.font.render(
            f"Best Time: {bestDisplay}",
            True,
            (255, 220, 0)
        )
        surface.blit(bestText, (20, 105))

        # Main game area
        if self.state == "waiting":
            message = self.largeFont.render(
                "Wait for the square...",
                True,
                (255, 255, 255)
            )
            surface.blit(message, message.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))

        elif self.state == "ready":
            pygame.draw.rect(surface, (0, 255, 0), self.square)

            timerText = self.font.render(
                f"Time left: {self.timeoutTimer:.1f}s",
                True,
                (255, 255, 255)
            )
            surface.blit(timerText, (20, 150))

        elif self.state == "result":
            message = self.largeFont.render(
                self.lastResult,
                True,
                (255, 255, 255)
            )
            surface.blit(message, message.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 30)))

            nextMessage = self.font.render(
                f"Next round in {self.resultTimer:.1f} seconds",
                True,
                (200, 200, 200)
            )
            surface.blit(nextMessage, nextMessage.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 30)))

        elif self.state == "game_over":

            results = [
                "Game Complete!",
                f"Best Time: {self.bestTime}"           ]

            for i, line in enumerate(results):
                text = self.font.render(line, True, (255, 255, 255))
                surface.blit(
                    text,
                    text.get_rect(center=(400, 210 + i * 45))
                )
