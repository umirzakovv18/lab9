import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20  # Grid size

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Snake initial setup
snake = [(100, 100), (80, 100), (60, 100)]  # Starting snake body
snake_dir = (CELL_SIZE, 0)  # Initial movement direction

def generate_food():
    while True:
        food_position = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        food_value = random.choices([1, 2, 3], weights=[70, 20, 10])[0]  # Assign different values
        if food_position not in snake:
            return food_position, food_value

food, food_value = generate_food()
food_spawn_time = time.time()  # Track food spawn time
food_lifespan = 5  # Food disappears after 5 seconds

# Game variables
running = True
game_over = False
clock = pygame.time.Clock()
speed = 10  # Initial speed
score = 0
level = 1
font = pygame.font.Font(None, 36)

def show_game_over():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 60, HEIGHT // 2 - 30))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    exit()

# Main game loop
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Snake movement control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != (0, CELL_SIZE):
        snake_dir = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and snake_dir != (0, -CELL_SIZE):
        snake_dir = (0, CELL_SIZE)
    if keys[pygame.K_LEFT] and snake_dir != (CELL_SIZE, 0):
        snake_dir = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and snake_dir != (-CELL_SIZE, 0):
        snake_dir = (CELL_SIZE, 0)
    
    # Move the snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    # Check wall collision
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        show_game_over()
    
    # Check self-collision
    if new_head in snake:
        show_game_over()
    
    # Add new head
    snake.insert(0, new_head)
    
    # Check if food is eaten
    if new_head == food:
        score += food_value  # Increase score based on food value
        food, food_value = generate_food()
        food_spawn_time = time.time()  # Reset food timer
        
        # Level up every 3 food items
        if score % 3 == 0:
            level += 1
            speed += 2  # Increase speed
    else:
        snake.pop()  # Remove tail if no food eaten
    
    # Remove food if it stays too long
    if time.time() - food_spawn_time > food_lifespan:
        food, food_value = generate_food()
        food_spawn_time = time.time()
    
    # Draw food (different colors for different values)
    food_color = RED if food_value == 1 else (BLUE if food_value == 2 else GREEN)
    pygame.draw.rect(screen, food_color, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    
    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    # Display score and level
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    
    # Refresh screen
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()