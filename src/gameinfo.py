import pygame

#Trey - 11/6/2026
#Draws the games info bar in the corner of the screen
class GameInfo:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 28)

    #Draws the info bar
    def draw(self, surface, session):
        text = self.font.render("Section: " + str(session.roundNumber), True, (255,255,255))
        surface.blit(text, (10,10))
        text = self.font.render("Difficulty: " + str(session.difficulty), True, (255,255,255))
        surface.blit(text, (10,40))
        y = 70
        for player in session.players:
            text = self.font.render(player.userName + "'s Lives: " + str(player.lives), True, (255,255,255))
            surface.blit(text, (10, y))
            y += 30
