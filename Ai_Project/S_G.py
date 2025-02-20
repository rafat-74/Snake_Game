import tkinter as tk
import random

# Game settings
WIDTH = 800  
HEIGHT = 600  
CELL_SIZE = 20

# Game window settings
window = tk.Tk()
window.title("Snake Game")
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# The snake and the food
snake = [(100, 100), (80, 100), (60, 100)]    
snake_dir = "Right"
food = (200, 200)
score = 0  
game_started = False 

# AI setting
ai_enabled = False

# Food colors
food_colors = ["#FF69B4", "#00BFFF", "#FFD700", "#32CD32"] 
food_color = None  

# Draw the snake and the food
def draw_snake():
    canvas.delete("snake")

    # Head color
    head = snake[0]
    canvas.create_rectangle(
        head[0], head[1], head[0] + CELL_SIZE, head[1] + CELL_SIZE, fill="#CDC1FF", tags="snake"
    )
    
    # Body color
    for segment in snake[1:]:
        x, y = segment
        canvas.create_rectangle(
            x, y, x + CELL_SIZE, y + CELL_SIZE, fill="#7F65D8", tags="snake"
        )

def draw_food():
    canvas.delete("food")
    x, y = food
    canvas.create_oval(
        x, y, x + CELL_SIZE, y + CELL_SIZE, fill=food_color, tags="food"
    )

# Score Section
def draw_score():
    canvas.delete("score")
    canvas.create_text(
        50,
        10,
        text=f"Score: {score}",
        fill="white",
        font=("Arial", 14),
        tags="score",
    )

# Control the snake's movement
def move_snake():
    global snake, food, snake_dir, score, game_started

    if not game_started: 
        return

    # Use AI if enabled
    if ai_enabled:
        snake_dir = get_greedy_direction()

    # Set direction
    head_x, head_y = snake[0]
    if snake_dir == "Right":
        new_head = (head_x + CELL_SIZE, head_y)
    elif snake_dir == "Left":
        new_head = (head_x - CELL_SIZE, head_y)
    elif snake_dir == "Up":
        new_head = (head_x, head_y - CELL_SIZE)
    elif snake_dir == "Down":
        new_head = (head_x, head_y + CELL_SIZE)

    # Check for collision
    if (
        new_head[0] < 0
        or new_head[1] < 0
        or new_head[0] >= WIDTH
        or new_head[1] >= HEIGHT
        or new_head in snake
    ):
        game_over()
        return

    # Update the snake's position
    snake = [new_head] + snake

    # Check for food consumption
    if new_head == food:
        score += 1  
        generate_food()
    else:
        snake.pop()

    draw_snake()
    draw_food()
    draw_score()
    window.after(100, move_snake)

# Food appears at a random location
def generate_food():
    global food, food_color
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:
            food = (x, y)
            break
    
    # Select a random color when new food appears
    food_color = random.choice(food_colors)
    draw_food()

# Game reset section
def reset_game():
    global snake, snake_dir, food, score, game_started, food_color
    
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    snake = [(center_x, center_y), (center_x - CELL_SIZE, center_y), (center_x - 2 * CELL_SIZE, center_y)]  
    snake_dir = "Right" 
    score = 0  
    generate_food()  
    canvas.delete("game_over")  
    draw_snake()
    draw_food()
    draw_score()
    game_started = False  
    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text="Press Enter to Start",
        fill="white",
        font=("Arial", 16),
        tags="start_message",
    )

# Game over and restart display section
def game_over():
    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text="GAME OVER",
        fill="white",
        font=("Arial", 24),
        tags="game_over",
    )
    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 30,
        text="Press R to Restart",
        fill="yellow",
        font=("Arial", 16),
        tags="game_over",
    )
    window.bind("<KeyPress-r>", lambda event: reset_game())  

# AI logic using Greedy algorithm
def get_greedy_direction():
    global snake, food
    head_x, head_y = snake[0]
    food_x, food_y = food

    if head_x < food_x and snake_dir != "Left":
        return "Right"
    elif head_x > food_x and snake_dir != "Right":
        return "Left"
    elif head_y < food_y and snake_dir != "Up":
        return "Down"
    elif head_y > food_y and snake_dir != "Down":
        return "Up"
    return snake_dir

# Toggle AI
def toggle_ai(event):
    global ai_enabled
    ai_enabled = not ai_enabled
    if ai_enabled:
        canvas.create_text(
            WIDTH // 2,
            HEIGHT - 30,
            text="AI Enabled",
            fill="green",
            font=("Arial", 12),
            tags="ai_status",
        )
    else:
        canvas.delete("ai_status")

# Control with keyboard 
def change_direction(event):
    global snake_dir, game_started
    if event.keysym == "Up" and snake_dir != "Down":
        snake_dir = "Up"
    elif event.keysym == "Down" and snake_dir != "Up":
        snake_dir = "Down"
    elif event.keysym == "Left" and snake_dir != "Right":
        snake_dir = "Left"
    elif event.keysym == "Right" and snake_dir != "Left":
        snake_dir = "Right"

def start_game(event):
    global game_started
    game_started = True
    canvas.delete("start_message")   
    move_snake()

# Run the game
window.bind("<KeyPress>", change_direction)
window.bind("<Return>", start_game)  
window.bind("<KeyPress-a>", toggle_ai)
reset_game()
window.mainloop()


# مع تحيات بصلة تيم 