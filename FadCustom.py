import pygame as p
import ChessEngine
import ChessMain
gs = ChessEngine.GameState()

class Move():    

    def movement_pickup():
         #rule of thumb for global, if the dropped square need that info, then global. also if variable got change, do global.
         global mouse_x, mouse_y, mouse_clicked, pickedup_square, possible_dropped_square

         mouse_x, mouse_y = p.mouse.get_pos()
         mouse_x, mouse_y = mouse_x//50, mouse_y//50
         pickedup_square = gs.board[mouse_y][mouse_x]

        #  print(mouse_y, mouse_x)

         #if didnt pickup anything, reset mouseclicked since didnt move
         if pickedup_square == "--":
             mouse_clicked = 0
         else:
             mouse_clicked = 1
             possible_dropped_square = Move.allowableMoveset(mouse_y, mouse_x)
             print(pickedup_square)
             print("Possible dropped_square: ",possible_dropped_square)
             
         return mouse_clicked

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
                #  gs.board[mouse_y2][mouse_x2] = dropped_square
                 hasMoved = False
         else:
             hasMoved = False
            #  pickedup_square = ''
            #  print("not passed") 
            #  gs.board[mouse_y2][mouse_x2] = dropped_square

         return gs, hasMoved, mouse_clicked
    
    def allowableMoveset(mouse_y,mouse_x):
        pickedup_square = gs.board[mouse_y][mouse_x]
        possible_dropped_square = []
        #ro = right obstacles, lo = left obstacles, to = top obstacles, bo = bottom obstacles
        ro, lo, to, bo, bro, blo, tro, tlo = Move.checkObstacles(mouse_y,mouse_x) 

        '''
        FLEXIBLE MOVEMENT PIECE: ROOK & BISHOP & QUEEN
        '''
        if pickedup_square in ("wR","bR","wQ","bQ"): # for Rook, either move X only, or move Y only
            possible_dropped_square.extend([[mouse_y-i, mouse_x] for i in range(to+1)]) # move up
            possible_dropped_square.extend([[mouse_y+j, mouse_x] for j in range(bo+1)]) # move down
            possible_dropped_square.extend([[mouse_y, mouse_x+k] for k in range(ro+1)]) # move right
            possible_dropped_square.extend([[mouse_y, mouse_x-l] for l in range(lo+1)]) # move left
            
        if pickedup_square in ("wB","bB","wQ","bQ"): # for Bishop, |x| need to be equal to |y|
            possible_dropped_square.extend([[mouse_y+jk, mouse_x+jk] for jk in range(bro+1)]) # move bottom right
            possible_dropped_square.extend([[mouse_y+jl, mouse_x-jl] for jl in range(blo+1)]) # move bottom left
            possible_dropped_square.extend([[mouse_y-ik, mouse_x+ik] for ik in range(tro+1)]) # move top right
            possible_dropped_square.extend([[mouse_y-il, mouse_x-il] for il in range(tlo+1)]) # move top left
        elif pickedup_square == "wN" or pickedup_square == "bN": # for Knight, move 2y and 1x, OR, 2x and 1y
             knight_move = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
             for y,x in knight_move:
                 possible_dropped_square.append([mouse_y+y, mouse_x+x])
        elif pickedup_square == "wK" or pickedup_square == "bK": # for King, same as Queen, but dont loop. Only plus 1
             for i in [1,0,-1]:
                 for j in [1,0,-1]:
                     if i==0 and j==0:# no movement, so remove
                         continue
                     possible_dropped_square.append([mouse_y+i, mouse_x+j])
        elif pickedup_square == "wp" or pickedup_square == "bp": # for pawn, normal move can only move Y positive or negative, depends on colour
             color = 1 if pickedup_square[0] == "b" else -1 # not that flexible, can be improved
             possible_dropped_square.append([mouse_y+color, mouse_x])
             if (mouse_y == 6 and pickedup_square[0] == "w") or (mouse_y == 1 and pickedup_square[0] == "b"):
                 possible_dropped_square.append([mouse_y+color+color, mouse_x])
 
            
        # SPECIAL MOVES LIST
            # first pawn when eat, can move diagonal
            # pawn when start, can move two square
            # castling
            # horse, king is fixed movement
            # rook, bishop, queen, pawn(kinda) is flexible movement
            #
        return possible_dropped_square
    
    def checkObstacles(mouse_y,mouse_x):
        #Original obstacle is the board border
        right_obstacle = ChessMain.DIMENSION - mouse_x -1
        left_obstacle = mouse_x
        top_obstacle = mouse_y
        bottom_obstacle = ChessMain.DIMENSION - mouse_y -1

        bottom_right_obstacle = min(ChessMain.DIMENSION - mouse_x -1, ChessMain.DIMENSION - mouse_y -1)
        bottom_left_obstacle = min(mouse_x, ChessMain.DIMENSION - mouse_y -1)
        top_right_obstacle = min(mouse_y, ChessMain.DIMENSION - mouse_x -1)
        top_left_obstacle = min(mouse_y, mouse_x)

        if pickedup_square == "wR" or pickedup_square == "bR":
            movement = ["+"]
        elif pickedup_square == "wB" or pickedup_square == "bB":
            movement = ["x"]
        elif pickedup_square == "wQ" or pickedup_square == "bQ":
            movement = ["x", "+"]
        else:
            movement = []

        if "+" in movement:
            for i in range(ChessMain.DIMENSION):
                if mouse_x+1+i <8 and gs.board[mouse_y][mouse_x+1+i] != "--":
                    right_obstacle = i+1
                    break
            for i in range(ChessMain.DIMENSION):
                if mouse_x-1-i >=0 and gs.board[mouse_y][mouse_x-1-i] != "--":
                    left_obstacle = i+1
                    break
            for i in range(ChessMain.DIMENSION):
                if mouse_y+1+i <8 and gs.board[mouse_y+1+i][mouse_x] != "--":
                    bottom_obstacle = i+1
                    break
            for i in range(ChessMain.DIMENSION):
                if mouse_y-1-i >=0 and gs.board[mouse_y-1-i][mouse_x] != "--":
                    top_obstacle = i+1
                    break
            
        if "x" in movement:
            for i in range(ChessMain.DIMENSION):
                if mouse_x+1+i < 8 and mouse_y+1+i < 8 and gs.board[mouse_y+1+i][mouse_x+1+i] != "--":
                    bottom_right_obstacle = i+1
                    break
            for i in range(ChessMain.DIMENSION):
                if mouse_x-1-i >= 0 and mouse_y+1+i < 8 and gs.board[mouse_y+1+i][mouse_x-1-i] != "--":
                    bottom_left_obstacle = i+1
                    break
            for i in range(ChessMain.DIMENSION):
                if mouse_x+1+i < 8 and mouse_y-1-i >= 0 and gs.board[mouse_y-1-i][mouse_x+1+i] != "--":
                    top_right_obstacle = i+1
                    break
            for i in range(ChessMain.DIMENSION):
                if mouse_x-1-i < 8 and mouse_y-1-i >= 0 and gs.board[mouse_y-1-i][mouse_x-1-i] != "--":
                    top_left_obstacle = i+1
                    break
            
        return right_obstacle, left_obstacle, top_obstacle, bottom_obstacle, bottom_right_obstacle, bottom_left_obstacle, top_right_obstacle, top_left_obstacle
