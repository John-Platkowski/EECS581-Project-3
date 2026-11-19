import pygame

#Trey - 11/6/2026
#Draws the games info bar in the corner of the screen
class GameInfo:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 22)
        self.padding = 10
        self.backgroundColor = (30, 30, 30)
        self.textColor = (255, 255, 255)

    #Draws the info bar
    def draw(self, surface, session):
        info = [
            f"Section: {session.roundNumber}",
            f"Difficulty: {session.difficulty}"
        ]

        for player in session.players:
            info.append(f"{player.userName}: {player.lives} Lives")

        #Render each piece of information
        texts = [self.font.render(item, True, self.textColor) for item in info]

        #Calculate bar dimensions
        width = sum(text.get_width() for text in texts)
        width += self.padding * (len(texts) + 1)
        height = max(text.get_height() for text in texts) + self.padding * 2

        #Draw background
        bar = pygame.Rect(surface.get_width() - width - 10, 10, width, height)
        pygame.draw.rect(surface, self.backgroundColor, bar, border_radius=6)

        #Draw information horizontally
        x = bar.x + self.padding
        y = bar.y + self.padding

        for text in texts:
            surface.blit(text, (x, y))
            x += text.get_width() + self.padding
