# Snake Game
import pygame
import random

# Set up the dimensions of the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
INITIAL_SNAKE_SPEED = 10  # Initial speed of the snake
BLOCK_SIZE = 10  # Size of each block of snake and fruit

# Define colors used in the game using RGB values
COLORS = {
    "black": pygame.Color(0, 0, 0),
    "white": pygame.Color(255, 255, 255),
    "red": pygame.Color(255, 0, 0),
    "green": pygame.Color(0, 255, 0),
    "blue": pygame.Color(0, 0, 255),
    "yellow": pygame.Color(255, 255, 0),
    "grey": pygame.Color(128, 128, 128),
}

# Initialize pygame modules
pygame.init()
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Customized Snake Game')  # Window title
clock = pygame.time.Clock()  # Clock for controlling game frame rate

class GameComponent:
    """Class to represent any drawable component in the game."""
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def draw(self, game_window):
        """Draw the component as a rectangle."""
        pygame.draw.rect(game_window, self.color, pygame.Rect(
            self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

class Snake:
    """Class to represent the snake."""
    def __init__(self, positions):
        self.body = [GameComponent(pos, COLORS["green"]) for pos in positions]
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'

    def move(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.body[0].position
        if self.next_direction == 'UP':
            head_y -= BLOCK_SIZE
        elif self.next_direction == 'DOWN':
            head_y += BLOCK_SIZE
        elif self.next_direction == 'LEFT':
            head_x -= BLOCK_SIZE
        elif self.next_direction == 'RIGHT':
            head_x += BLOCK_SIZE
        new_head = GameComponent([head_x, head_y], COLORS["green"])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        """Increase the size of the snake."""
        tail_x, tail_y = self.body[-1].position
        self.body.append(GameComponent([tail_x, tail_y], COLORS["green"]))

    def check_collision(self, other):
        """Check for collision with another game component."""
        head_x, head_y = self.body[0].position
        return head_x == other.position[0] and head_y == other.position[1]

    def check_self_collision(self):
        """Check if the snake has collided with itself."""
        head_x, head_y = self.body[0].position
        return any(head_x == part.position[0] and head_y == part.position[1] for part in self.body[1:])

    def draw(self, game_window):
        """Draw the snake on the game window."""
        for part in self.body:
            part.draw(game_window)

class Fruit:
    """Class to represent the fruit."""
    def __init__(self):
        self.position = [random.randrange(1, (WINDOW_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                         random.randrange(1, (WINDOW_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
        self.color = random.choice([COLORS["red"], COLORS["blue"], COLORS["yellow"]])
        self.points = 10 if self.color == COLORS["red"] else 15 if self.color == COLORS["blue"] else 20

    def respawn(self):
        """Respawn the fruit at a new location."""
        self.position = [random.randrange(1, (WINDOW_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                         random.randrange(1, (WINDOW_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
        self.color = random.choice([COLORS["red"], COLORS["blue"], COLORS["yellow"]])
        self.points = 10 if self.color == COLORS["red"] else 15 if self.color == COLORS["blue"] else 20

    def draw(self):
        """Draw the fruit on the game window."""
        pygame.draw.rect(game_window, self.color, pygame.Rect(
            self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

class Obstacle:
    """Class to represent obstacles in the game."""
    def __init__(self, number):
        self.obstacles = []
        for _ in range(number):
            x = random.randrange(1, (WINDOW_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE
            y = random.randrange(1, (WINDOW_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE
            self.obstacles.append(GameComponent([x, y], COLORS["grey"]))

    def draw(self):
        """Draw obstacles on the game window."""
        for obstacle in self.obstacles:
            obstacle.draw(game_window)

def game_loop():
    """Control the game's main loop including restarting and quitting."""
    snake = Snake([[100 - i * BLOCK_SIZE, 50] for i in range(4)])
    fruit = Fruit()
    obstacles = Obstacle(5)  # Start with 5 obstacles
    score = 0
    level = 1
    speed = INITIAL_SNAKE_SPEED
    game_over = False

    running = True
    while running:
        if not game_over:
            game_window.fill(COLORS['black'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.direction != 'DOWN':
                        snake.next_direction = 'UP'
                    elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                        snake.next_direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                        snake.next_direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                        snake.next_direction = 'RIGHT'

            snake.direction = snake.next_direction
            snake.move()

            if snake.check_collision(GameComponent(fruit.position, fruit.color)):
                score += fruit.points
                fruit.respawn()
                snake.grow()
                if score >= level * 100:
                    level += 1
                    speed = min(25, speed + 1)
                    obstacles = Obstacle(5 + 2 * level)

            if snake.check_self_collision() or \
               snake.body[0].position[0] < 0 or snake.body[0].position[0] >= WINDOW_WIDTH or \
               snake.body[0].position[1] < 0 or snake.body[0].position[1] >= WINDOW_HEIGHT:
                game_over = True

            snake.draw(game_window)
            fruit.draw()
            obstacles.draw()

            font = pygame.font.SysFont('times new roman', 20)
            score_surf = font.render(f'Score: {score} Level: {level}', True, COLORS['white'])
            game_window.blit(score_surf, (5, 5))

            pygame.display.update()
            clock.tick(speed)
        else:
            pygame.time.wait(1500)

            game_window.fill(COLORS['black'])
            font_big = pygame.font.SysFont('times new roman', 36)
            game_over_surf = font_big.render('Game Over', True, COLORS['red'])
            score_surf = font_big.render(f'Final Score: {score}', True, COLORS['yellow'])

            game_window.blit(game_over_surf, (WINDOW_WIDTH / 2 - game_over_surf.get_width() / 2, WINDOW_HEIGHT / 2 - game_over_surf.get_height() / 2 - 20))
            game_window.blit(score_surf, (WINDOW_WIDTH / 2 - score_surf.get_width() / 2, WINDOW_HEIGHT / 2 + 20))

            pygame.display.update()
            pygame.time.wait(5000)
            running = False

def main():
    """Main function to handle game restarts."""
    while True:
        if not game_loop():
            break  # Exit the loop if game_loop returns False (quit)

# Define run_game_snake
def run_game_snake():
    print("Starting Snake Game...")
    main()  # Start the Game


if __name__ == "__main__":
    run_game_snake()

