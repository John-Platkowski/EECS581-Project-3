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

        self.font = pygame.font.Font(None, 36)
        self.largeFont = pygame.font.Font(None, 48)

        self.totalRounds = 10
        self.currentRound = 1

        self.bestTime = None
        self.currentTime = None
        self.successes = 0
        self.failures = 0

        self.state = "waiting"
        self.waitTimer = 5.0
        self.resultTimer = 0.0
        self.timeoutTimer = 5.0

        self.squareSize = 100
        self.difficulty = difficulty
        self.reactionStartTime = None
        self.lastResult = ""

    def start(self):
        self.currentRound = 1
        self.reactionTimes = []
        self.bestTime = None
        self.currentTime = None
        
        self.startRound()

    def startRound(self):
        self.state = "waiting"
        self.waitTimer = 5.0
        self.timeoutTimer = 5.0
        self.reactionStartTime = None
        self.lastResult = ""

    def spawnSquare(self):
        width, height = self.game.surface.get_size()

        if self.difficulty == 3:
            self.squareSize = random.randint(50, 200)
        else:
            self.squareSize = 200

        center_x = width // 2
        center_y = height // 2

        if self.difficulty == 3:
            rand_x = random.randint(max(0, center_x - 300), min(width - self.squareSize, center_x + 300))
            rand_y = random.randint(max(0, center_y - 200), min(height - self.squareSize, center_y + 200))

        elif self.difficulty == 2:
            rand_x = random.randint(max(0, center_x - 200), min(width - self.squareSize, center_x + 200))
            rand_y = random.randint(max(0, center_y - 100), min(height - self.squareSize, center_y + 100))

        else:
            rand_x = center_x - self.squareSize // 2
            rand_y = center_y - self.squareSize // 2

        self.square = pygame.Rect(rand_x, rand_y, self.squareSize, self.squareSize)



    def finishRound(self, result):
        self.lastResult = result

        if self.currentRound < self.totalRounds:
            self.currentRound += 1
            self.startRound()
        else:
            self.state = "game_over"
            if not self.game.session.isSingle():
                self.game.session.send({"type": "reaction_time", "time": self.bestTime})
            self.finish(True)

    def handleNetMessage(self, message):
        if message.get("type") == "reaction_time":
            self.opponentTime = message.get("time")
            self.determineWin()

    def determineWin(self):
        if self.bestTime is None or self.opponentTime is None:
            return
        if self.bestTime < self.opponentTime:
            self.result.score = 1
        elif self.bestTime == self.opponentTime:
            self.result.score = 0
        else:
            self.result.score = -1
        self.finish()

    def recordTime(self):
        reactionTime = (time.perf_counter() - self.reactionStartTime) * 1000
        self.currentTime = reactionTime

        self.successes += 1

        if self.bestTime is None or reactionTime < self.bestTime:
            self.bestTime = reactionTime

        self.finishRound(f"Reaction Time: {reactionTime:.2f} ms")

    def handleEvent(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if self.state == "waiting":
            self.currentTime = "Too Early!"
            self.failures += 1
            self.finishRound("Too Early!")

        elif self.state == "ready":
            if self.square.collidepoint(event.pos):
                self.recordTime()
            else:
                self.currentTime = "Missed!"
                self.failures += 1
                self.finishRound("Missed the Square!")

    def update(self, dt):
        if self.state == "waiting":
            self.waitTimer -= dt

            if self.waitTimer <= 0:
                self.spawnSquare()
                self.state = "ready"
                self.reactionStartTime = time.perf_counter()
                self.timeoutTimer = 8.0

        elif self.state == "ready":
            self.timeoutTimer -= dt

            if self.timeoutTimer <= 0:
                self.currentTime = "Too Slow!"
                self.failures += 1
                self.finishRound("Too Slow! Time's Up!")

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
        if self.currentTime is None:
            currentDisplay = ""
        elif isinstance(self.currentTime, str):
            currentDisplay = self.currentTime
        else:
            currentDisplay = f"{self.currentTime:.2f} ms"

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
        self.gameInfo.draw(surface, self.game.session)
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
