#Jack Larson 11/5/2026
#Stores information regarding a given player, as well as handles lives management.
class Player:
    #Jack Larson 11/5/2026
    def __init__(self):
        self.userName = "Steve"
        self.userID = -1
        self.lives = 0

    #Jack Larson 11/5/2026
    #Removes a life and checks for total loss.
    #Likely called by the Session class when a minigame returns a
    #GameResult object it deems as a failure when comparing to the other players'.
    def loseLife(self):
        self.lives = self.lives - 1
        if self.lives < 1:
            #End the game somehow.
            #Dummy code to avoid error.
            1+1
