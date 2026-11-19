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

    #Joshua - 11/19/2026
    #Created less than which is what handle uses to compare results

    def __lt__(self, other):
        if not isinstance(other, GameResult):
            return NotImplemented
        
        # An incomplete game is worse than a completed game.
        if self.completed != other.completed:
            return not self.completed

        # Higher scores are better.
        if self.score != other.score:
            return self.score < other.score

        # More progress is better.
        if self.progress != other.progress:
            return self.progress < other.progress

        # Less time is better.
        return self.time > other.time
    
    def __le__(self,other):
        #Nickan Safi 11/6/2026
        return self < other or self == other
    
    def __eq__(self,other):
        #joshua - 11/19/2026
        #Type handling 
        if not isinstance(other, GameResult):
            return NotImplemented

        #Nickan Safi 11/6/2026
        return self.completed == other.completed and self.score == other.score and self.progress == other.progress and self.time == other.time