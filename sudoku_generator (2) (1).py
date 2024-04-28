import math, random
import pygame, sys
from pygame.locals import *
from board import Board

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = 9
        self.removed_cells = removed_cells
        self.board = [[0] * row_length for i in range(row_length)]
        self.box_length = int(math.sqrt(row_length))

    def get_board(self):
        return self.board

    def print_board(self):
        for i in range(0, len(self.board)):
            for j in self.board[i]:
                print(j, end=" ")
            print()

    def valid_in_row(self, row, num):
        for i in range(self.row_length):
            if self.board[row][i] == num:
                return False
        return True

    def valid_in_col(self, col, num):
        for i in range(self.row_length):
            if (self.board[i][int(col)] == num):
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        if self.valid_in_box(row - row % self.box_length, col - col % self.box_length, num) and self.valid_in_col(col,
                                                                                                                  num) and self.valid_in_row(
                row, num):
            return True
        return False

    def fill_box(self, row_start, col_start):
        list_available = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                while True:
                    random_value = random.randint(1, 9)
                    if random_value in list_available:
                        break
                self.board[i][j] = random_value
                list_available.remove(random_value)

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        count_left = self.removed_cells
        while count_left > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.get_board()[row][col] != 0:
                self.get_board()[row][col] = 0
                count_left -= 1

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

def fill_board(numbers, board):
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if numbers[i][j] != 0:
                board.place_given_number(str(numbers[i][j]), i + 1, j + 1)

# NEW
def set_up_welcome():
    pygame.init()
    welcome_screen = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku Project 4")
    background = pygame.image.load("sudoku.png").convert()
    background = pygame.transform.scale(background, (540, 540))
    welcome_screen.blit(background, (0, 0))

    header_text = pygame.font.SysFont("Times New Roman", 30)
    title = header_text.render("Welcome to Sudoku", True, (21, 70, 255))
    text_rect = title.get_rect()
    text_rect.center = (270, 50)

    select_text = pygame.font.SysFont("Times New Roman", 20)
    select = select_text.render("Select Game Mode:", True, (21, 70, 255))
    select_text_rect = select.get_rect()
    select_text_rect.center = (270, 150)

    easy_text = pygame.font.SysFont("Times New Roman", 30)
    easy = easy_text.render("Easy", True, (0, 0, 0))
    easy_rect = easy.get_rect()
    easy_rect.center = (270, 250)

    medium_text = pygame.font.SysFont("Times New Roman", 30)
    medium = medium_text.render("Medium", True, (0, 0, 0))
    medium_rect = medium.get_rect()
    medium_rect.center = (270, 350)

    hard_text = pygame.font.SysFont("Times New Roman", 30)
    hard = hard_text.render("Hard", True, (0, 0, 0))
    hard_rect = hard.get_rect()
    hard_rect.center = (270, 450)

    title_box = pygame.Rect(text_rect.left - 15, text_rect.top - 15, text_rect.width + 30, text_rect.height + 30)
    pygame.draw.rect(welcome_screen, (201, 169, 123), title_box)
    pygame.draw.rect(welcome_screen, (0, 0, 0), title_box, 3)

    select_box = pygame.Rect(select_text_rect.left - 15, select_text_rect.top - 15, select_text_rect.width + 30,
                             select_text_rect.height + 30)
    pygame.draw.rect(welcome_screen, (177, 182, 177), select_box)
    pygame.draw.rect(welcome_screen, (0, 0, 0), select_box, 3)

    easy_box = pygame.Rect(easy_rect.left - 15, easy_rect.top - 15, easy_rect.width + 30, easy_rect.height + 30)
    pygame.draw.rect(welcome_screen, (145, 186, 156), easy_box)
    pygame.draw.rect(welcome_screen, (0, 0, 0), easy_box, 3)

    medium_box = pygame.Rect(medium_rect.left - 15, medium_rect.top - 15, medium_rect.width + 30,
                             medium_rect.height + 30)
    pygame.draw.rect(welcome_screen, (229, 215, 126), medium_box)
    pygame.draw.rect(welcome_screen, (0, 0, 0), medium_box, 3)

    hard_box = pygame.Rect(hard_rect.left - 15, hard_rect.top - 15, hard_rect.width + 30, hard_rect.height + 30)
    pygame.draw.rect(welcome_screen, (169, 97, 97), hard_box)
    pygame.draw.rect(welcome_screen, (0, 0, 0), hard_box, 3)

    welcome_screen.blit(title, text_rect)
    welcome_screen.blit(select, select_text_rect)
    welcome_screen.blit(easy, easy_rect)
    welcome_screen.blit(medium, medium_rect)
    welcome_screen.blit(hard, hard_rect)
    pygame.display.update()




    global values
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    game_board = pygame.display.set_mode((540, 620))
                    game_board.fill((255, 255, 255))
                    the_board = Board(540, 540, game_board, "Easy")
                    the_board.draw()
                    values = generate_sudoku(9, 30)
                    fill_board(values, the_board)
                    buttons_board(game_board)
                    check_for_inputs(the_board)
                if medium_rect.collidepoint(event.pos):
                    game_board = pygame.display.set_mode((540, 620))
                    game_board.fill((255, 255, 255))
                    the_board = Board(540, 540, game_board, "Medium")
                    the_board.draw()
                    values = generate_sudoku(9, 40)
                    fill_board(values, the_board)
                    buttons_board(game_board)  # Add buttons rendering for Medium mode
                    check_for_inputs(the_board)
                if hard_rect.collidepoint(event.pos):
                    game_board = pygame.display.set_mode((540, 620))
                    game_board.fill((255, 255, 255))
                    the_board = Board(540, 540, game_board, "Hard")
                    the_board.draw()
                    values = generate_sudoku(9, 50)
                    fill_board(values, the_board)
                    buttons_board(game_board)  # Add buttons rendering for Hard mode
                    check_for_inputs(the_board)
    pygame.quit()




