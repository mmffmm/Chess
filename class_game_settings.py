#WIP

import pygame as p
import ChessEngine
import ChessMain
gs = ChessEngine.GameState()


#quick copy pasted from class Move. might have issue
class GameSetting():
    
    def __init__(self, game_state, SQ_SIZE):
        self.gs = game_state
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_x2 = 0
        self.mouse_y2 = 0
        self.mouse_clicked = 0
        self.clicked_location = ""
        self.SQ_SIZE = SQ_SIZE

    def action(self):
        self.mouse_x, self.mouse_y = p.mouse.get_pos()
        self.mouse_x, self.mouse_y = self.mouse_x//self.SQ_SIZE, self.mouse_y//self.SQ_SIZE
        self.clicked_location = gs.board[self.mouse_y][self.mouse_x]

        