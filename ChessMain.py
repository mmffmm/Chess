import pygame as p
import ChessEngine
import MoveClass as MoveClass
import buttons

import copy


'''Custom value initialized to setup the GUI'''
GAME_WIDTH = 400
HEIGHT = 400
CONTROL_PANEL = 100
WIDTH = GAME_WIDTH + CONTROL_PANEL
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animation, maybe later on idk

IMAGE_DIR = "images/"



'''Initialize the images'''
IMAGES = {}
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ',
              'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.image.load(IMAGE_DIR+piece+".png")



'''Initialize the driver, user input and update the graphics/pics. THE MAIN'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    screen.fill(p.Color("grey"))
    init_gs = ChessEngine.GameState()             # Gamestate function, coming from the ChessEngine folder imported.
    gs = copy.deepcopy(init_gs)
    clock = p.time.Clock()                   #setup the clock
    move = MoveClass.Move(gs, SQ_SIZE)       #init class

    loadImages()                             # p.image.load. ps: only do once, before looping.

    '''LINE START, INITIALIZE THE VALUE RETURNED FROM MoveClass'''
    mouse_clicked = 0
    mouse_x = 'a'
    mouse_y = 'a'
    possible_dropped_square = 'a'
    '''LINE END, INITIALIZE THE VALUE RETURNED FROM MoveClass'''

    restart = drawButton(screen)


    #the running part
    running = True
    while running:
        for e in p.event.get():
                if e.type == p.QUIT:
                     running = False
                elif e.type == p.MOUSEBUTTONDOWN:   
                     if e.button == 1: # if left click. 2 = right click iirc
                          
                          mouse_clicked += 1  # why tf this here, this one functional but looks ugly #REWORK

                          if mouse_clicked == 1:
                              mouse_x, mouse_y = checkPosition()
                              if mouse_x <= GAME_WIDTH and mouse_x>=0 and mouse_y <= HEIGHT and mouse_y >=0:
                                   mouse_clicked, mouse_x, mouse_y, possible_dropped_square = move.movement_pickup(gs,1)
                                   
                              else:
                                   print("outsiddeeee (PICK)") #WIP
                                   print(gs.board)
                                   mouse_clicked, mouse_x, mouse_y, possible_dropped_square, gs = buttons.restartButton(init_gs)

                          elif mouse_clicked == 2:
                              mouse_x, mouse_y = checkPosition()
                              if mouse_x <= GAME_WIDTH and mouse_x>=0 and mouse_y <= HEIGHT and mouse_y >=0:
                                   gs, hasMoved, mouse_clicked = move.movement_drop(gs)
                                   mouse_x = mouse_y = 'a'
                                   print(hasMoved)
                                   print(gs.board)
                              else: print("outsiddeeee (DROP)") #WIP
      
        drawGameState(screen,gs,mouse_x,mouse_y,possible_dropped_square)
        clock.tick(MAX_FPS)
        p.display.flip()



'''The functions'''
# drawGameState update the graphics etc, the main item to update the state/pic of the current game
def drawGameState(screen, gs, mouse_x='a', mouse_y='a', possible_dropped_square = 'a'):

          drawBoard(screen)            #draw board + control panel                                                             #running p.draw.rect, for each square
          if mouse_x != 'a' and mouse_y != 'a':
               if mouse_x <= GAME_WIDTH and mouse_x>=0 and mouse_y <= HEIGHT and mouse_y >=0:
                    drawBoardColor(screen, "green", mouse_x, mouse_y)                                    # colour the pickedup square                                    
                    for square in possible_dropped_square:
                         drawBoardColor(screen, "green", square[1], square[0], 'Y')                      # colour border of possible drop
                    
          if(gs.board): drawPieces(screen,gs.board)                                                               #running screen.blit, this function commonly used to write on top of the screen/board


def drawBoard(screen):
     colors = [p.Color("white"), p.Color("grey")]
     for row in range(DIMENSION):
          for column in range(DIMENSION):
               color = colors[((row+column)%2)] # cause in chess, if row+column is even number, then its white
               #draw rectangle(where is it drawn on, the color, p.Rect(x coordinate, y coordinate, width, height))
               p.draw.rect(screen, color, p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    

# notes: this is doing 2D loops again, not that expensive since only image                  
def drawPieces(screen,board):
     for row in range(DIMENSION):
          for column in range(DIMENSION):
               piece = board[row][column]
               if piece != "--":
                    #blit function is to draw somethin on top of the other board.
                    screen.blit(IMAGES[piece], p.Rect((column-0.1)*SQ_SIZE, (row-0.1)*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # need to -0.1, since the original a bit to the right and bottom


def drawBoardColor(screen, colors, mouse_x, mouse_y, drop_flag='N'):
    
    color = p.Color(colors)

    if drop_flag == 'N':
         p.draw.rect(screen, color, p.Rect(mouse_x*SQ_SIZE, mouse_y*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if drop_flag == 'Y':
         p.draw.rect(screen, color, p.Rect(mouse_x*SQ_SIZE, mouse_y*SQ_SIZE, SQ_SIZE, SQ_SIZE), 5)

def drawButton(screen):
     restart_rect = p.draw.rect(screen, p.Color(0,255,170), p.Rect((HEIGHT+(0.10*(WIDTH-HEIGHT))),
                                                                   (0.10*(WIDTH-HEIGHT)),
                                                                   (0.80*(WIDTH-HEIGHT)),
                                                                   (0.50*(WIDTH-HEIGHT))))
     font = p.font.Font(None, 30) 
     text = font.render('Restart', 0, p.Color('black'))
     text_centre = text.get_rect(center=restart_rect.center)

     screen.blit(text,text_centre)
     
     return restart_rect # this return statement, cant remember why return this. Probably because want to initialize again.

def checkPosition():
     mouse_x, mouse_y = p.mouse.get_pos()
     return mouse_x, mouse_y

if __name__ == "__main__":
     main()