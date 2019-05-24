import pygame, sys, time
from pygame.locals import QUIT
BLUE=(0,0,155)
WHITE=(255,255,255)
GREY=(217,222,226)
BOX_SIZE=20
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
BOARD_WIDTH=10

def run():
    pygame.init()
    window_size = (SCREEN_WIDTH,SCREEN_HEIGHT)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Tetris')
    game_matrix = create_game_matrix()
    last_time_move = time.time()
    piece = create_piece()
    while True:
        screen.fill((0,0,0))
        if(time.time()-last_time_move>1):
            piece['row'] += 1
            last_time_move = time.time()
        draw_piece(screen,piece)
        pygame.draw.rect(screen,BLUE,[100,50,10*20,20*20+10],5)
        draw_board(screen,game_matrix)
        if(piece['row']==19 or game_matrix[piece['row']+1][piece['column']]!='.'):
            game_matrix[piece['row']][piece['column']] = 'c'
            piece=create_piece()
        pygame.display.update()
        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

def draw_board(screen,matrix):
    matrix_row = 20
    matrix_column = 10
    for row in range(matrix_row):
        for column in range(matrix_column):
            if(matrix[row][column] == 'c'):
                draw_single_piece(screen,row,column,WHITE,GREY)

def create_piece():
    piece = {}
    piece['row'] = 0
    piece['column'] = 4
    return piece

def draw_single_piece(screen,row,column,color,color2):
    origin_x = 100+5+(column*20+1)
    origin_y = 50+5+(row*20+1)
    pygame.draw.rect(screen,color,[origin_x,origin_y,20,20])
    pygame.draw.rect(screen,color2,[origin_x,origin_y,18,18])

def draw_piece(screen,piece):
    origin_x = 100+5+(piece['column']*20+1)
    origin_y = 50+5+(piece['row']*20+1)
    pygame.draw.rect(screen,GREY,[origin_x,origin_y,20,20])
    pygame.draw.rect(screen,WHITE,[origin_x,origin_y,18,18])

def create_game_matrix():
    game_matrix_columns = 10
    game_matrix_rows = 20
    matrix = []
    for row in range(game_matrix_rows):
        new_row = []
        for column in range(game_matrix_columns):
            new_row.append('.')
        matrix.append(new_row)
    return matrix
run()
