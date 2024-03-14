import random
import pygame

# Initialize Pygame
pygame.init()

# Set up game window
WIDTH = 400
HEIGHT = 800
BLOCK_SIZE = 40
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
GAME_SPEED = 500

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
colors = [RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN]

# Set up fonts
font = pygame.font.Font(None, 36)

# Define game functions
def new_piece():
    shape = random.choice([
        [[1, 1, 1, 1]],
        [[1, 1], [1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[1, 1, 0], [0, 1, 1]],
        [[1, 0, 0], [1, 1, 1]],
        [[0, 0, 1], [1, 1, 1]],
        [[1, 0, 0], [1, 0, 0], [1, 1, 1]]
    ])
    color = random.choice(colors)
    piece = {'shape': shape, 'color': color, 'x': BOARD_WIDTH//2-len(shape[0])//2, 'y': 0}
    return piece

def check_collision(board, piece, offset):
    for y, row in enumerate(piece['shape']):
        for x, col in enumerate(row):
            if col != 0:
                board_x = piece['x'] + x + offset[0]
                board_y = piece['y'] + y + offset[1]
                if not (0 <= board_x < BOARD_WIDTH and 0 <= board_y < BOARD_HEIGHT and board[board_y][board_x] == 0):
                    return True
    return False

def merge_piece(board, piece):
    for y, row in enumerate(piece['shape']):
        for x, col in enumerate(row):
            if col != 0:
                board[piece['y'] + y][piece['x'] + x] = piece['color']

def check_lines(board):
    lines_cleared = 0
    for y, row in enumerate(board):
        if all(col != 0 for col in row):
            board.pop(y)
            board.insert(0, [0] * BOARD_WIDTH)
            lines_cleared += 1
    return lines_cleared

def draw_piece(piece):
    for y, row in enumerate(piece['shape']):
        for x, col in enumerate(row):
            if col != 0:
                rect = pygame.Rect((piece['x'] + x) * BLOCK_SIZE, (piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, piece['color'], rect)

def draw_board(board):
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if isinstance(col, tuple):
                # Check if col is a tuple (color)
                pygame.draw.rect(screen, col, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif col > 0:
                # Otherwise, col represents a filled cell
                pygame.draw.rect(screen, colors[1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

""" def draw_board(board):
    for y, row in enumerate(board):
        # print(f"this is the board {list(enumerate(board))}")
        for x, col in enumerate(row):
            # print(f"this is the row {list(enumerate(row))}")
            # print(f"what is col value? {col}")
            if col > 0:
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, colors[1],rect)
                print(f"is it happening {col}")
    # print(f"what is x,y value? {x},{y}\n") """
                               

def draw_text(text, x, y):
    surface = font.render(text, True, WHITE)
    rect = surface.get_rect()
    rect.midtop = (x, y)
    screen.blit(surface, rect)

# Set up game variables
board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
piece = new_piece()
game_over = False
last_drop_time = pygame.time.get_ticks()

# Set up game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')

score=0

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(board, piece, (-1, 0)):
                    piece['x'] -= 1
            if event.key == pygame.K_RIGHT:
                if not check_collision(board, piece, (1, 0)):
                    piece['x'] += 1
            if event.key == pygame.K_UP:
                rotated_shape = [[piece['shape'][y][x] for y in range(len(piece['shape']))] for x in range(len(piece['shape'][0])-1, -1, -1)]
                if not check_collision(board, {'shape': rotated_shape, 'color': piece['color'], 'x': piece['x'], 'y': piece['y']}, (0, 0)):
                    piece['shape'] = rotated_shape
            if event.key == pygame.K_DOWN:
                if not check_collision(board, piece, (0, 1)):
                    piece['y'] += 1
    
    # Game logic
    
    if not game_over:
        if pygame.time.get_ticks() - last_drop_time > GAME_SPEED:
            if check_collision(board, piece, (0, 1)):
                merge_piece(board, piece)
                lines_cleared = check_lines(board)
                score += lines_cleared * 10
                piece = new_piece()
                if check_collision(board, piece, (0, 0)):
                    game_over = True
            else:
                piece['y'] += 1
                last_drop_time = pygame.time.get_ticks()

    # Draw game objects
    screen.fill(BLACK)
    draw_board(board)
    draw_piece(piece)
    draw_text(f'Score: {score}', WIDTH//2, 10)
    if game_over:
        draw_text('GAME OVER', WIDTH//2, HEIGHT//2)
    pygame.display.update()