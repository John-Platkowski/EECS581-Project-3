import pygame

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
class TestScreen1(Screen):
    def handleEvent(self, event):
        #Pressing any key changes to the other test screen
        if event.type == pygame.KEYDOWN:
            self.switchScreen("t2")

    def draw(self, surface):
        surface.fill((255, 0, 0))


class TestScreen2(Screen):
    #Pressing any key changes to the other test screen
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.switchScreen("t1")

    def draw(self, surface):
        surface.fill((0, 0, 255))