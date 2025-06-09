import pygame
import sys
from stockfish import Stockfish

## StockFish Engine and other Paths
STOCKFISH_PATH = "./learning pygame/NeuroChess/stockfish1/stockfish-windows-x86-64-avx2.exe"
IMAGE_PATH = "./learning pygame/NeuroChess/pieces/"
QUEEN_LOGO = './learning pygame/NeuroChess/images/queen-logo.webp'
SETTING_ICON_PATH = './learning pygame/NeuroChess/images/settings.png'
MOVES_TEXT_FILE = "./learning pygame/NeuroChess/storage/moves.txt"
GAME_HISTORY_PATH = "./learning pygame/NeuroChess/storage/game_history.txt"
FONT1_PATH = './learning pygame/NeuroChess/fonts/BarberChop.otf'
FONT2_PATH = './learning pygame/NeuroChess/fonts/BarberChop.otf'

# Settings
STATE_MAIN_MENU = "main-menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game-over"
STATE_SETTINGS = "settings"
STATE_SETTINGS_GAME = "settings-game"
WIDTH, HEIGHT = 600, 600
SQ_SIZE = WIDTH // 8
PIECES = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK',
          'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
MAIN_MENU_COLOR = ("#181616")
TEXT_COLOR = ("#603232")
PLAY_BUTTON_COLOR = [("white"), ("#603232")]
BLACK_SQUARE_COLOR = "#B58863"
WHITE_SQUARE_COLOR = "#F0D9B5"

## Chess Board ##
def load_images():
    images = {}
    for piece in PIECES:
        img = pygame.image.load(f"./{IMAGE_PATH}{piece}.png")
        images[piece] = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))
    return images

def draw_board(screen):
    colors = [WHITE_SQUARE_COLOR, BLACK_SQUARE_COLOR]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board, images):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

## Piece Move hints ##
def draw_possible_moves(screen, targets):
    for (row, col) in targets:
        center_x = col * SQ_SIZE + SQ_SIZE//2
        center_y = row * SQ_SIZE + SQ_SIZE//2
        pygame.draw.circle(screen, (100, 200, 100), (center_x, center_y), 10)

def draw_selected_square(screen, selected_square):
    if selected_square is not None:
        row, col = selected_square
        rect = pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, (0, 255, 0), rect, 4)  # 4 is the thickness

def get_board_from_fen(fen):
    rows = fen.split()[0].split('/')
    board = []
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                board_row += ["--"] * int(char)
            else:
                color = 'w' if char.isupper() else 'b'
                piece = char.upper()
                board_row.append(color + piece)
        board.append(board_row)
    return board

def get_legal_moves(stockfish):
    moves = stockfish.get_top_moves(100)
    return [move['Move'] for move in moves]

### |--MAIN MENU DESIGN--| ###

## Logo Image ##
def logo(screen):
    logo = pygame.image.load(QUEEN_LOGO).convert_alpha()
    logo = pygame.transform.scale(logo, (200, 200))
    logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(logo, logo_rect)

## Main Menu Text##

def draw_main_menu_text(screen, font):
    title_text = font.render("NeuroChess", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 225))
    screen.blit(title_text, title_rect)

## PLAY BUTTON ##
def play_button(display, font):
    play_button_rect = pygame.draw.rect(display, PLAY_BUTTON_COLOR[1], (WIDTH // 2 - 75, HEIGHT // 2 + 115, 150, 60), 0, 20)

    play_button = font.render("Play", True, PLAY_BUTTON_COLOR[0])
    play_button_rect_text = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
    display.blit(play_button, play_button_rect_text)

    return play_button_rect_text, play_button_rect

def settings(screen):
    setting_icon = pygame.image.load(SETTING_ICON_PATH).convert_alpha()
    setting_icon = pygame.transform.scale(setting_icon, (50, 50))
    setting_icon_rect = setting_icon.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 225))
    screen.blit(setting_icon, setting_icon_rect)

    return setting_icon_rect

