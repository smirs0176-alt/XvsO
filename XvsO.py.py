import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CROSS_COLOR = (66, 66, 66)
CIRCLE_COLOR = (239, 231, 200)

CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

screen = None
board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
player = 1
game_over = False

score = {1: 0, 2: 0}
WIN_SCORE = 3


def terminal_menu():
    print("\n===============================")
    print("      КРЕСТИКИ-НОЛИКИ          ")
    print("===============================")
    print(f" Игра идет до {WIN_SCORE} побед!")
    print(" 1. Начать новую игру")
    print(" 2. Выход")
    print("===============================")
    
    choice = input("Выберите действие (1 или 2): ").strip()
    if choice == '1':
        start_game()
    elif choice == '2':
        print("Выход из игры...")
        sys.exit()
    else:
        print("Неверный ввод, попробуйте снова.")
        terminal_menu()


def init_window():
    global screen
    if screen is None:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Крестики-Нолики (до 3 побед)")


def draw_lines():
    screen.fill(BG_COLOR)
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

            if board[row][col] == 1:
                start_1 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_1 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                start_2 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_2 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)

                pygame.draw.line(screen, CROSS_COLOR, start_1, end_1, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, start_2, end_2, CROSS_WIDTH)

            elif board[row][col] == 2:
                pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)


def mark_square(row, col, player_num):
    board[row][col] = player_num


def is_square_available(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


def check_win(player_num):
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player_num:
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player_num:
            return True

    if board[0][0] == board[1][1] == board[2][2] == player_num:
        return True

    if board[2][0] == board[1][1] == board[0][2] == player_num:
        return True

    return False


def print_score():
    print(f"\n--- ТЕКУЩИЙ СЧЕТ ---")
    print(f" Игрок 1 (Крестики): {score[1]}")
    print(f" Игрок 2 (Нолики)  : {score[2]}")
    print("--------------------")


def reset_round():
    global player, game_over, board
    draw_lines()
    board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
    player = 1
    game_over = False


def start_game():
    global score, game_over, player
    score = {1: 0, 2: 0}
    init_window()
    reset_round()
    
    print("\nИгра началась! Ходите, кликая мышкой в окне Pygame.")
    print("Нажмите R на клавиатуре для перезапуска текущего раунда.")
    print_score()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                terminal_menu()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if is_square_available(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)

                    if check_win(player):
                        game_over = True
                        score[player] += 1
                        draw_figures()
                        pygame.display.update()
                        print(f"\nРаунд выиграл Игрок {player}!")
                        print_score()

                        if score[player] == WIN_SCORE:
                            print(f"\n ПОБЕДИТЕЛЬ МАТЧА — ИГРОК {player}! ")
                            print("Возврат в терминал...")
                            pygame.time.wait(2000)
                            pygame.quit()
                            terminal_menu()
                            return
                        else:
                            print("Нажмите R для следующего раунда.")

                    elif is_board_full():
                        game_over = True
                        draw_figures()
                        pygame.display.update()
                        print("\nНичья в раунде!")
                        print_score()
                        print("Нажмите R для следующего раунда.")

                    player = 2 if player == 1 else 1
                    draw_figures()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_round()

        pygame.display.update()


if __name__ == "__main__":
    terminal_menu()