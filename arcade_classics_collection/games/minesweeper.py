# Minesweeper
# Import necessary libraries
import pygame
import random
import sys

# Define colors using RGB values
COLORS = {
    'white': (239, 235, 235),   # Define white, light grayish
    'grey': (116, 128, 129),  # Define slate grey, a grey with a subtle green undertone
    'darkgrey': (42, 44, 51),  # Define dark grey
    'black': (29, 31, 32),      # Define black, almost black
    'red': (163, 72, 53),       # Define red, dark red
    'green': (143, 188, 143)  # Define light green, a muted sage green
}

# Initialize pygame module
pygame.init()
# Set Caption to 'Minesweeper Game!'
pygame.display.set_caption('Minesweeper Game!')
# Set the dimensions for the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
# Create a surface on screen that has the size of WINDOW_WIDTH x WINDOW_HEIGHT
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Create standard font for text and size
font = pygame.font.SysFont('times new roman', 36)
# Create an object to help track time
clock = pygame.time.Clock()

# Define constants for the game
GRID_SIZE = 10  # Number of cells in each row and column
CELL_SIZE = 60  # Pixel size of each cell
NUM_MINES = 10  # Total number of mines to place on the grid
# Class to manage cells and mines
class Cell:
    def __init__(self, x, y):  # Constructor initializes cell properties
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.x = x
        self.y = y
        self.adjacent_mines = 0

    def reveal(self, grid):  # Reveal cell
        if not self.revealed and not self.flagged:  # Don't reveal flagged ones.
            self.revealed = True
            if self.adjacent_mines == 0 and not self.is_mine:  # Only when 0 mines are next to the cell, reveal neighbors
                directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # Directions for 8 neighbors
                for dx, dy in directions:
                    nx, ny = self.x + dx, self.y + dy
                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        neighbor = grid[nx][ny]
                        if not neighbor.revealed:
                            neighbor.reveal(grid)  # Reveal neighbor

    def force_reveal(self):  # For game over or game won, show all cells
        if not self.revealed:  # Reduce unnecessary revealing
            self.revealed = True  # This forcibly reveals the cell

    def draw(self):  # Draws each cell based on its state (revealed, flagged, mine)
        rect = pygame.Rect(100 + self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.revealed:  # Only revealed
            if self.is_mine:
                # Draw mine
                pygame.draw.rect(game_window, COLORS["red"], rect)  # Draw mine differently if you like
            else:
                # Draw revealed cell
                pygame.draw.rect(game_window, COLORS["white"], rect)  # Base Color
                if self.adjacent_mines > 0:  # When mines adjacent
                    # Show number of adjacent mines
                        text = font.render(str(self.adjacent_mines), True, COLORS["black"])
                        text_rect = text.get_rect(center=rect.center)
                        game_window.blit(text, text_rect)
        else:  # Draw unrevealed cell, dark / covered
            pygame.draw.rect(game_window, COLORS["darkgrey"], rect)
            if self.flagged:
                # Show flag on flagged cells
                text = font.render('F', True, COLORS["green"])
                text_rect = text.get_rect(center=rect.center)
                game_window.blit(text, text_rect)
        # Draw grey border for cell
        pygame.draw.rect(game_window, COLORS["grey"], rect, 1)  # Border

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

def check_win_condition(grid):
    for row in grid:
        for cell in row:
            # If there's a non-mine cell that isn't revealed, or a mine that isn't flagged, return False
            if (not cell.is_mine and not cell.revealed) or (cell.is_mine and not cell.flagged):
                return False
    return True  # All conditions met for a win
def game_won_message():  # Game Won Message at the end
    game_window.fill(COLORS["black"])  # Clear the screen for message
    game_won = font.render('GAME WON!', True, COLORS['green'])
    game_window.blit(game_won, (WINDOW_WIDTH / 2 - game_won.get_width() / 2,
                                 WINDOW_HEIGHT / 2 - game_won.get_height() / 2))
    pygame.display.flip()  # Update the display to show the game won message
    pygame.time.wait(3000)  # wait 3 seconds
def game_over_message():  # Game Over Message at the end
    game_window.fill(COLORS["black"])  # Clear the screen for message
    game_over = font.render('Landed on a mine. GAME OVER!', True, COLORS['red'])
    game_window.blit(game_over, (WINDOW_WIDTH / 2 - game_over.get_width() / 2,
                                 WINDOW_HEIGHT / 2 - game_over.get_height() / 2))
    pygame.display.flip()  # Update the display to show the game over message
    pygame.time.wait(3000)  # Allow time for the player to read the message

def game_loop():  # Define game_loop function
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = (event.pos[0] - 100) // CELL_SIZE, event.pos[1] // CELL_SIZE
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:  # Ensure the click is within the grid
                    if event.button == 1:  # Left click
                        if not grid[x][y].flagged:  # Only reveal if not flagged
                            grid[x][y].reveal(grid)  # Use  reveal
                            if grid[x][y].is_mine:
                                print("Game Over!")  # Indicate game over
                                # Reveal all cells because a mine was clicked
                                for row in grid:
                                    for cell in row:
                                        cell.force_reveal()
                                for row in grid:
                                    for cell in row:
                                        cell.draw()
                                pygame.display.flip()  # Update the display to show all mines
                                pygame.time.wait(3000)  # Wait three seconds to show the mines
                                game_over_message()  # Show Game over Message
                                running = False  # Stop the game loop after displaying the message

                    elif event.button == 3:  # Right click
                        # Toggle flag on and off
                        grid[x][y].flagged = not grid[x][y].flagged


        if running:
            game_window.fill(COLORS["black"])  # Clear the screen
            # Draw all cells
            for row in grid:
                for cell in row:
                    cell.draw()
            if check_win_condition(grid):
                print("Game WON!")  # Indicate game over
                # Reveal all mines because game won
                for row in grid:
                    for cell in row:
                        cell.force_reveal()
                for row in grid:
                    for cell in row:
                        cell.draw()
                pygame.display.flip()  # Update the display to show all mines
                pygame.time.wait(3000)  # Wait three seconds to show the revealed mines
                game_won_message()  # Show game won message
                running = False  # Stop the game loop after displaying the message

            pygame.display.flip()  # Update the full display Surface to the screen

        clock.tick(60)  # Maintain 60 frames per second

# Define run_game_[game] for arcade interface.
def run_game_minesweeper():
    print("Starting Minesweeper Game...")
    game_loop()  # Start the game loop after exiting the menu

# Start main
if __name__ == '__main__':
    run_game_minesweeper()  # Start the application by displaying the main menu
