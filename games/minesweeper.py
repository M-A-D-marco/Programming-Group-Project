# Minesweeper
# Import necessary libraries
import pygame
import random
import sys

# Define colors used in the game interface, using RGB values
COLORS = {
    'white': pygame.Color(239, 235, 235),   # Define white, light grayish
    'black': pygame.Color(29, 31, 32),      # Define black, almost black
    'red': pygame.Color(163, 72, 53),       # Define red, dark red
    'grey': pygame.Color(225, 225, 225),    # Define grey
    'dark_grey': pygame.Color(42, 44, 51),  # Define dark grey
    'green': pygame.Color(162, 173, 159)    # Define green, dark green
}

# Initialize pygame module
pygame.init()
# Set Caption to Minesweeper
pygame.display.set_caption('Minesweeper')
# Set the dimensions for the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
# Create a surface on screen that has the size of WINDOW_WIDTH x WINDOW_HEIGHT
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Create the font for text, using Arial and size 36
font = pygame.font.SysFont('times new roman', 36)
# Create an object to help track time
clock = pygame.time.Clock()

# Define button size
BUTTON_WIDTH = 420  # Example width
BUTTON_HEIGHT = 50  # Example height

# Define constants for the game
GRID_SIZE = 10  # Number of cells in each row and column
CELL_SIZE = 60  # Pixel size of each cell
NUM_MINES = 20  # Total number of mines to place on the grid

class Button:
    def __init__(self, x, y, text):
        # Initialize button properties
        self.color = COLORS['grey']  # Color of the button
        self.text = text             # Text displayed on the button
        # Button's size
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        # Calculate the button's position, centering it at (x, y)
        self.x = x - self.width // 2
        self.y = y - self.height // 2

    # Method to draw the button on a given surface
    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        # Draw the button's main rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        # Render the button's text in the center of the button
        text_render = font.render(self.text, True,
                                  COLORS['black'])  # Render text to a surface with anti-aliasing and black color
        # game_window.blit: draws the text_render surface onto the game window at the calculated position.
        win.blit(text_render,
                 (self.x + (self.width - text_render.get_width()) // 2,
                               # Calculate X position: Center text horizontally within the button
                               self.y + (
                                           self.height - text_render.get_height()) // 2))
        # Calculate Y position: Center text vertically within the button

    # Method to determine if a given position (mouse cursor) is over the button
    def is_over(self, pos):
        # Check if the cursor is within the button's boundaries
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

# Class to manage cells and mines
class Cell:
    def __init__(self, x, y):  # Constructor initializes cell properties
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.x = x
        self.y = y
        self.adjacent_mines = 0

    def draw(self, win):  # Draws each cell based on its state (revealed, flagged, mine)
        # `win` parameter represents surface to draw on for more flexibility, code reusability, control and clarity
        rect = pygame.Rect(100 + self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.revealed:
            if self.is_mine:
                # Draw mine
                pygame.draw.rect(win, COLORS["red"], rect)
            else:
                # Draw revealed cell
                pygame.draw.rect(win, COLORS["grey"], rect)
                if self.adjacent_mines > 0:
                    # Show number of adjacent mines
                    font = pygame.font.SysFont('times new roman', 35)
                    text = font.render(str(self.adjacent_mines), True, COLORS["black"])
                    text_rect = text.get_rect(center=rect.center)
                    win.blit(text, text_rect)
        else:
            # Draw unrevealed cell
            pygame.draw.rect(win, COLORS["dark_grey"], rect)
            if self.flagged:
                # Show flag on flagged cells
                font = pygame.font.SysFont('times new roman', 35)
                text = font.render('F', True, COLORS["green"])
                text_rect = text.get_rect(center=rect.center)
                win.blit(text, text_rect)
        # Draw border for cell
        pygame.draw.rect(win, COLORS["white"], rect, 1)  # Border

def create_grid():
    grid = [[Cell(x, y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
    mine_locations = set()
    while len(mine_locations) < NUM_MINES:
        mine_locations.add((random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)))
    for (x, y) in mine_locations:
        grid[x][y].is_mine = True
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if not grid[x][y].is_mine:
                grid[x][y].adjacent_mines = sum(1 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                                               if 0 <= x + dx < GRID_SIZE and 0 <= y + dy < GRID_SIZE
                                               and grid[x + dx][y + dy].is_mine)
    return grid

# Define game_loop function
def start_game_menu():
    # Set the background of the main menu to dark grey
    game_window.fill(COLORS['dark_grey'])

    # Setup fonts for text display on the main menu
    title_font = pygame.font.SysFont('times new roman', 48)  # main title
    message_font = pygame.font.SysFont('times new roman', 36)  # sub-message

    # Render the title and instruction text with anti-aliasing enabled
    title_text = title_font.render('Arcade Games Collection', True, COLORS['green'])  # Title in green
    message_text = message_font.render('Minesweeper', True, COLORS['red'])  # Message text in red

    # Define button using a centralized x coordinate and staggered y coordinates
    start_btn = Button(WINDOW_WIDTH // 2, 350, 'Start Game')

    while True:  # Control variable for the main menu loop
        # Draw the titles on the window at calculated positions to center them
        game_window.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 20))
        game_window.blit(message_text, (WINDOW_WIDTH // 2 - message_text.get_width() // 2, 80))

        # Draw button on the start game menu screen
        start_btn.draw(game_window, COLORS['white'])

        # Event handling loop to process user inputs
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.is_over(pos):
                    return  # Proceed to game if button is clicked


        pygame.display.update()  # Refresh the display
        clock.tick(60)  # Maintain 60 frames per second

# Define game_loop function
def game_loop():
    grid = create_grid()  # Initialize the grid with cells and mines

    # Define a variable to control the game loop
    running = True
    while running:  # Game Loop
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # Only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # Change the value running to 'False', to exit the game loop
                running = False
                game_window.fill(COLORS["black"])  # Clear the screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = (event.pos[0] - 100) // CELL_SIZE, event.pos[1] // CELL_SIZE
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:  # Ensure the click is within the grid
                    if event.button == 1:  # Left click
                        if not grid[x][y].flagged:  # Only reveal if not flagged
                            grid[x][y].revealed = True
                            if grid[x][y].is_mine:
                                print("Game Over!")  # Indicate game over
                                running = False
                    elif event.button == 3:  # Right click
                        # Toggle flag on and off
                        grid[x][y].flagged = not grid[x][y].flagged

        game_window.fill(COLORS["black"])  # Clear the screen

        # Draw all cells
        for row in grid:
            for cell in row:
                cell.draw(game_window)

        pygame.display.flip()  # Update the full display Surface to the screen
        clock.tick(60)  # Maintain 60 frames per second

# Define main
def run_game_minesweeper():
    print("Starting Minesweeper Game...")
    start_game_menu()  # Show the main menu
    game_loop()  # Start the game loop after exiting the menu

# Start main
if __name__ == '__main__':
    run_game_minesweeper()  # Start the application by displaying the main menu
