
import pygame, sys
from pygame.locals import *
import random, time

# Initialize Pygame
pygame.init()

# Set FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Define Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
COIN_THRESHOLD = 5  # Increase speed after collecting 5 coins

# Set up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load Background Image
background = pygame.image.load("C:\\Users\\ayatj\\OneDrive\\Desktop\\lab8PP\\Racer\\AnimatedStreet.png")

# Create Game Window
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer Game")

# Enemy Car Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\ayatj\\OneDrive\\Desktop\\lab8PP\\Racer\\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """ Moves enemy down and resets when it leaves the screen. """
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1  # Increase score
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player Car Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\ayatj\\OneDrive\\Desktop\\lab8PP\\Racer\\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        """ Moves the player's car left and right based on key input. """
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Coin Class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load("C:\\Users\\ayatj\\OneDrive\\Desktop\\lab8PP\\Racer\\Coin.png")
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.rect = self.image.get_rect()
        self.value = self.assign_value()
        self.reset_position()

    def assign_value(self):
        """ Randomly assigns a coin value (1, 2, or 5) based on probability. """
        return random.choices([1, 2, 5], weights=[70, 20, 10])[0]

    def reset_position(self):
        """ Places the coin at a new random position and assigns a new value. """
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(100, SCREEN_HEIGHT - 100))
        self.value = self.assign_value()

    def move(self):
        """ Moves the coin down and resets if it goes off-screen. """
        self.rect.move_ip(0, SPEED // 2)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

# Create Sprite Objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Create Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Add Event to Increase Speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Gradual speed increase
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw Background
    DISPLAYSURF.blit(background, (0, 0))

    # Display Score and Collected Coins
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10))

    # Move and Draw Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Check Collision with Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('labs/lab8/musics/crash.wav.mp3').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Check Collision with Coin
    collected_coin = pygame.sprite.spritecollideany(P1, coins)
    if collected_coin:
        COINS_COLLECTED += collected_coin.value
        collected_coin.reset_position()
        
        # Increase Enemy Speed after Collecting COIN_THRESHOLD coins
        if COINS_COLLECTED % COIN_THRESHOLD == 0:
            SPEED += 1

    # Update Display
    pygame.display.update()
    FramePerSec.tick(FPS)
