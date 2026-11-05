#Jack Larson 11/5/2026
#Stores information regarding the result of the game,
#to be returned by a minigame upon completion.
class GameResult:
    #Jack Larson 11/5/2026
    def __init__(self):
        self.completed = False
        self.progress = 0.0
        self.score = 0
        self.time = 0.0
