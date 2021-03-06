import pygame, sys, time, random
BLUE=(0,0,155)
GREEN=(0,255,0)
RED=(255,0,0)
WHITE=(255,255,255)
GREY=(217,222,226)
BOX_SIZE=20
SCREEN_WIDTH=440
SCREEN_HEIGHT=480
BOARD_WIDTH=10

T_SHAPE = [['.....',
            '.....',
            '..c..',
            '.ccc.',
            '.....'],
           ['.....',
            '.....',
            '..c..',
            '..cc.',
            '..c..'],
           ['.....',
            '.....',
            '.ccc.',
            '..c..',
            '.....'],
           ['.....',
            '..c..',
            '.cc..',
            '..c..',
            '.....']]

TWO_DOT_SHAPE = [['.....',
                  '.....',
                  '..cc.',
                  '.....',
                  '.....'],
                  ['.....',
                  '..c..',
                  '..c..',
                  '.....',
                  '.....']]

REV_Z_SHAPE = [['.....',
                '.....',
                '..cc.',
                '.cc..',
                '.....'],
               ['.....',
                '..c..',
                '..cc.',
                '...c.',
                '.....']]

Z_SHAPE = [['.....',
            '.....',
            '.cc..',
            '..cc.',
            '.....'],
           ['.....',
            '...c.',
            '..cc.',
            '..c..',
            '.....']]

I_SHAPE = [['..c..',
            '..c..',
            '..c..',
            '..c..',
            '.....'],
           ['.....',
            '.....',
            'cccc.',
            '.....',
            '.....']]

L_SHAPE = [['.....',
            '..c..',
            '..c..',
            '..ccc',
            '.....'],
           ['.....',
            '.....',
            '.ccc.',
            '.c...',
            '.c...'],
           ['.....',
            '.ccc.',
            '...c.',
            '...c.',
            '.....'],
           ['.....',
            '...c.',
            '...c.',
            '.ccc.',
            '.....']]

BOX_SHAPE = [['.....',
              '.....',
              '.cc..',
              '.cc..',
              '.....']]

def availble_piece():
    return {
        'T':T_SHAPE,
        'D':TWO_DOT_SHAPE,
        'Z':Z_SHAPE,
        'z':REV_Z_SHAPE,
        'I':I_SHAPE,
        'B':BOX_SHAPE,
        'L':L_SHAPE
    }

def run():
    pygame.init()
    window_size = (SCREEN_WIDTH,SCREEN_HEIGHT)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Tetris')
    game_matrix = create_game_matrix()
    last_time_move = time.time()
    piece = create_piece()
    score = 0
    NOW = 0
    DELAY = 0.9
    running = True

    while running:
        screen.fill((0,0,0))
        if score > 5:
            DELAY = 0.85
        elif score > 10:
            DELAY = 0.65
        elif score > 15:
            DELAY = 0.60
        elif score > 20:
            DELAY = 0.55

        if(time.time()-last_time_move > DELAY):
            piece['row'] += 1
            last_time_move = time.time()
        NOW += 1
        NOW %= 4
        if NOW == 0:
            draw_big_piece(screen,piece,WHITE)
        elif NOW == 1:
            draw_big_piece(screen,piece,RED)
        elif NOW == 2:
            draw_big_piece(screen,piece,GREEN)
        else:
            draw_big_piece(screen,piece,BLUE)
        pygame.draw.rect(screen,BLUE,[100,50,10*20+10,20*20+10],5)
        draw_board(screen,game_matrix)
        show_score(screen,score)

        listen_to_user_input(game_matrix,piece)

        if(not valid_position(game_matrix,piece,adjr=1)):
            game_matrix = update_matrix(game_matrix,piece)
            lines_removed = remove_line(game_matrix)
            score += lines_removed
            piece = create_piece()

        pygame.display.update()

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

def create_piece():
    piece = {}
    random_shape = random.choice(list(availble_piece().keys()))
    piece['shape'] = random_shape
    piece['rotation'] = 0
    piece['row'] = 0
    piece['column'] = 2
    return piece

def draw_board(screen,matrix):
    matrix_row = 20
    matrix_column = 10
    for row in range(matrix_row):
        for col in range(matrix_column):
            if(matrix[row][col] == 'c'):
                draw_single_piece(screen,row,col,WHITE,GREY)

def draw_single_piece(screen,row,column,color,color2):
    origin_x = 100+5+(column*20+1)
    origin_y = 50+5+(row*20+1)
    pygame.draw.rect(screen,color,[origin_x,origin_y,20,20])
    pygame.draw.rect(screen,color2,[origin_x,origin_y,18,18])

def draw_big_piece(screen ,piece, color):
    shape_to_draw = availble_piece()[piece['shape']][piece['rotation']]
    for row in range(5):
        for col in range(5):
            if(shape_to_draw[row][col]=='c'):
                draw_single_piece(screen,piece['row']+row,piece['column']+col,GREY,color)

def inside_board(row,column):
    return column >=0 and column < 10 and row < 20

def line_complete(game_matrix,row):
    for column in range(10):
        if(game_matrix[row][column] == '.'):
            return False
    return True

def listen_to_user_input(game_matrix,piece):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit(0)
            elif(event.key== pygame.K_LEFT and valid_position(game_matrix,piece,adjc = -1)):
                piece['column'] -= 1
            elif(event.key == pygame.K_RIGHT and valid_position(game_matrix,piece,adjc = 1)):
                piece['column'] += 1
            elif(event.key == pygame.K_DOWN):
                piece['row'] += 1
            elif(event.key == pygame.K_UP):
                piece['rotation'] = (piece['rotation']+1) % len(availble_piece()[piece['shape']])
                if not valid_position(game_matrix, piece):
                     piece['rotation'] = (piece['rotation']-1) % len(availble_piece()[piece['shape']])
                return

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

def show_score(screen,score):
    myfont = pygame.font.Font('freesansbold.ttf',18)
    text_surface = myfont.render('Score: %s' % score,True,WHITE)
    screen.blit(text_surface,(350,20))

def update_matrix(matrix,piece):
    for row in range(5):
        for col in range(5):
            if(availble_piece()[piece['shape']][piece['rotation']][row][col] == 'c'):
                matrix[piece['row']+row][piece['column']+col] = 'c'
    return matrix

def valid_position(game_matrix,piece,adjc=0,adjr=0):
    piece_matrix = availble_piece()[piece['shape']][piece['rotation']]
    for row in range(5):
        for col in range(5):
            if(piece_matrix[row][col]=='.'):
                continue
            if(not inside_board(piece['row']+row+adjr,piece['column']+col+adjc)):
                return False
            if(game_matrix[piece['row']+row+adjr][piece['column']+col+adjc]=='c'):
                return False
    return True

run()
exit(0)