def difficulty(screen, font2):
    difficulty_text = font2.render("Difficulty:", True, TEXT_COLOR)
    difficulty_text_rect = difficulty_text.get_rect(center=(WIDTH // 2 - 220, HEIGHT // 2 - 165))
    screen.blit(difficulty_text, difficulty_text_rect)

    easy_button_rect = pygame.draw.rect(screen, PLAY_BUTTON_COLOR[1], (WIDTH // 2 - 145, HEIGHT // 2 - 193, 120, 50), 0, 20)
    easy_button = font2.render("Easy", True, PLAY_BUTTON_COLOR[0])
    easy_button_rect_text = easy_button.get_rect(center=(WIDTH // 2 - 80, HEIGHT // 2 - 165))
    screen.blit(easy_button, easy_button_rect_text)

    medium_button_rect = pygame.draw.rect(screen, PLAY_BUTTON_COLOR[1], (WIDTH // 2 - 5, HEIGHT // 2 - 193, 120, 50), 0, 20)
    medium_button = font2.render("Medium", True, PLAY_BUTTON_COLOR[0])
    medium_button_rect_text = medium_button.get_rect(center=(WIDTH // 2 + 55, HEIGHT // 2 - 165))
    screen.blit(medium_button, medium_button_rect_text)
    
    hard_button_rect = pygame.draw.rect(screen, PLAY_BUTTON_COLOR[1], (WIDTH // 2 + 135, HEIGHT // 2 - 193, 120, 50), 0, 20)
    hard_button = font2.render("Hard", True, PLAY_BUTTON_COLOR[0])
    hard_button_rect_text = hard_button.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 - 165))
    screen.blit(hard_button, hard_button_rect_text)

    return easy_button_rect, easy_button_rect_text, medium_button_rect, medium_button_rect_text, hard_button_rect, hard_button_rect_text

def back(screen, font2):
    back_button = font2.render("<-", True, TEXT_COLOR)
    back_button_rect = back_button.get_rect(topright=(40, 10))
    screen.blit(back_button, back_button_rect)

    return back_button_rect

def move_assist(screen, font2):
    move_assist_text = font2.render("Move Assist:", True, TEXT_COLOR)
    move_assist_text_rect = move_assist_text.get_rect(center=(WIDTH // 2 - 210, HEIGHT // 2 - 85))
    screen.blit(move_assist_text, move_assist_text_rect)

    on_btn = pygame.draw.rect(screen, PLAY_BUTTON_COLOR[1], (WIDTH // 2 - 125, HEIGHT // 2 - 113, 120, 50), 0, 20)
    on_btn_text = font2.render("ON", True, PLAY_BUTTON_COLOR[0])
    on_btn_text_rect = on_btn_text.get_rect(center=(WIDTH // 2 - 65, HEIGHT // 2 - 85))
    screen.blit(on_btn_text, on_btn_text_rect)

    off_btn = pygame.draw.rect(screen, PLAY_BUTTON_COLOR[1], (WIDTH // 2 + 10, HEIGHT // 2 - 113, 120, 50), 0, 20)
    off_btn_text = font2.render("OFF", True, PLAY_BUTTON_COLOR[0])
    off_btn_text_rect = off_btn_text.get_rect(center=(WIDTH // 2 + 67, HEIGHT // 2 - 85))
    screen.blit(off_btn_text, off_btn_text_rect)

    return on_btn, on_btn_text_rect, off_btn, off_btn_text_rect

def instructions(screen, font2):
    move_assist_text = font2.render("While In Game:", True, TEXT_COLOR)
    move_assist_text_rect = move_assist_text.get_rect(topright=(195, HEIGHT // 2 - 15))
    screen.blit(move_assist_text, move_assist_text_rect)

    move_assist_text = font2.render("(ESC) Quit Game", True, TEXT_COLOR)
    move_assist_text_rect = move_assist_text.get_rect(topright=(450, HEIGHT // 2 - 15))
    screen.blit(move_assist_text, move_assist_text_rect)

    move_assist_text = font2.render("(TAB) Open Settings", True, TEXT_COLOR)
    move_assist_text_rect = move_assist_text.get_rect(topright=(500, HEIGHT // 2 + 35))
    screen.blit(move_assist_text, move_assist_text_rect)

def archive_game():
    moves_path = MOVES_TEXT_FILE
    archive_path = GAME_HISTORY_PATH

    try:
        with open(moves_path, "r") as f:
            moves = f.read().strip()
    except FileNotFoundError:
        return
    def get_next_game_num(archive_path):
        try:
            with open(archive_path, "r") as f:
                lines = f.readlines()
            game_lines = [line for line in lines if line.startswith("Game ")]
            return len(game_lines) + 1
        except FileNotFoundError:
            return 1

    game_num = get_next_game_num(archive_path)

    with open(archive_path, "a") as f:
        f.write(f"Game {game_num}:\n{moves}\n\n")

    open(moves_path, "w").close()



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neuro Chess")
    clock = pygame.time.Clock()
    images = load_images()
    font = pygame.font.Font(FONT1_PATH, 50)
    font2 = pygame.font.Font(FONT2_PATH, 30)
    set_depth = 4
    set_skill = 5

    stockfish = Stockfish(path=STOCKFISH_PATH, depth=set_depth) # 6 -> fast 15 -> slow (Tested personally)
    stockfish.set_skill_level(set_skill) # 0 to 20

    state = STATE_MAIN_MENU
    selected_square = None
    possible_targets = []
    ai_think_pending = False
    assistance = True
    turn = 'w'

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
    default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
    board = get_board_from_fen(fen)
    stockfish.set_fen_position(fen)
    winner = None

    play_button_rect_text, play_button_rect = play_button(screen, font)
    setting_icon_rect = settings(screen)
    easy_button_rect, easy_button_rect_text, medium_button_rect, medium_button_rect_text, hard_button_rect, hard_button_rect_text = difficulty(screen, font)
    back_button_rect = back(screen, font2)
    on_btn, on_btn_text_rect, off_btn, off_btn_text_rect = move_assist(screen, font)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == STATE_MAIN_MENU:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    state = STATE_PLAYING
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_rect_text.collidepoint(event.pos) or play_button_rect.collidepoint(event.pos):
                        state = STATE_PLAYING
                    elif setting_icon_rect.collidepoint(event.pos):
                        state = STATE_SETTINGS


            elif state == STATE_PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN and turn == 'w':
                    x, y = pygame.mouse.get_pos()
                    col, row = x // SQ_SIZE, y // SQ_SIZE
                    
                    if selected_square:
                        # Attempt to make move
                        from_row, from_col = selected_square
                        move = f"{chr(from_col+97)}{8-from_row}{chr(col+97)}{8-row}"
                        legal_moves = get_legal_moves(stockfish)   
                        
                        if move in legal_moves:
                            with open(MOVES_TEXT_FILE, "a") as f:
                                f.write(move + "\n") 
                            stockfish.make_moves_from_current_position([move])
                            fen = stockfish.get_fen_position()
                            board = get_board_from_fen(fen)
                            turn = 'b'
                            selected_square = None
                            possible_targets.clear()
                            ai_think_pending = True
                        else:
                            selected_square = None
                            possible_targets.clear()
                    else:
                        # Select piece and show possible moves
                        if board[row][col] != "--" and board[row][col][0] == turn:
                            selected_square = (row, col)
                            # Calculate possible moves
                            start_col = chr(selected_square[1] + 97)
                            start_rank = 8 - selected_square[0]
                            start_uci = f"{start_col}{start_rank}"
                            legal_moves = get_legal_moves(stockfish)
                            possible_moves = [move for move in legal_moves if move.startswith(start_uci)]
                            
                            # Convert to target positions
                            possible_targets.clear()
                            for move in possible_moves:
                                end_uci = move[2:4]
                                end_col = ord(end_uci[0]) - ord('a')
                                end_rank = int(end_uci[1])
                                end_row = 8 - end_rank
                                possible_targets.append((end_row, end_col))
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MAIN_MENU
                        stockfish.set_fen_position(default_fen)
                        board = get_board_from_fen(default_fen)
                        archive_game()
                    
                    elif event.key == pygame.K_TAB:
                        state = STATE_SETTINGS_GAME
                
                
            elif state == STATE_SETTINGS or state == STATE_SETTINGS_GAME:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if state == STATE_SETTINGS:
                        if back_button_rect.collidepoint(event.pos):
                            state = STATE_MAIN_MENU
                    elif state == STATE_SETTINGS_GAME:
                            if back_button_rect.collidepoint(event.pos):
                                state = STATE_PLAYING

                    if easy_button_rect.collidepoint(event.pos) or easy_button_rect_text.collidepoint(event.pos):
                        set_depth = 4
                        set_skill = 5
                        stockfish = Stockfish(path=STOCKFISH_PATH, depth=set_depth)
                        stockfish.set_skill_level(set_skill)
                        stockfish.set_fen_position(default_fen)
                        board = get_board_from_fen(default_fen)
                        
                    elif medium_button_rect.collidepoint(event.pos) or medium_button_rect_text.collidepoint(event.pos):
                        set_depth = 8
                        set_skill = 12
                        stockfish = Stockfish(path=STOCKFISH_PATH, depth=set_depth)
                        stockfish.set_skill_level(set_skill)
                        stockfish.set_fen_position(default_fen)
                        board = get_board_from_fen(default_fen)
                         

                    elif hard_button_rect.collidepoint(event.pos) or hard_button_rect_text.collidepoint(event.pos):
                        set_depth = 12
                        set_skill = 20
                        stockfish = Stockfish(path=STOCKFISH_PATH, depth=set_depth)
                        stockfish.set_skill_level(set_skill)
                        stockfish.set_fen_position(default_fen)
                        board = get_board_from_fen(default_fen)
                        
                    
                    elif on_btn.collidepoint(event.pos) or on_btn_text_rect.collidepoint(event.pos):
                        assistance = True

                    elif off_btn.collidepoint(event.pos) or off_btn_text_rect.collidepoint(event.pos):
                        assistance = False
        # Drawing
        screen.fill((0, 0, 0))
        if state == STATE_MAIN_MENU:
            ## BACKGROUND COLOR ##
            screen.fill(MAIN_MENU_COLOR)

            ## MENU CONTENTS ##
            logo(screen)
            draw_main_menu_text(screen, font)
            play_button(screen, font)
            settings(screen)

        elif state == STATE_PLAYING:
            draw_board(screen)
            if selected_square:
                draw_selected_square(screen, selected_square)
            draw_pieces(screen, board, images)
            if selected_square and assistance:
                draw_possible_moves(screen, possible_targets)
            
            if ai_think_pending and turn == 'b':
                pygame.display.flip()
                pygame.time.delay(100)
                ai_move = stockfish.get_best_move()
                with open(MOVES_TEXT_FILE, "a") as f:
                            f.write(ai_move + "\n")  
                if ai_move:
                    stockfish.make_moves_from_current_position([ai_move])
                    fen = stockfish.get_fen_position()
                    board = get_board_from_fen(fen)
                    turn = 'w'
                ai_think_pending = False

            # Check game over
            if not get_legal_moves(stockfish):
                state = STATE_GAME_OVER
                winner = "White" if turn == 'b' else "Black"
        
        elif state == STATE_GAME_OVER:
            archive_game()
            draw_board(screen)
            draw_pieces(screen, board, images)
            pygame.draw.rect(screen, PLAY_BUTTON_COLOR[1], (20, HEIGHT // 2 - 50, WIDTH - 40, HEIGHT // 2 - 100), 0, 20)
            if winner is not None:
                text = font.render(f"Game Over! {winner} wins", True, (255, 0, 0))
            else:
                text = font.render(f"Game Over! It's a draw!", True, (255, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            text = font2.render("Press ENTER for Main Menu", True, (200, 200, 200))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 60))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
                board = get_board_from_fen(fen)
                stockfish.set_fen_position(fen)
                turn = 'w'
                state = STATE_MAIN_MENU
        
        elif state == STATE_SETTINGS or state == STATE_SETTINGS_GAME:
            screen.fill(MAIN_MENU_COLOR)
            back(screen, font2)
            difficulty(screen, font2)
            move_assist(screen, font2)
            instructions(screen, font2)
            



        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
