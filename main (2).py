import pygame
import sys
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 540, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Constants
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
SELECTED_COLOR = (200, 200, 200)
SQUARE_SIZE = WIDTH // 9
LINE_WIDTH = 2

# Font for displaying numbers
number_font = pygame.font.Font(None, 40)
text_font = pygame.font.Font(None, 40)

# Define the Cell class
class Cell:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.is_selected = False
        self.is_initial = False

    def draw(self, screen):
        # Draw the cell background
        rect = pygame.Rect(self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, SELECTED_COLOR if self.is_selected else BG_COLOR, rect)

        # Draw the cell border
        pygame.draw.rect(screen, LINE_COLOR, rect, LINE_WIDTH)

        # Draw the cell value (number)
        if self.value != 0:
            number_surface = number_font.render(str(self.value), True, TEXT_COLOR)
            center_pos = rect.centerx, rect.centery
            screen.blit(number_surface, number_surface.get_rect(center=center_pos))

    def draw(self, screen):
        # Draw the cell background
        rect = pygame.Rect(self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, SELECTED_COLOR if self.is_selected else BG_COLOR, rect)

        # Draw the cell border
        pygame.draw.rect(screen, LINE_COLOR, rect, LINE_WIDTH)

        # Draw the cell value (number)
        if self.value != 0:
            number_surface = number_font.render(str(self.value), True, TEXT_COLOR)
            center_pos = rect.centerx, rect.centery
            screen.blit(number_surface, number_surface.get_rect(center=center_pos))

# Define the Board class
class Board:
    def __init__(self):
        self.cells = [[Cell(0, row, col) for col in range(9)] for row in range(9)]
        # Store a list of empty cells
        self.empty_cells = []
        self.initial_state = [[0] * 9 for _ in range(9)]

    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)

    def reset(self):
        # Reset only the empty cells to their empty state
        for row, col in self.empty_cells:
            self.cells[row][col].value = 0

# Function to solve a Sudoku puzzle using backtracking
def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if empty_cell is None:
        return True  # Puzzle solved

    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board.cells[row][col].value = num
            if solve_sudoku(board):
                return True
            board.cells[row][col].value = 0  # Backtrack
    return False

# Function to find an empty cell
def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board.cells[row][col].value == 0:
                return row, col
    return None

# Function to check if a move is valid
def is_valid_move(board, row, col, num):
    # Check row
    if any(board.cells[row][j].value == num for j in range(9)):
        return False
    # Check column
    if any(board.cells[i][col].value == num for i in range(9)):
        return False
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board.cells[i][j].value == num:
                return False
    return True

# Check if the board is filled correctly and completely
def is_board_filled_correctly(board):
    for row in range(9):
        if not is_valid_row(board, row) or not is_valid_col(board, row):
            return False
    for subgrid in range(9):
        if not is_valid_subgrid(board, subgrid):
            return False
    return True

# Helper functions to check row, column, and subgrid validity
def is_valid_row(board, row):
    numbers = {board.cells[row][col].value for col in range(9)}
    return len(numbers) == 9 and all(numbers)

def is_valid_col(board, col):
    numbers = {board.cells[row][col].value for row in range(9)}
    return len(numbers) == 9 and all(numbers)

