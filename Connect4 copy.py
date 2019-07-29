import numpy as np
import random
import pygame
import sys
import math

BLUE = (108, 6, 122)
RED = (221, 39, 0)
YELLOW = (241, 169, 4)
BACKGROUND = (222, 231, 255)
BLACK = (0, 0, 0)  # used for repaint on movement tracking of piece


def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board


def display_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * BLOCK, r * BLOCK + BLOCK, BLOCK, BLOCK))
            pygame.draw.circle(screen, BACKGROUND, (
                int(c * BLOCK + BLOCK / 2), int(r * BLOCK + BLOCK + BLOCK / 2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * BLOCK + BLOCK / 2), S_height - int(r * BLOCK + BLOCK / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * BLOCK + BLOCK / 2), S_height - int(r * BLOCK + BLOCK / 2)), RADIUS)
    pygame.display.update()


def print_board(board):
    print(np.flip(board, 0))


# Intro Menu on console:
def menu():
    print("""CONNECT4:
            Welcome to Connect4 Python! Please sekect your game mode:
            """)
    # specific region is a button
    choice = int(input(
        "\nPress '1' for player 1 VS player 2\nPress '2' for player 1 VS Computer (easy)\nPress '3' for player 1 VS Computer (medium)\n**NOTE: Computer advances upon click\nGame mode: "))
    return choice


def apply_move(board, row, col, piece):
    board[row][col] = piece


def check_move(board, col):
    return board[ROWS - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r


def check_victory(board, piece):
    # Horizontal win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Vertical win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Positive slope diagonales
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Negatively slope diagonales
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def computer_move_easy(turn):
    Col_choice = random.randint(0, 6)
    row = get_next_open_row(board, Col_choice)
    apply_move(board, row, Col_choice, 2)
    if check_victory(board, 2):
        print("Computer WINS!!! GAME OVER")
        label = Font.render("Computer WINS!!! GAME OVER", 2, YELLOW)
        screen.blit(label, (40, 10))
        game_over = True
    turn += 1
    turn = turn % 2
    return turn

def computer_move_med(turn):
    Col_choice = random.randint(0, 6)
    row = get_next_open_row(board, Col_choice)
    apply_move(board, row, Col_choice, 2)
    if check_victory(board, 2):
        print("Computer WINS!!! GAME OVER")
        label = Font.render("Computer WINS!!! GAME OVER", 2, YELLOW)
        screen.blit(label, (40, 10))
        game_over = True
    turn += 1
    turn = turn % 2
    return turn




# Size of board
ROWS = 6
COLUMNS = 7

# State of game
board = create_board()
game_over = False

# Turn of player
turn = 0

# Choice of gameplay on console
Choice = menu()

# Design:
pygame.init()

BLOCK = 100  # Pixels
RADIUS = int(BLOCK / 2 - 5)

S_width = COLUMNS * BLOCK
S_height = (ROWS + 1) * BLOCK
size = (S_width, S_height)

screen = pygame.display.set_mode(size)
display_board(board)
pygame.display.update()

Font = pygame.font.SysFont("monospace", 75)


# Human Vs Human
if Choice == 1:
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, S_width, BLOCK))
                coordinates = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (coordinates, int(BLOCK / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (coordinates, int(BLOCK / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

                # Ask for player 1 input
                if turn == 0:
                    # col = int(input("Player 1 make your selection (1-7):"))
                    # col = col - 1
                    # print(col)
                    # print(type(col))
                    coordinates = event.pos[0]
                    Col_choice = int(math.floor(coordinates / BLOCK))

                    if check_move(board, Col_choice):
                        row = get_next_open_row(board, Col_choice)
                        apply_move(board, row, Col_choice, 1)

                        if check_victory(board, 1):
                            print("PLAYER 1 WINS!!! GAME OVER")
                            label = Font.render("PLAYER 1 WINS!!! GAME OVER", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                # Ask for player 2 input
                else:
                    # col = int(input("Player 2 make your selection (1-7):"))
                    # col = col - 1
                    coordinates = event.pos[0]
                    Col_choice = int(math.floor(coordinates / BLOCK))

                    if check_move(board, Col_choice):
                        row = get_next_open_row(board, Col_choice)
                        apply_move(board, row, Col_choice, 2)

                        if check_victory(board, 2):
                            print("PLAYER 2 WINS!!! GAME OVER")
                            label = Font.render("PLAYER 2 WINS!!! GAME OVER", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                print_board(board)
                display_board(board)

                # change turn of player
                turn += 1
                turn = turn % 2

                # make sure game not close, have time to read msg
                if game_over:
                    pygame.time.wait(5000)

# Human Vs Computer (easy)
elif Choice == 2:
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, S_width, BLOCK))
                coordinates = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (coordinates, int(BLOCK / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (coordinates, int(BLOCK / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(event.pos)

                # Ask for player 1 input
                if turn == 0:

                    coordinates = event.pos[0]
                    Col_choice = int(math.floor(coordinates / BLOCK))

                    if check_move(board, Col_choice):
                        row = get_next_open_row(board, Col_choice)
                        apply_move(board, row, Col_choice, 1)

                        turn += 1
                        turn = turn % 2

                        if check_victory(board, 1):
                            print("\n\n!!!PLAYER 1 WINS!!! GAME OVER")
                            label = Font.render("\n\n\n!!!PLAYER 1 WINS!!! GAME OVER", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        else:
                            computer_move_med(turn)
                            turn += 1
                            turn = turn % 2

                    print_board(board)
                    display_board(board)

                    if game_over:
                        pygame.time.wait(5000)


# Human Vs Computer (medium) This does not work yet

# elif Choice == 3:
#     while not game_over:
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#
#             if event.type == pygame.MOUSEMOTION:
#                 pygame.draw.rect(screen, BLACK, (0, 0, S_width, BLOCK))
#                 coordinates = event.pos[0]
#                 if turn == 0:
#                     pygame.draw.circle(screen, RED, (coordinates, int(BLOCK / 2)), RADIUS)
#                 else:
#                     pygame.draw.circle(screen, YELLOW, (coordinates, int(BLOCK / 2)), RADIUS)
#             pygame.display.update()
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 #print(event.pos)
#
#                 # Ask for player 1 input
#                 if turn == 0:
#
#                     coordinates = event.pos[0]
#                     Col_choice = int(math.floor(coordinates / BLOCK))
#
#                     if check_move(board, Col_choice):
#                         row = get_next_open_row(board, Col_choice)
#                         apply_move(board, row, Col_choice, 1)
#
#                         turn += 1
#                         turn = turn % 2
#
#                         if check_victory(board, 1):
#                             print("PLAYER 1 WINS!!! GAME OVER")
#                             label = Font.render("PLAYER 1 WINS!!! GAME OVER", 1, RED)
#                             screen.blit(label, (40, 10))
#                             game_over = True
#
#                         else:
#                             computer_move_easy(turn)
#                             turn += 1
#                             turn = turn % 2
#
#                 print_board(board)
#                 display_board(board)
#
#                 if game_over:
#                     pygame.time.wait(5000)
