
# Joshua Lin - November 12, 2026
# Implements the Maze minigame, including maze display and player navigation.
# Handles directional movement, collision detection, and destination completion.

import pygame
from minigame import Minigame
from mazeGenerator import generateMaze


class Maze(Minigame):
    title = "Maze"
    instructions = "Navigate through the maze and reach the destination!"

    def __init__(self, game, difficulty, seed):
        super().__init__(game, difficulty, seed)

        self.cellSize = 30
        self.font = pygame.font.Font(None, 32)

        # Generate the maze
        self.maze = generateMaze(difficulty, seed)

        self.rows = len(self.maze)
        self.cols = len(self.maze[0])

        # Find player starting position and destination
        self.playerPosition = self.findStart()
        self.destination = self.findDestination()

    # Finds the starting position in the maze
    def findStart(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 2:
                    return (x, y)

        return None

    # Finds the destination in the maze
    def findDestination(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 3:
                    return (x, y)

        return None

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN and not self.finished:
            if event.key == pygame.K_UP:
                self.move(0, -1)
            elif event.key == pygame.K_DOWN:
                self.move(0, 1)
            elif event.key == pygame.K_LEFT:
                self.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.move(1, 0)

    # Moves the player if the destination tile is traversable
    def move(self, dx, dy):
        newX = self.playerPosition[0] + dx
        newY = self.playerPosition[1] + dy

        # Prevent movement outside the maze
        if not (0 <= newX < self.cols and 0 <= newY < self.rows):
            return

        # Prevent movement through walls
        if self.maze[newY][newX] == 1:
            return

        self.playerPosition = (newX, newY)

        # Check whether the player reached the destination
        if self.playerPosition == self.destination:
            self.finish()

    def draw(self, surface):
        surface.fill((30, 30, 50))

        # Center the maze within the game window
        mazeWidth = self.cols * self.cellSize
        mazeHeight = self.rows * self.cellSize
        offsetX = (surface.get_width() - mazeWidth) // 2
        offsetY = (surface.get_height() - mazeHeight) // 2

        # Draw each maze cell
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(
                    offsetX + x * self.cellSize,
                    offsetY + y * self.cellSize,
                    self.cellSize,
                    self.cellSize
                )

                if self.maze[y][x] == 1:
                    color = (50, 50, 50)       # Wall
                else:
                    color = (220, 220, 220)    # Path

                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (100, 100, 100), rect, 1)

        # Draw destination
        destinationRect = pygame.Rect(
            offsetX + self.destination[0] * self.cellSize,
            offsetY + self.destination[1] * self.cellSize,
            self.cellSize,
            self.cellSize
        )
        pygame.draw.rect(surface, (0, 200, 0), destinationRect)

        # Draw player
        # Draw player as a smaller circle inside the current tile
        playerCenter = (
            offsetX + self.playerPosition[0] * self.cellSize + self.cellSize // 2,
            offsetY + self.playerPosition[1] * self.cellSize + self.cellSize // 2
        )

        pygame.draw.circle(
            surface,
            (50, 100, 255),
            playerCenter,
            self.cellSize // 3
        )
        elapsed = (pygame.time.get_ticks() - self.startTime) / 1000

        timerText = self.font.render(
            f"Time: {elapsed:.2f}s", True, (255, 255, 255)
        )
        surface.blit(timerText, (10, 10))