def is_valid_subgrid(board, index):
    start_row, start_col = (index // 3) * 3, (index % 3) * 3
    numbers = {board.cells[i][j].value for i in range(start_row, start_row + 3) for j in range(start_col, start_col + 3)}
    return len(numbers) == 9 and all(numbers)

def fill_random_cells(board, num_filled_cells=25):
    while num_filled_cells > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        # Check if the cell is empty
        if board.cells[row][col].value == 0:
            num = random.randint(1, 9)
            # Check if the move is valid before placing the number
            if is_valid_move(board, row, col, num):
                board.cells[row][col].value = num
                num_filled_cells -= 1

# Function to generate a Sudoku puzzle by randomly removing numbers
def generate_sudoku(difficulty):
    board = Board()

    # Function to fill random cells in the board
    def fill_random_cells():
        num_filled_cells = random.randint(15, 25)
        filled_positions = set()

        while num_filled_cells > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if (row, col) not in filled_positions:
                num = random.randint(1, 9)
                if is_valid_move(board, row, col, num):
                    board.cells[row][col].value = num
                    # Mark the cell as initially placed by the program
                    board.cells[row][col].is_initial = True
                    filled_positions.add((row, col))
                    num_filled_cells -= 1

    # Fill the board randomly and solve it to complete the solution
    fill_random_cells()
    solve_sudoku(board)

    # Adjust difficulty based on the number of empty cells
    difficulty_ranges = {
        "easy": (25, 35),
        "medium": (36, 45),
        "hard": (46, 54)
    }
    empty_cells_range = difficulty_ranges.get(difficulty, (25, 35))
    num_empty_cells = random.randint(*empty_cells_range)

    # Store empty cells and remove cells randomly to set the difficulty
    empty_cells = []
    empty_count = 0
    while empty_count < num_empty_cells:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board.cells[row][col].value != 0:
            # Add the cell to the list of empty cells
            empty_cells.append((row, col))
            board.cells[row][col].value = 0
            # Mark the cell as not initially placed by the program
            board.cells[row][col].is_initial = False
            empty_count += 1

    # Save the empty cells list to the board
    board.empty_cells = empty_cells

    return board


# Function to display the end game screen
def end_game_screen(screen, menu_button):
    screen.fill(BG_COLOR)

    # Displaying the "Congratulations!" text
    congratulations_text = text_font.render("Congratulations!", True, LINE_COLOR)
    text_rect = congratulations_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(congratulations_text, text_rect)

    # Display the menu button
    menu_button.draw(screen)
    pygame.display.update()

    # Wait for the user to click the menu button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                # Check if the menu button is clicked
                if menu_button.is_clicked(pos):
                    return  # Exit the function, returning the user to the difficulty screen

# Define the Button class
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = text_font

    def draw(self, screen):
        pygame.draw.rect(screen, LINE_COLOR, self.rect, LINE_WIDTH)
        pygame.draw.rect(screen, BG_COLOR, self.rect.inflate(-LINE_WIDTH, -LINE_WIDTH))
        text_surface = self.font.render(self.text, True, LINE_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def run_game():
    # Initialization
    selected_cell = None
    running = True

    # Define buttons
    difficulty_buttons = [
        Button("Easy", 50, 50, 100, 50),
        Button("Medium", 200, 50, 100, 50),
        Button("Hard", 350, 50, 100, 50)
    ]

    reset_button = Button("Reset (R)", 50, 500, 100, 30)
    exit_button = Button("Exit", 390, 500, 100, 30)
    menu_button = Button("Menu", 220, 500, 100, 30)  # Menu button position and size

    current_board = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

                # Event handling when the board is created and game is in progress
                if current_board:
                    # Handle number input and other key events
                    if selected_cell:
                        row, col = selected_cell.row, col
                        # Only allow changing cells that were not initially placed by the program
                        if not current_board.cells[row][col].is_initial:
                            if event.unicode.isdigit():
                                num = int(event.unicode)
                                if is_valid_move(current_board, row, col, num):
                                    current_board.cells[row][col].value = num
                                elif event.key == pygame.K_0:
                                    current_board.cells[row][col].value = 0
                            elif event.key == pygame.K_r:
                                current_board.reset()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                # Check for button clicks
                if current_board is None:
                    for button in difficulty_buttons:
                        if button.is_clicked(pos):
                            current_board = generate_sudoku(button.text.lower())
                            break
                else:
                    # Check for reset button click
                    if reset_button.is_clicked(pos):
                        current_board.reset()  # Reset the board

                    # Check for exit button click
                    if exit_button.is_clicked(pos):
                        running = False
                        break

                    # Check for menu button click
                    if menu_button.is_clicked(pos):
                        current_board = None  # Reset the board, returning to the difficulty screen
                        break

                    # Check for cell selection
                    col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                    if 0 <= col < 9 and 0 <= row < 9:
                        selected_cell = current_board.cells[row][col]
                        # Deselect all other cells
                        for r in current_board.cells:
                            for cell in r:
                                cell.is_selected = False
                        selected_cell.is_selected = True

        # Draw everything
        screen.fill(BG_COLOR)

        # Draw buttons if the game is not started yet
        if current_board is None:
            for button in difficulty_buttons:
                button.draw(screen)
        else:
            # Draw board, buttons, and menu button
            current_board.draw(screen)
            reset_button.draw(screen)
            exit_button.draw(screen)
            menu_button.draw(screen)

            # Check if the game is filled correctly
            if is_board_filled_correctly(current_board):
                end_game_screen(screen, menu_button)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    run_game()


