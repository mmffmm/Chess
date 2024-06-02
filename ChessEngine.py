## responsible for the current state, determining the moves

class GameState():
        DIMENSION = 8 # I think better put dimension here tbh
        def __init__(self):
                self.board = [
                        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
                ]

                self.whiteToMove = True
                self.moveLog = []
                
        # This one is not really used, got from youtube.
                
        # def distanceTravel(self):
        #         if self == "bR" or self == "bB" or self == "bQ" or self == "wR" or self == "wB" or self == "wQ":
        #                 travel_distance = GameState.DIMENSION
        #         elif self != "wN" or self != "bN":
        #                 travel_distance = 1

        #         return travel_distance
        
        
        # def presetMove(self):
        #         piece = []
        #         piece['wR'] = 