def buttons_board(board):
    # buttons for clearing the board/ Justin Oh
    clear_cell = pygame.font.SysFont("Times New Roman", 20)
    reset_cell = pygame.font.SysFont("Times New Roman", 20)
    exit_cell = pygame.font.SysFont("Times New Roman", 20)  # New font for Exit button

    clear = clear_cell.render("Reset", True, (0, 0, 0))
    reset = reset_cell.render("Restart", True, (0, 0, 0))
    exit_game = exit_cell.render("Exit", True, (0, 0, 0))  # Render the "Exit" button

    clear_rect = clear.get_rect()
    reset_rect = reset.get_rect()
    exit_rect = exit_game.get_rect()  # Get rect for the "Exit" button

    # Calculate positions for buttons
    button_height = clear_rect.height + 30
    button_width = clear_rect.width + 30
    window_width, window_height = board.get_width(), board.get_height()
    clear_x = (window_width - button_width * 3) // 4
    reset_x = clear_x * 2 + button_width
    exit_x = reset_x + clear_x + button_width
    button_y = window_height - button_height - 15

    # Draw rectangles for buttons
    clear_box = pygame.Rect(clear_x, button_y, button_width, button_height)
    pygame.draw.rect(board, (177, 182, 177), clear_box)
    pygame.draw.rect(board, (0, 0, 0), clear_box, 3)

    reset_box = pygame.Rect(reset_x, button_y, button_width, button_height)
    pygame.draw.rect(board, (177, 182, 177), reset_box)
    pygame.draw.rect(board, (0, 0, 0), reset_box, 3)

    exit_box = pygame.Rect(exit_x, button_y, button_width, button_height)  # Rect for "Exit" button
    pygame.draw.rect(board, (177, 182, 177), exit_box)  # Draw "Exit" button
    pygame.draw.rect(board, (0, 0, 0), exit_box, 3)  # Draw border for "Exit" button

    # Display buttons
    board.blit(clear, clear_rect.move(clear_x + 15, button_y + 15))
    board.blit(reset, reset_rect.move(reset_x + 15, button_y + 15))
    board.blit(exit_game, exit_rect.move(exit_x + 15, button_y + 15))  # Display "Exit" button
    pygame.display.update()

    # Handle button clicks
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if clear_box.collidepoint(position):
                    # Logic for clearing the board
                    board.clear_board()  # Implement the function to clear the board
                elif reset_box.collidepoint(position):
                    # Go back to the home screen
                    set_up_welcome()
                    running = False
                elif exit_box.collidepoint(position):  # Check if "Exit" button is clicked
                    pygame.quit()  # Quit the game





def check_for_inputs(board):
    global values
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                cell_clicked = board.click(position[0], position[1])
                if cell_clicked:
                    board.select(cell_clicked[0], cell_clicked[1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    board.clear((board.click(position[0], position[1])))
                elif "1" <= event.unicode <= "9" and cell_clicked:
                    number = event.unicode
                    board.sketch(number, cell_clicked)
                elif event.key == pygame.K_RETURN:
                    for i in board.list_of_cells:
                        if i.col == cell_clicked[1] and i.row == cell_clicked[0]:
                            i.set_cell_value(i.value)
                            i.set_sketched_value(None)
                            board.place_number(i.value, cell_clicked[0], cell_clicked[1])
                            board.change_screen()
    pygame.quit()





if __name__ == "__main__":
    set_up_welcome()
