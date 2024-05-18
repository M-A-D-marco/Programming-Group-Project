# Arcade Classics Collection - Main Menu Interface
# Import necessary libraries
import pygame
import sys
import importlib

# Define colors used in the game interface, using RGB values
COLORS = {
    'white': pygame.Color(239, 235, 235),   # Define white, light grayish
    'black': pygame.Color(29, 31, 32),      # Define black, almost black
    'red': pygame.Color(163, 72, 53),       # Define red, dark red
    'grey': pygame.Color(225, 225, 225),    # Define grey
    'dark_grey': pygame.Color(42, 44, 51),  # Define dark grey
    'green': pygame.Color(162, 173, 159)    # Define green, dark green
}

# Initialize the pygame library
pygame.init()
# Set the title of the window
pygame.display.set_caption('Arcade Classics Collection')
# Set the dimensions for the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
# Create the game window with predefined dimensions
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Create the font for text, using Arial and size 36
font = pygame.font.SysFont('arial', 36)
# Initialize a clock for managing frame rate
clock = pygame.time.Clock()

# Define button size
BUTTON_WIDTH = 420  # Example width
BUTTON_HEIGHT = 50  # Example height

# A global variable to store which game is currently being played
current_game = None

# Class to create buttons within the main menu interface
class Button:
    def __init__(self, x, y, text, action=None):
        # Initialize button properties
        self.color = COLORS['grey']  # Color of the button
        self.text = text             # Text displayed on the button
        self.action = action         # Optional function to execute when button is clicked
        # Button's size
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        # Calculate the button's position, centering it at (x, y)
        self.x = x - self.width // 2
        self.y = y - self.height // 2

    # Method to draw the button on a given surface
    def draw(self, win, outline=None):
        # If an outline is specified, draw it around the button
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        # Draw the button's main rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        # Render the button's text in the center of the button
        text_render = font.render(self.text, True,
                                  COLORS['black'])  # Render text to a surface with anti-aliasing and black color
        # win.blit: draws the text_render surface onto the game window at the calculated position.
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

    # Method to handle mouse click events on the button
    def handle_event(self, event):
        # Check if the mouse button is pressed down
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()  # Get the position of the mouse cursor
            # If the mouse is over the button when clicked, execute the button's action
            if self.is_over(pos) and self.action:
                self.action()

# Display the main menu and handle user interactions from a list of games to play.
def main_menu():
    global current_game  # Reference global variable to manage the state of the game currently being played
    current_game = None  # Reset the current game to None

    # Set the background of the main menu to dark grey
    game_window.fill(COLORS['dark_grey'])

    # Setup fonts for text display on the main menu
    title_font = pygame.font.SysFont('arial', 48)  # main title
    message_font = pygame.font.SysFont('arial', 36)  # sub-messages or instructions

    # Render the title and instruction text with anti-aliasing enabled
    title_text = title_font.render('Arcade Games Collection', True, COLORS['green'])  # Title in green
    message_text = message_font.render('Select game', True, COLORS['red'])  # Message text in red

    # Define buttons for each available game using a centralized x coordinate and staggered y coordinates
    snake_btn = Button(WINDOW_WIDTH // 2, 200, 'Snake')
    minesweeper_btn = Button(WINDOW_WIDTH // 2, 300, 'Minesweeper')
    memory_btn = Button(WINDOW_WIDTH // 2, 400, 'Memory')
    hangman_btn = Button(WINDOW_WIDTH // 2, 500, 'Hangman')
    buttons = [snake_btn, minesweeper_btn, memory_btn, hangman_btn]  # List of button objects for easy management

    running = True  # Control variable for the main menu loop
    while running:
        # Draw the title and instruction text on the window at calculated positions to center them
        game_window.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 20))
        game_window.blit(message_text, (WINDOW_WIDTH // 2 - message_text.get_width() // 2, 80))

        # Draw each button on the main menu screen
        for button in buttons:
            button.draw(game_window, COLORS['white'])  # white color for button outline

        # Event handling loop to process user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User closed the window
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button was pressed
                    for button in buttons:
                        # Check if the click was on any of the buttons
                        if button.is_over(event.pos):
                            current_game = button.text  # Update current game based on button text
                            print('Game launched:', current_game)
                            run_game(current_game)  # Launch the selected game

        pygame.display.update()  # Refresh the display
        clock.tick(60)  # Maintain 60 frames per second

# Def run_game: running the selected game and handle its termination
def run_game(game_name):
    # Normalize the game name to lowercase for the module and construct the function name
    module_name = f"games.{game_name.lower()}"
    function_name = f"run_game_{game_name.lower()}"

    try:
        # Dynamically import the game module
        game_module = importlib.import_module(module_name)

        # Get the specific function from the module using getattr
        game_function = getattr(game_module, function_name)

        # Execute the game function
        game_function()
    except ModuleNotFoundError:
        print(
            f"Module for {game_name} not found. Please check that the file {game_name.lower()}.py exists in the 'games' directory.")
    except AttributeError:
        print(f"Function {function_name} not found in the {game_name.lower()} module. Please ensure it is defined.")
    finally:
        # Call game_over after attempting to run the game
        game_over()

# Display the game over screen with options to return to the main menu, play again, or quit.
def game_over():
    global current_game  # Use the global variable to manage the game state

    # Clear the screen and set background to dark grey
    game_window.fill(COLORS['dark_grey'])

    # Set up title and message
    title_font = pygame.font.SysFont('arial', 48)  # main title
    message_font = pygame.font.SysFont('arial', 36)  # secondary messages

    # Render text with anti-aliasing for smoother text
    title_text = title_font.render('Arcade Games Collection', True, COLORS['green'])
    message_text = message_font.render('Game Over', True, COLORS['red'])

    # Create buttons to navigate from the game over screen
    main_menu_btn = Button(WINDOW_WIDTH // 2, 225, 'Main Menu')  # Button to return to the main menu
    play_again_btn = Button(WINDOW_WIDTH // 2, 350, f'Play {current_game} Again')  # Button to replay the current game
    quit_btn = Button(WINDOW_WIDTH // 2, 475, 'Quit')  # Button to quit the application
    buttons = [main_menu_btn, play_again_btn, quit_btn]  # List of buttons for easy management

    running = True  # Control variable for the game over loop
    while running:
        # Display the title and message at the center of the screen
        game_window.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 20))
        game_window.blit(message_text, (WINDOW_WIDTH // 2 - message_text.get_width() // 2, 80))

        # Draw each button with an optional white outline for visibility
        for button in buttons:
            button.draw(game_window, COLORS['white'])

        # Event handling loop to process user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User closed the window
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Check if the left mouse button was pressed
                    for button in buttons:
                        # Check if the click was on any of the buttons
                        if button.is_over(event.pos):
                            if button.text == 'Main Menu':
                                return main_menu()  # Return to the main menu
                            elif button.text == f'Play {current_game} Again':
                                run_game(current_game)  # Restart the game

                            elif button.text == 'Quit':  # Quit
                                pygame.quit()
                                sys.exit()

        # Update the display and enforce a frame rate of 60 fps
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main_menu()  # Start the application by displaying the main menu