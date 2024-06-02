import pygame as p
import ChessEngine
import ChessMain
gs = ChessEngine.GameState()

class Move():    

    def movement_pickup():
         #for global, if the dropped square need that info, then global. also if variable got change, do global.
         global mouse_x, mouse_y, mouse_clicked, pickedup_square, possible_dropped_square

         mouse_x, mouse_y = p.mouse.get_pos()
         mouse_x, mouse_y = mouse_x//50, mouse_y//50
         pickedup_square = gs.board[mouse_y][mouse_x]

        #  print(mouse_y, mouse_x)

         #if didnt pickup anything, reset mouseclicked since didnt move
         if pickedup_square == "--":
             mouse_clicked = 0
         else:
             print("mouse_X = ",mouse_x)
             print("mouse_y = ",mouse_y)
             mouse_clicked = 1
             possible_dropped_square = Move.allowableMoveset(mouse_y, mouse_x)
             print(pickedup_square)
             print("Possible dropped_square: ",possible_dropped_square)
             
         return mouse_clicked, mouse_x, mouse_y, possible_dropped_square

    def movement_drop():
         global pickedup_square
         mouse_x2, mouse_y2 = p.mouse.get_pos()
         mouse_x2, mouse_y2 = mouse_x2//50, mouse_y2//50
         dropped_square = gs.board[mouse_y2][mouse_x2]
         mouse_clicked = 0

         #validate the movement, legit or not
         if [mouse_y2, mouse_x2] in (possible_dropped_square):
             print("passed")
             #only move the piece, if the dropped_square is not the same colour and theres a room.
             if dropped_square[0] != pickedup_square [0]: #if can be dropped(TRUE)
                 gs.board[mouse_y2][mouse_x2] = pickedup_square
                 gs.board[mouse_y][mouse_x] = "--"
                 hasMoved = True
             elif dropped_square[0] == pickedup_square [0]: #if cannot be dropped(FALSE)
                 pickedup_square = []
                 hasMoved = False
         else:
             pickedup_square = []
             hasMoved = False

         return gs, hasMoved, mouse_clicked
    
    def allowableMoveset(mouse_y,mouse_x):
        # pickedup_square = gs.board[mouse_y][mouse_x]
        possible_dropped_square = []
        #ro = right obstacles, lo = left obstacles, to = top obstacles, bo = bottom obstacles
        ro, lo, to, bo, bro, blo, tro, tlo = Move.checkObstacles(mouse_y,mouse_x) 

        if pickedup_square in ("wR","bR","wQ","bQ"): # for Rook, either move X only, or move Y only
            possible_dropped_square.extend([[mouse_y-i, mouse_x] for i in range(1,to)]) # move up
            possible_dropped_square.extend([[mouse_y+j, mouse_x] for j in range(1,bo)]) # move down
            possible_dropped_square.extend([[mouse_y, mouse_x+k] for k in range(1,ro)]) # move right
            possible_dropped_square.extend([[mouse_y, mouse_x-l] for l in range(1,lo)]) # move left
            
        if pickedup_square in ("wB","bB","wQ","bQ"): # for Bishop, |x| need to be equal to |y|
            possible_dropped_square.extend([[mouse_y+jk, mouse_x+jk] for jk in range(1,bro)]) # move bottom right
            possible_dropped_square.extend([[mouse_y+jl, mouse_x-jl] for jl in range(1,blo)]) # move bottom left
            possible_dropped_square.extend([[mouse_y-ik, mouse_x+ik] for ik in range(1,tro)]) # move top right
            possible_dropped_square.extend([[mouse_y-il, mouse_x-il] for il in range(1,tlo)]) # move top left
        elif pickedup_square == "wN" or pickedup_square == "bN": # for Knight, move 2y and 1x, OR, 2x and 1y
            knight_move = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for y,x in knight_move:
                if 0 <= mouse_y + y < 8 and 0 <= mouse_x + x < 8:
                    if Move.canEatPiece(pickedup_square[0],gs.board[mouse_y+y][mouse_x+x][0]):
                        possible_dropped_square.append([mouse_y+y, mouse_x+x])
        elif pickedup_square == "wK" or pickedup_square == "bK": # for King, same as Queen, but dont loop. Only plus 1
            for i in [1,0,-1]:
                for j in [1,0,-1]:
                    if i==0 and j==0:# no movement, so remove
                        continue
                    if 0 <= mouse_y + i < 8 and 0 <= mouse_x + j < 8:
                        if Move.canEatPiece(pickedup_square[0],gs.board[mouse_y+i][mouse_x+j][0]):
                            possible_dropped_square.append([mouse_y+i, mouse_x+j])
        elif pickedup_square == "wp" or pickedup_square == "bp": # for pawn, normal move can only move Y positive or negative, depends on colour
            pawn_move_up = pawn_move_down = False
            color = 1 if pickedup_square[0] == "b" else -1 # not that flexible, can be improved
            if color==1 and mouse_y+1<ChessMain.DIMENSION:
                if mouse_x+1<ChessMain.DIMENSION and gs.board[mouse_y+1][mouse_x+1][0] not in [pickedup_square[0],"-"]:
                    possible_dropped_square.append([mouse_y+1, mouse_x+1])
                if mouse_x-1>=0 and gs.board[mouse_y+1][mouse_x-1][0] not in [pickedup_square[0],"-"]:
                    possible_dropped_square.append([mouse_y+1, mouse_x-1])
                if gs.board[mouse_y+1][mouse_x] == "--":
                    possible_dropped_square.append([mouse_y+1, mouse_x])
                    pawn_move_down = True
            elif color==-1 and mouse_y-1>=0:
                if mouse_x+1<ChessMain.DIMENSION and gs.board[mouse_y-1][mouse_x+1][0] not in [pickedup_square[0],"-"]:
                    possible_dropped_square.append([mouse_y-1, mouse_x+1])
                if mouse_x-1>=0 and gs.board[mouse_y-1][mouse_x-1][0] not in [pickedup_square[0],"-"]:
                    possible_dropped_square.append([mouse_y-1, mouse_x-1])
                if gs.board[mouse_y-1][mouse_x] == "--":
                    possible_dropped_square.append([mouse_y-1, mouse_x])
                    pawn_move_up = True

            if (mouse_y == 6 and pickedup_square[0] == "w" and pawn_move_up and gs.board[mouse_y-2][mouse_x] == "--"):#initial movement where pawn can move 2 steps.
                possible_dropped_square.append([mouse_y-2, mouse_x])
            if (mouse_y == 1 and pickedup_square[0] == "b" and pawn_move_down and gs.board[mouse_y+2][mouse_x] == "--"):
                possible_dropped_square.append([mouse_y+2, mouse_x])
             
        return possible_dropped_square
    
    def checkObstacles(mouse_y,mouse_x):
        #Original obstacle is the board border, the numbers of distance to the side of the obstacle
        #readability
        right_border_distance = ChessMain.DIMENSION
        bottom_border_distance = ChessMain.DIMENSION

        right_obstacle = right_border_distance
        left_obstacle = mouse_x+1
        top_obstacle = mouse_y+1
        bottom_obstacle = bottom_border_distance

        bottom_right_obstacle = min(right_border_distance - mouse_x, bottom_border_distance - mouse_y)
        bottom_left_obstacle = min(mouse_x, bottom_border_distance - mouse_y)
        top_right_obstacle = min(mouse_y, right_border_distance - mouse_x)
        top_left_obstacle = min(mouse_y, mouse_x)

        if pickedup_square in ["wR", "bR"]:
            movement = ["+"]
        elif pickedup_square in ["wB", "bB"]:
            movement = ["x"]
        elif pickedup_square in ["wQ", "bQ"]:
            movement = ["x", "+"]
        else:
            movement = []

        if "+" in movement:
            for i in range(1,ChessMain.DIMENSION-mouse_x):## (1,8)
                if (gs.board[mouse_y][mouse_x+i]) != "--":
                    right_obstacle = i if not Move.canEatPiece(pickedup_square[0], gs.board[mouse_y][mouse_x+i][0]) else i+1
                    break
            for i in range(1,mouse_x+1):
                if gs.board[mouse_y][mouse_x-i] != "--":
                    left_obstacle = i if not Move.canEatPiece(pickedup_square[0], gs.board[mouse_y][mouse_x-i][0]) else i+1     
                    break
            for i in range(1,ChessMain.DIMENSION-mouse_y):
                if gs.board[mouse_y+i][mouse_x] != "--":
                    bottom_obstacle = i if not Move.canEatPiece(pickedup_square[0], gs.board[mouse_y+i][mouse_x][0]) else i+1 
                    break
            for i in range(1,mouse_y+1):
                if gs.board[mouse_y-i][mouse_x] != "--":
                    top_obstacle = i if not Move.canEatPiece(pickedup_square[0], gs.board[mouse_y-i][mouse_x][0]) else i+1
                    break
            
        if "x" in movement:##can try copy code above, the pattern can be the same maybe
            for i in range(1,ChessMain.DIMENSION):
                if mouse_x+i > 7 or mouse_y+i > 7:
                    bottom_right_obstacle = i
                    break
                elif gs.board[mouse_y+i][mouse_x+i] != "--":
                    bottom_right_obstacle = i if not Move.canEatPiece(pickedup_square[0], gs.board[mouse_y+i][mouse_x+i][0]) else i+1
                    break
            for i in range(1,ChessMain.DIMENSION):
                if mouse_x-i < 0 or mouse_y+i > 7:
                    bottom_left_obstacle = i
                    break
                elif gs.board[mouse_y+i][mouse_x-i] != "--":
                    bottom_left_obstacle = i if not Move.canEatPiece(pickedup_square[0], gs.board[mouse_y+i][mouse_x-i][0]) else i+1
                    break
            for i in range(1,ChessMain.DIMENSION):
                if mouse_x+i > 7 or mouse_y-i < 0:
                    top_right_obstacle = i
                    break
                elif gs.board[mouse_y-i][mouse_x+i] != "--":
                    top_right_obstacle = i if not Move.canEatPiece(pickedup_square[0], gs.board[mouse_y-i][mouse_x+i][0]) else i+1
                    break
            for i in range(1,ChessMain.DIMENSION):
                if mouse_x-i < 0 or mouse_y-i < 0:
                    top_left_obstacle = i
                    break
                elif gs.board[mouse_y-i][mouse_x-i] != "--":
                    top_left_obstacle = i if not Move.canEatPiece(pickedup_square[0], gs.board[mouse_y-i][mouse_x-i][0]) else i+1
                    break
            
        return right_obstacle, left_obstacle, top_obstacle, bottom_obstacle, bottom_right_obstacle, bottom_left_obstacle, top_right_obstacle, top_left_obstacle
    
    def canEatPiece(pickedPiece, target):
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
