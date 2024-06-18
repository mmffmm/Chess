import pygame as p
import ChessEngine
import ChessMain
gs = ChessEngine.GameState()

class Move():

    def __init__(self, game_state):
        self.gs = game_state
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_x2 = 0
        self.mouse_y2 = 0
        self.mouse_clicked = 0
        self.pickedup_square = ""
        self.possible_dropped_square = []

    def movement_pickup(self):

        self.mouse_x, self.mouse_y = p.mouse.get_pos()
        self.mouse_x, self.mouse_y = self.mouse_x//50, self.mouse_y//50
        self.pickedup_square = gs.board[self.mouse_y][self.mouse_x]

        #  print(mouse_y, mouse_x)

        #if didnt pickup anything, reset mouseclicked since didnt move
        if self.pickedup_square == "--":
            self.mouse_clicked = 0
            self.possible_dropped_square = []
        else:
            print("mouse_X = ",self.mouse_x)
            print("mouse_y = ",self.mouse_y)
            self.mouse_clicked = 1
            self.possible_dropped_square = self._allowableMoveset()
            print(self.pickedup_square)
            print("Possible dropped_square: ",self.possible_dropped_square)
            
        return self.mouse_clicked, self.mouse_x, self.mouse_y, self.possible_dropped_square

    def movement_drop(self):
         self.mouse_x2, self.mouse_y2 = p.mouse.get_pos()
         self.mouse_x2, self.mouse_y2 = self.mouse_x2//50, self.mouse_y2//50
         self.dropped_square = gs.board[self.mouse_y2][self.mouse_x2]
         self.mouse_clicked = 0

         #validate the movement, legit or not
         if [self.mouse_y2, self.mouse_x2] in (self.possible_dropped_square):
             print("passed")
             #only move the piece, if the dropped_square is not the same colour and theres a room.
             if self.dropped_square[0] != self.pickedup_square [0]: #if can be dropped(TRUE)
                 gs.board[self.mouse_y2][self.mouse_x2] = self.pickedup_square
                 gs.board[self.mouse_y][self.mouse_x] = "--"
                 hasMoved = True
             elif self.dropped_square[0] == self.pickedup_square [0]: #if cannot be dropped(FALSE)
                 self.pickedup_square = []
                 hasMoved = False
         else:
             self.pickedup_square = []
             hasMoved = False

         return gs, hasMoved, self.mouse_clicked
    
    def _allowableMoveset(self):
        # pickedup_square = gs.board[mouse_y][mouse_x]
        self.possible_dropped_square = []
        #ro = right obstacles, lo = left obstacles, to = top obstacles, bo = bottom obstacles
        ro, lo, to, bo, bro, blo, tro, tlo = self._checkObstacles() 

        if self.pickedup_square in ("wR","bR","wQ","bQ"): # for Rook, either move X only, or move Y only
            self.possible_dropped_square.extend([[self.mouse_y-i, self.mouse_x] for i in range(1,to)]) # move up
            self.possible_dropped_square.extend([[self.mouse_y+j, self.mouse_x] for j in range(1,bo)]) # move down
            self.possible_dropped_square.extend([[self.mouse_y, self.mouse_x+k] for k in range(1,ro)]) # move right
            self.possible_dropped_square.extend([[self.mouse_y, self.mouse_x-l] for l in range(1,lo)]) # move left
            
        if self.pickedup_square in ("wB","bB","wQ","bQ"): # for Bishop, |x| need to be equal to |y|
            self.possible_dropped_square.extend([[self.mouse_y+jk, self.mouse_x+jk] for jk in range(1,bro)]) # move bottom right
            self.possible_dropped_square.extend([[self.mouse_y+jl, self.mouse_x-jl] for jl in range(1,blo)]) # move bottom left
            self.possible_dropped_square.extend([[self.mouse_y-ik, self.mouse_x+ik] for ik in range(1,tro)]) # move top right
            self.possible_dropped_square.extend([[self.mouse_y-il, self.mouse_x-il] for il in range(1,tlo)]) # move top left

        elif self.pickedup_square in ("wN","bN"): # for Knight, move 2y and 1x, OR, 2x and 1y
            knight_move = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for y,x in knight_move:
                if 0 <= self.mouse_y + y < 8 and 0 <= self.mouse_x + x < 8:
                    if self._canEatPiece(self.pickedup_square[0],gs.board[self.mouse_y+y][self.mouse_x+x][0]):
                        self.possible_dropped_square.append([self.mouse_y+y, self.mouse_x+x])

        elif self.pickedup_square in ("wK","bK"): # for King, same as Queen, but dont loop. Only plus 1
            for i in [1,0,-1]:
                for j in [1,0,-1]:
                    if i==0 and j==0:# no movement, so remove
                        continue
                    if 0 <= self.mouse_y + i < 8 and 0 <= self.mouse_x + j < 8:
                        if self._canEatPiece(self.pickedup_square[0],gs.board[self.mouse_y+i][self.mouse_x+j][0]):
                            self.possible_dropped_square.append([self.mouse_y+i, self.mouse_x+j])

        elif self.pickedup_square in ("wp","bp"): # for pawn, normal move can only move Y positive or negative, depends on colour
            pawn_move_up = pawn_move_down = False
            color = 1 if self.pickedup_square[0] == "b" else -1 # not that flexible, can be improved
            if color==1 and self.mouse_y+1<ChessMain.DIMENSION:
                if self.mouse_x+1<ChessMain.DIMENSION and gs.board[self.mouse_y+1][self.mouse_x+1][0] not in [self.pickedup_square[0],"-"]:
                    self.possible_dropped_square.append([self.mouse_y+1, self.mouse_x+1])
                if self.mouse_x-1>=0 and gs.board[self.mouse_y+1][self.mouse_x-1][0] not in [self.pickedup_square[0],"-"]:
                    self.possible_dropped_square.append([self.mouse_y+1, self.mouse_x-1])
                if gs.board[self.mouse_y+1][self.mouse_x] == "--":
                    self.possible_dropped_square.append([self.mouse_y+1, self.mouse_x])
                    pawn_move_down = True
            elif color==-1 and self.mouse_y-1>=0:
                if self.mouse_x+1<ChessMain.DIMENSION and gs.board[self.mouse_y-1][self.mouse_x+1][0] not in [self.pickedup_square[0],"-"]:
                    self.possible_dropped_square.append([self.mouse_y-1, self.mouse_x+1])
                if self.mouse_x-1>=0 and gs.board[self.mouse_y-1][self.mouse_x-1][0] not in [self.pickedup_square[0],"-"]:
                    self.possible_dropped_square.append([self.mouse_y-1, self.mouse_x-1])
                if gs.board[self.mouse_y-1][self.mouse_x] == "--":
                    self.possible_dropped_square.append([self.mouse_y-1, self.mouse_x])
                    pawn_move_up = True

            if (self.mouse_y == 6 and self.pickedup_square[0] == "w" and pawn_move_up and gs.board[self.mouse_y-2][self.mouse_x] == "--"):#initial movement where pawn can move 2 steps.
                self.possible_dropped_square.append([self.mouse_y-2, self.mouse_x])
            if (self.mouse_y == 1 and self.pickedup_square[0] == "b" and pawn_move_down and gs.board[self.mouse_y+2][self.mouse_x] == "--"):
                self.possible_dropped_square.append([self.mouse_y+2, self.mouse_x])
             
        return self.possible_dropped_square
    
    def _checkObstacles(self):
        #Original obstacle is the board border, the numbers of distance to the side of the obstacle
        #readability
        right_border_distance = ChessMain.DIMENSION
        bottom_border_distance = ChessMain.DIMENSION

        right_obstacle = right_border_distance
        left_obstacle = self.mouse_x+1
        top_obstacle = self.mouse_y+1
        bottom_obstacle = bottom_border_distance

        bottom_right_obstacle = min(right_border_distance - self.mouse_x, bottom_border_distance - self.mouse_y)
        bottom_left_obstacle = min(self.mouse_x, bottom_border_distance - self.mouse_y)
        top_right_obstacle = min(self.mouse_y, right_border_distance - self.mouse_x)
        top_left_obstacle = min(self.mouse_y, self.mouse_x)

        if self.pickedup_square in ["wR", "bR"]:
            movement = ["+"]
        elif self.pickedup_square in ["wB", "bB"]:
            movement = ["x"]
        elif self.pickedup_square in ["wQ", "bQ"]:
            movement = ["x", "+"]
        else:
            movement = []

        if "+" in movement:
            for i in range(1,ChessMain.DIMENSION-self.mouse_x):## (1,8)
                if (gs.board[self.mouse_y][self.mouse_x+i]) != "--":
                    right_obstacle = i if not self._canEatPiece(self.pickedup_square[0], gs.board[self.mouse_y][self.mouse_x+i][0]) else i+1
                    break
            for i in range(1,self.mouse_x+1):
                if gs.board[self.mouse_y][self.mouse_x-i] != "--":
                    left_obstacle = i if not self._canEatPiece(self.pickedup_square[0], gs.board[self.mouse_y][self.mouse_x-i][0]) else i+1     
                    break
            for i in range(1,ChessMain.DIMENSION-self.mouse_y):
                if gs.board[self.mouse_y+i][self.mouse_x] != "--":
                    bottom_obstacle = i if not self._canEatPiece(self.pickedup_square[0], gs.board[self.mouse_y+i][self.mouse_x][0]) else i+1 
                    break
            for i in range(1,self.mouse_y+1):
                if gs.board[self.mouse_y-i][self.mouse_x] != "--":
                    top_obstacle = i if not self._canEatPiece(self.pickedup_square[0], gs.board[self.mouse_y-i][self.mouse_x][0]) else i+1
                    break
            
        if "x" in movement:##can try copy code above, the pattern can be the same maybe
            for i in range(1,ChessMain.DIMENSION):
                if self.mouse_x+i > 7 or self.mouse_y+i > 7:
                    bottom_right_obstacle = i
                    break
                elif gs.board[self.mouse_y+i][self.mouse_x+i] != "--":
                    bottom_right_obstacle = i if not self._canEatPiece(self.pickedup_square[0], gs.board[self.mouse_y+i][self.mouse_x+i][0]) else i+1
                    break
            for i in range(1,ChessMain.DIMENSION):
                if self.mouse_x-i < 0 or self.mouse_y+i > 7:
                    bottom_left_obstacle = i
                    break
                elif gs.board[self.mouse_y+i][self.mouse_x-i] != "--":
                    bottom_left_obstacle = i if not self._canEatPiece(self.pickedup_square[0], gs.board[self.mouse_y+i][self.mouse_x-i][0]) else i+1
                    break
            for i in range(1,ChessMain.DIMENSION):
                if self.mouse_x+i > 7 or self.mouse_y-i < 0:
                    top_right_obstacle = i
                    break
                elif gs.board[self.mouse_y-i][self.mouse_x+i] != "--":
                    top_right_obstacle = i if not self._canEatPiece(self.pickedup_square[0], gs.board[self.mouse_y-i][self.mouse_x+i][0]) else i+1
                    break
            for i in range(1,ChessMain.DIMENSION):
                if self.mouse_x-i < 0 or self.mouse_y-i < 0:
                    top_left_obstacle = i
                    break
                elif gs.board[self.mouse_y-i][self.mouse_x-i] != "--":
                    top_left_obstacle = i if not self._canEatPiece(self.pickedup_square[0], gs.board[self.mouse_y-i][self.mouse_x-i][0]) else i+1
                    break
            
        return right_obstacle, left_obstacle, top_obstacle, bottom_obstacle, bottom_right_obstacle, bottom_left_obstacle, top_right_obstacle, top_left_obstacle
    
    def _canEatPiece(self, pickedPiece, target):
         if pickedPiece == target:
            return False
         else:
            return True
#test
    
      
        # SPECIAL MOVES LIST
            # first pawn when eat, can move diagonal
            # pawn when start, can move two square
            # castling
            # horse, king is fixed movement
            # rook, bishop, queen, pawn(kinda) is flexible movement
