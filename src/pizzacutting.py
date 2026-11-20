# Lena Palmieri - 11/19/26
# Creates the pizza cutting minigame

import pygame
import random
import math
from minigame import Minigame

class PizzaCutting(Minigame):

    title = "Pizza Cutting"
    instructions = "Cut the pizza into equal slices!"

    def __init__(self, game, difficulty, seed):
        super().__init__(game, difficulty, seed)

        self.rng = random.Random(seed)

        # Pizza properties
        self.pizzaRadius = 140
        self.pizzaDiameter = self.pizzaRadius * 2

        # Rotation properties
        self.rotation = 0.0
        self.rotationSpeed = 90.0  # Degrees per second

        # Game properties
        self.totalSlices = 0
        self.expectedAngle = 0
        self.cuts = []

        self.state = "playing"

        # Results
        self.sliceResults = []
        self.overallAccuracy = 0.0

        self.font = pygame.font.Font(None, 32)
        self.largeFont = pygame.font.Font(None, 48)
        self.smallFont = pygame.font.Font(None, 25)

        self.pizzaBase = self.createPizza()

    def createPizza(self):
        # Create a transparent surface for the pizza
        pizza = pygame.Surface(
            (self.pizzaDiameter, self.pizzaDiameter),
            pygame.SRCALPHA
        )

        center = (self.pizzaRadius, self.pizzaRadius)

        pygame.draw.circle(
            pizza, (165, 85, 35),
            center, self.pizzaRadius
        )

        pygame.draw.circle(
            pizza, (255, 205, 95),
            center, self.pizzaRadius - 12
        )

        # Pepperoni
        toppings = [
            (0.35, 0.30),
            (0.65, 0.25),
            (0.50, 0.50),
            (0.30, 0.65),
            (0.70, 0.70),
            (0.50, 0.20),
            (0.22, 0.45),
            (0.78, 0.48),
            (0.42, 0.80),
        ]

        for x, y in toppings:
            pos = (
                int(x * self.pizzaDiameter),
                int(y * self.pizzaDiameter)
            )

            pygame.draw.circle(
                pizza, (190, 35, 35),
                pos, 11
            )

        return pizza

    def start(self):
        self.totalSlices = self.rng.randint(3, 10)
        self.expectedAngle = 360.0 / self.totalSlices

        self.rotation = 0.0
        self.cuts = []

        self.sliceResults = []
        self.overallAccuracy = 0.0

        self.state = "playing"

    def getPizzaCenter(self):
        width, height = self.game.surface.get_size()

        return (
            width // 2,
            height // 2 + 20
        )

    def makeCut(self):
        # The guide is stationary at the top of the screen.
        # Record its angle relative to the rotating pizza.
        cutAngle = (self.rotation - 90) % 360

        self.cuts.append(cutAngle)

        # Each radial cut creates one additional slice.
        if len(self.cuts) >= self.totalSlices:
            self.calculateAccuracy()
            self.state = "results"
            self.finish(True)

    def calculateAccuracy(self):
        # Sort cuts by their angular position
        angles = sorted(self.cuts)

        self.sliceResults = []

        for i in range(len(angles)):

            # Find the next cut, including the wraparound
            nextIndex = (i + 1) % len(angles)

            actualAngle = angles[nextIndex] - angles[i]

            if nextIndex == 0:
                actualAngle += 360

            # Compare actual angle with expected angle
            error = abs(actualAngle - self.expectedAngle)

            accuracy = max(
                0,
                100 * (1 - error / self.expectedAngle)
            )

            self.sliceResults.append({
                "angle": actualAngle,
                "accuracy": accuracy
            })

        # Calculate average accuracy
        self.overallAccuracy = sum(
            result["accuracy"] for result in self.sliceResults
        ) / len(self.sliceResults)

    def handleEvent(self, event):
        if self.state != "playing":
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            center = self.getPizzaCenter()

            # Check if the player clicked inside the pizza
            distance = math.hypot(
                event.pos[0] - center[0],
                event.pos[1] - center[1]
            )

            if distance <= self.pizzaRadius:
                self.makeCut()

    def update(self, dt):
        if self.state == "playing":

            # Continuously rotate the pizza
            self.rotation = (
                self.rotation + self.rotationSpeed * dt
            ) % 360
            
    def drawDottedGuide(self, surface, center):
        # Draw a stationary radial cutting guide
        cx, cy = center

        for distance in range(0, self.pizzaRadius, 14):

            start = (cx, cy - distance)
            end = (cx, cy - min(distance + 7, self.pizzaRadius))

            pygame.draw.line(
                surface,
                (255, 255, 255),
                start,
                end,
                3
            )
            

    def drawPizza(self, surface, center):
        # Start with the original pizza
        pizza = self.pizzaBase.copy()

        cx = cy = self.pizzaRadius

        # Draw all previously made cuts
        for angle in self.cuts:

            radians = math.radians(angle)

            endX = cx + math.cos(radians) * self.pizzaRadius
            endY = cy + math.sin(radians) * self.pizzaRadius

            pygame.draw.line(
                pizza,
                (100, 45, 20),
                (cx, cy),
                (int(endX), int(endY)),
                4
            )

        # Rotate the pizza
        rotatedPizza = pygame.transform.rotate(
            pizza,
            self.rotation
        )

        rect = rotatedPizza.get_rect(center=center)

        surface.blit(rotatedPizza, rect)

    def draw(self, surface):
        surface.fill((30, 30, 50))

        center = self.getPizzaCenter()

        if self.state == "playing":

            # Challenge information
            title = self.largeFont.render(
                f"Cut the pizza into {self.totalSlices} slices!",
                True,
                (255, 255, 255)
            )

            surface.blit(
                title,
                title.get_rect(
                    center=(surface.get_width() // 2, 35)
                )
            )

            counter = self.font.render(
                f"Cuts: {len(self.cuts)}/{self.totalSlices}",
                True,
                (255, 220, 0)
            )

            surface.blit(counter, (20, 75))

            # Draw pizza and guide
            self.drawPizza(surface, center)
            self.drawDottedGuide(surface, center)

            instructions = self.smallFont.render(
                "Click inside the pizza to make a cut!",
                True,
                (220, 220, 220)
            )

            surface.blit(
                instructions,
                instructions.get_rect(
                    center=(
                        surface.get_width() // 2,
                        surface.get_height() - 25
                    )
                )
            )

        elif self.state == "results":

            title = self.largeFont.render(
                "Pizza Cutting Results",
                True,
                (255, 255, 255)
            )

            self.drawPizza(surface, center)

            surface.blit(
                title,
                title.get_rect(
                    center=(surface.get_width() // 2, 35)
                )
            )

            overall = self.largeFont.render(
                f"Overall Accuracy: {self.overallAccuracy:.2f}%",
                True,
                (255, 220, 0)
            )

            surface.blit(
                overall,
                overall.get_rect(
                    center=(surface.get_width() // 2, 85)
                )
            )

            # Display individual slice measurements
            for i, result in enumerate(self.sliceResults):

                column = i // 12
                row = i % 12

                x = 120 + column * 400
                y = 140 + row * 38

                text = self.smallFont.render(
                    f"Slice {i + 1}: "
                    f"{result['angle']:.2f} degrees  |  "
                    f"{result['accuracy']:.2f}%",
                    True,
                    (255, 255, 255)
                )

                surface.blit(text, (x, y))
