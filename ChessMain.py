import pygame as p
import ChessEngine
import FadCustom


WIDTH = HEIGHT = 400
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animation, maybe later on idk
IMAGES = {}

'''Initialize the images'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ',
              'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.image.load("Chess/images/"+piece+".png")

'''Initialize the driver, user input and update the graphics/pics. THE MAIN'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    screen.fill(p.Color("grey"))
    gs = ChessEngine.GameState()    # Gamestate function, coming from the ChessEngine folder imported.
    clock = p.time.Clock()  #setup the clock
    
    loadImages() # p.image.load. ps: only do once, before looping.

    mouse_clicked = 0

    #the running part
    running = True
    while running:
        for e in p.event.get():
                if e.type == p.QUIT:
                     running = False
                elif e.type == p.MOUSEBUTTONDOWN:   
                     if e.button == 1:
                          mouse_clicked += 1
                          if mouse_clicked == 1:
                               mouse_clicked = FadCustom.Move.movement_pickup()
                          elif mouse_clicked == 2:
                               gs, hasMoved, mouse_clicked = FadCustom.Move.movement_drop()
                               print(hasMoved)
      
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()



'''The functions'''
# drawGameState update the graphics etc, the main item to update the state/pic of the current game
def drawGameState(screen,gs):
     drawBoard(screen) #running p.draw.rect, for each square
     drawPieces(screen,gs.board) #running screen.blit, this function commonly used to write on top of the screen/board

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


if __name__ == "__main__":
     main()
