import pygame, sys
from pygame.locals import QUIT
BLUE=(0,0,155)
BOX_SIZE=20
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
BOARD_WIDTH=10
def run():
    pygame.init()
    window_size=(SCREEN_WIDTH,SCREEN_HEIGHT)
    screen=pygame.display.set_mode(window_size)
    pygame.display.set_caption('Tetris')
    game_matrix = create_game_matrix()
    while True:
        screen.fill((0,0,0))
        pygame.draw.rect(screen,BLUE,[100,50,10*20,20*20],5)
        pygame.display.update()
        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
def create_game_matrix():
    game_matrix_columns=10
    game_matrix_rows=20
    matrix=[]
    return matrix
run()
