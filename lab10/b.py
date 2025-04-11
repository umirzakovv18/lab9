import pygame
import random
import time
import psycopg2
from datetime import datetime

# Database setup
conn = psycopg2.connect(
    dbname="snakedb",
    user="postgres",
    password="rootroot",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Ensure tables exist
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);
''')
cur.execute('''
CREATE TABLE IF NOT EXISTS user_score (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    score INTEGER,
    level INTEGER,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')
conn.commit()

# Pygame initialization
pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Login")
font = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Function to render text input box
def get_username():
    username = ""
    input_active = True
    while input_active:
        screen.fill(WHITE)
        prompt = font.render("Enter your username:", True, BLACK)
        screen.blit(prompt, (150, 100))
        text_surface = font.render(username, True, BLUE)
        screen.blit(text_surface, (150, 150))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15:
                        username += event.unicode
    return username.strip()

# Get or create user
def get_user_data(username):
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
        cur.execute("SELECT level FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
        result = cur.fetchone()
        last_level = result[0] if result else 1
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        last_level = 1
    return user_id, last_level

# Game logic
def generate_food(snake):
    while True:
        food_position = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        food_value = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
        if food_position not in snake:
            return food_position, food_value

def show_game_over(score):
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 60, HEIGHT // 2 - 30))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)

def save_progress(user_id, score, level):
    cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
                (user_id, score, level))
    conn.commit()

# Get username and data
username = get_username()
user_id, level = get_user_data(username)

snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = (CELL_SIZE, 0)
food, food_value = generate_food(snake)
food_spawn_time = time.time()
food_lifespan = 5

running = True
paused = False
score = 0
speed = 10 + (level - 1) * 2
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_progress(user_id, score, level)
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    save_progress(user_id, score, level)

    if paused:
        pause_text = font.render("Game Paused. Press P to resume.", True, BLACK)
        screen.blit(pause_text, (100, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(5)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != (0, CELL_SIZE):
        snake_dir = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and snake_dir != (0, -CELL_SIZE):
        snake_dir = (0, CELL_SIZE)
    if keys[pygame.K_LEFT] and snake_dir != (CELL_SIZE, 0):
        snake_dir = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and snake_dir != (-CELL_SIZE, 0):
        snake_dir = (CELL_SIZE, 0)

    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT or new_head in snake:
        show_game_over(score)
        save_progress(user_id, score, level)
        break

    snake.insert(0, new_head)

    if new_head == food:
        score += food_value
        food, food_value = generate_food(snake)
        food_spawn_time = time.time()
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    if time.time() - food_spawn_time > food_lifespan:
        food, food_value = generate_food(snake)
        food_spawn_time = time.time()

    # Draw food
    food_color = RED if food_value == 1 else (BLUE if food_value == 2 else GREEN)
    pygame.draw.rect(screen, food_color, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Draw texts
    name_text = font.render(f"Player: {username}", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(name_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(level_text, (10, 70))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
cur.close()
conn.close()