import pygame, sys, time
from pygame.locals import QUIT
BLUE=(0,0,155)
WHITE=(255,255,255)
GREY=(217,222,226)
BOX_SIZE=20
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
BOARD_WIDTH=10

REV_Z_SHAPE = [['.....'
                '.....'
                '..cc.'
                '.cc..'
                '.....']]
Z_SHAPE = [['.....'
            '.....'
            '.cc..'
            '..cc.'
            '.....']]

I_SHAPE = [['..c..'
            '..c..'
            '..c..'
            '..c..'
            '.....']]

L_SHAPE = [['..c..'
            '..c..'
            '..c..'
            '..ccc'
            '.....']]

BOX_SHAPE = [['.....'
              '.....'
              '.cc..'
              '.cc..'
              '.....']]

def run():
    pygame.init()
    window_size = (SCREEN_WIDTH,SCREEN_HEIGHT)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Tetris')
    game_matrix = create_game_matrix()
    last_time_move = time.time()
    piece = create_piece()
    score = 0
    while True:
        screen.fill((0,0,0))
        #moving piece
        if(time.time()-last_time_move>1):
            piece['row'] += 1
            last_time_move = time.time()
        draw_piece(screen,piece)
        pygame.draw.rect(screen,BLUE,[100,50,10*20+10,20*20+10],5)
        draw_board(screen,game_matrix)
        show_score(screen,score)
        #taking user input left or right
        listen_to_user_input(game_matrix,piece)
        #checking if piece is going out of board or collison with existing piece
        if(piece['row']==19 or game_matrix[piece['row']+1][piece['column']]!='.'):
            game_matrix[piece['row']][piece['column']] = 'c'
            lines_removed=remove_line(game_matrix)
            score += lines_removed
            piece=create_piece()
        pygame.display.update()
        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

def show_score(screen,score):
    myfont = pygame.font.Font('freesansbold.ttf',18)
    text_surface = myfont.render('Score: %s' % score,True,WHITE)
    screen.blit(text_surface,(500,20))

def listen_to_user_input(game_matrix,piece):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if(event.key== pygame.K_LEFT and valid_position(game_matrix,piece['row'],piece['column']-1)):
                piece['column'] -= 1
            elif(event.key == pygame.K_RIGHT and valid_position(game_matrix,piece['row'],piece['column']+1)):
                piece['column'] +=1
            elif(event.key == pygame.K_DOWN):
                piece['row'] +=2
            elif(event.key == pygame.K_UP):
                piece['row'] +=1

def remove_line(game_matrix):
    line_removed = 0
    for row in range(20):
        if(line_complete(game_matrix,row)):
            for row_to_shift in range(row,0,-1):
                for column in range(10):
                    game_matrix[row_to_shift][column] = game_matrix[row_to_shift-1][column]
            for i in range(10):
                game_matrix[0][i] = '.'
            line_removed += 1
    return line_removed

def line_complete(game_matrix,row):
    for column in range(10):
        if(game_matrix[row][column] == '.'):
            return False
    return True

def valid_position(game_matrix,row,column):
    if row>19 or column<0 or column>9  or game_matrix[row][column]=='c':
        return False
    return True

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
