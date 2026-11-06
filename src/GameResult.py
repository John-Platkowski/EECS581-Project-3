#Nickan Safi 11/6/2026
#Added comparison operators between results

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

    def __le__(self,other):
        #Nickan Safi 11/6/2026
        if self.completed < other.completed:
            return True
        if self.completed == other.completed and self.score < other.score
            return True
        if self.completed == other.completed and self.score == other.score and self.progress < other.progress:
            return True
        if self.completed == other.completed and self.score == other.score and self.progress == other.progress and self.time > other.time:
            return True
    
    def __eq__(self,other):
        #Nickan Safi 11/6/2026
        return self.completed == other.completed and self.score == other.score and self.progress == other.progress and self.time == other.time