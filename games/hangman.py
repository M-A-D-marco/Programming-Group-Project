# Hangman

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Fonts and Colors
LETTER_FONT = pygame.font.SysFont('times new roman', 30)
WORD_FONT = pygame.font.SysFont('times new roman', 36)
TITLE_FONT = pygame.font.SysFont('times new roman', 36)

COLORS = {
    'white': (239, 235, 235),   # Define white, light grayish
    'black': (29, 31, 32),      # Define black, almost black
    'red': (163, 72, 53),       # Define red, dark red
    'green': (143, 188, 143)  # Define light green, a muted sage green
}

# Game variables
themes = {
    "Science": ["GRAVITY", "ATOM", "ENERGY", "QUANTUM", "NEURON"],
    "Sports": ["FOOTBALL", "BASKETBALL", "CRICKET", "TENNIS", "BASEBALL"],
    "Geography": ["MOUNTAIN", "RIVER", "COUNTRY", "CITY", "OCEAN"],
    "Animals": ["ELEPHANT", "GIRAFFE", "RHINOCEROS", "KANGAROO", "TIGER"]
}
words = []
word = ''
guessed = {}
hangman_status = 0

# Keyboard layout (QWERTZ)
keys = [
    "QWERTZUIOPÜ",
    "ASDFGHJKLÖÄ",
    "YXCVBNM"
]
key_positions = []

def init_keys():
    global key_positions
    key_positions.clear()
    key_width = 40
    key_height = 40
    key_spacing = 10
    starting_y = 400
    for index, row in enumerate(keys):
        total_row_width = len(row) * (key_width + key_spacing) - key_spacing
        starting_x = (WIDTH - total_row_width) // 2
        for i, letter in enumerate(row):
            x = starting_x + i * (key_width + key_spacing)
            y = starting_y + index * (key_height + 10)
            key_positions.append((letter, x, y, key_width, key_height, COLORS['white']))

def draw_keys():
    for letter, x, y, width, height, color in key_positions:
        pygame.draw.rect(win, color, (x, y, width, height))
        text = LETTER_FONT.render(letter, True, COLORS['black'])
        win.blit(text, (x + (width - text.get_width()) // 2, y + (height - text.get_height()) // 2))

def draw_hangman():
    stages = [
        lambda: pygame.draw.circle(win, COLORS['white'], (650, 150), 30, 3),  # Head
        lambda: pygame.draw.line(win, COLORS['white'], (650, 180), (650, 250), 3),  # Body
        lambda: pygame.draw.line(win, COLORS['white'], (650, 200), (600, 230), 3),  # Left Arm
        lambda: pygame.draw.line(win, COLORS['white'], (650, 200), (700, 230), 3),  # Right Arm
        lambda: pygame.draw.line(win, COLORS['white'], (650, 250), (600, 300), 3),  # Left Leg
        lambda: pygame.draw.line(win, COLORS['white'], (650, 250), (700, 300), 3)  # Right Leg
    ]
    for i in range(hangman_status):
        stages[i]()

def update_keys(guess, correct):
    for i, (letter, x, y, width, height, color) in enumerate(key_positions):
        if letter == guess:
            key_positions[i] = (letter, x, y, width, height, COLORS['green'] if correct else COLORS['red'])

def draw(current_guess):
    win.fill(COLORS['black'])
    text = TITLE_FONT.render("HANGMAN", 1, COLORS['white'])
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))
    display_word = " ".join([letter if letter in guessed else '_' for letter in word])
    text = WORD_FONT.render(display_word, 1, COLORS['white'])
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 200))
    draw_keys()
    draw_hangman()
    pygame.display.update()

def message_display(message):
    win.fill(COLORS['black'])  # Clear screen before displaying the message
    text = WORD_FONT.render(message, 1, COLORS['white'])
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)

def end_game_message(message):
    message_display(message)

def draw_theme_buttons():
    global theme_buttons
    theme_buttons = [
        ("Science", 150, 250, 200, 50, COLORS['white']),
        ("Sports", 450, 250, 200, 50, COLORS['white']),
        ("Geography", 150, 350, 200, 50, COLORS['white']),
        ("Animals", 450, 350, 200, 50, COLORS['white'])
    ]
    for theme, x, y, width, height, color in theme_buttons:
        pygame.draw.rect(win, color, (x, y, width, height))
        text = LETTER_FONT.render(theme, True, COLORS['black'])
        win.blit(text, (x + (width - text.get_width()) // 2, y + (height - text.get_height()) // 2))

def theme_selection():
    win.fill(COLORS['black'])
    text = TITLE_FONT.render("Please select theme for your words", True, COLORS['white'])
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))
    draw_theme_buttons()
    pygame.display.update()
    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for theme, tx, ty, twidth, theight, _ in theme_buttons:
                    if tx <= x <= tx + twidth and ty <= y <= ty + theight:
                        return theme
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main():
    global words, word, guessed, hangman_status
    selected_theme = theme_selection()
    words = themes[selected_theme]
    word = random.choice(words).upper()
    guessed = {}
    hangman_status = 0
    init_keys()
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for letter, kx, ky, kwidth, kheight, kcolor in key_positions:
                    if kx <= x <= kx + kwidth and ky <= y <= ky + kheight:
                        if letter not in guessed:
                            guessed[letter] = letter in word
                            update_keys(letter, guessed[letter])
                            if not guessed[letter]:
                                hangman_status += 1
                            if hangman_status == 6:
                                end_game_message(f"You LOST! Word was: {word}")
                                run = False
                            elif all(letter in guessed for letter in word):
                                end_game_message("You WON! Congrats!")
                                run = False
                            break

        if run:
            draw("")

# Define run_game_hangman
def run_game_hangman():
    print("Starting Hangman Game...")
    main()  # Start the Game

if __name__ == "__main__":
    run_game_hangman()
