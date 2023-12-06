from tkinter import *
import random
from enum import Enum

# Constants
GAME_WIDTH = 100
GAME_HEIGHT = 700
SPEED = 75
SIZE = 25
BODY = 3
COLOR = "#00FF00"
APPLE_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Enumeration for directions
class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

class Snake:
    """
    Represents the snake in the game.
    """
    def __init__(self, initial_coordinates):
        """
        Initializes the snake with given initial coordinates.

        Parameters:
            initial_coordinates (list): Initial coordinates of the snake.
        """
        self.body_size = BODY
        self.coordinates = initial_coordinates
        self.squares = [canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=COLOR, tag="snake") for x, y in initial_coordinates]

class Food:
    """
    Represents the food in the game.
    """
    def __init__(self):
        """
        Initializes the food at a random position.
        """
        x = random.randint(0, (GAME_WIDTH // SIZE) - 1) * SIZE
        y = random.randint(0, (GAME_HEIGHT // SIZE) - 1) * SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SIZE, y + SIZE, fill=APPLE_COLOR, tag="food")

def next_turn(snake, food):
    """
    Handles the game logic for the next turn.

    Parameters:
        snake (Snake): The snake object.
        food (Food): The food object.
    """
    x, y = snake.coordinates[0]

    if direction == Direction.UP.value:
        y -= SIZE
    elif direction == Direction.DOWN.value:
        y += SIZE
    elif direction == Direction.LEFT.value:
        x -= SIZE
    elif direction == Direction.RIGHT.value:
        x += SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    """
    Changes the direction of the snake.

    Parameters:
        new_direction (Direction): The new direction to set.
    """
    global direction
    if new_direction.value in (Direction.LEFT.value, Direction.RIGHT.value, Direction.UP.value, Direction.DOWN.value):
        if direction != new_direction.value:
            direction = new_direction.value

def check_collisions(snake):
    """
    Checks for collisions with walls or itself.

    Parameters:
        snake (Snake): The snake object.

    Returns:
        bool: True if there is a collision, False otherwise.
    """
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    """
    Handles the game over scenario.
    """
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consoles', 70),
                       text="GAME OVER", fill="red", tag="gameover")

if __name__ == "__main__":
    # Tkinter setup and window configuration
    window = Tk()
    window.title("Snake Game")
    window.resizable(False, False)

    # Initializations
    score = 0
    direction = Direction.DOWN.value

    label = Label(window, text="Score:{}".format(score), font=("consoles", 40))
    label.pack()

    canvas = Canvas(window, bg=COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Event bindings
    window.bind('<Left>', lambda event: change_direction(Direction.LEFT))
    window.bind('<Right>', lambda event: change_direction(Direction.RIGHT))
    window.bind('<Up>', lambda event: change_direction(Direction.UP))
    window.bind('<Down>', lambda event: change_direction(Direction.DOWN))

    # Initializations of snake and food
    initial_snake_coordinates = [(0, 0) for _ in range(BODY)]
    snake = Snake(initial_snake_coordinates)
    food = Food()

    # Start the game loop
    next_turn(snake, food)

    window.mainloop()
