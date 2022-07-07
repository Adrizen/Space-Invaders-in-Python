import wave
import pygame
import os
import time
import random
pygame.font.init()

# Game dimension.
WIDTH, HEIGHT = 1024, 768

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images.
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))

# Player's ship.
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers.
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

# Background image.
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


# Abstract ship class
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0

    def draw(self, WINDOW):  # Draw the ship in the screen.
        WINDOW.blit(self.ship_img, (self.x, self.y))

    def get_width(self):    # Return the width of the ship's image.
        return self.ship_img.get_width()

    def get_height(self):   # Return the height of the ship's image.
        return self.ship_img.get_height()

# Player ship that inherits from Ship.


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

# Enemy ship that inherits from Ship.


class Enemy(Ship):
    # This is used when creating random enemy ships.
    COLOR_MAP = {"red": (RED_SPACE_SHIP, RED_LASER),
                 "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                 "blue": (BLUE_SPACE_SHIP, BLUE_LASER), }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def main():
    run = True  # Game is running.
    FPS = 60    # Frames per second.
    clock = pygame.time.Clock()  # Get the clock of the game.
    level = 0   # Initial level.
    lives = 5   # Initial lives.
    main_font = pygame.font.Font(   # Loading game's main font.
        os.path.join("assets", "fonts/Silver.ttf"), 50)
    lost_font = pygame.font.Font(
        os.path.join("assets", "fonts/Silver.ttf"), 80)

    player_vel = 15     # Player velocity.
    enemy_vel = 10      # Enemy velocity.
    enemies = []        # Initial empty enemies array.
    # How many enemies ships in a wave. At first is 5 and it's increasing with every new level.
    wave_length = 5
    lost = False        # Flag to detemrinate if the player lost.
    # Used to count how many seconds the lost screen is shown.
    lost_count = 0

    player = Player(300, 650)   # Create the player with a given coordinates.

    # Recursive function to manage the game.
    def redraw_window():
        WINDOW.blit((BG), (0, 0))   # Draw the background in the scrren.
        # Draw text
        lives_label = main_font.render(f"Lives: {lives}", 0, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 0, (255, 255, 255))
        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # Draw the enemies and the player.
        for enemy in enemies:
            enemy.draw(WINDOW)
        player.draw(WINDOW)

        # If the player lost, show the lost message on the screen.
        if lost:
            lost_label = lost_font.render("You lost!!", 0, (255, 255, 255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)  # Run the game at a given FPS.
        redraw_window()  # Call parent function.

        # If there are not lives left or the player's health is 0, then he lost.
        if lives <= 0 or player.health <= 0:
            lost = True
            # Used below to determinate how many seconds the lost message is shown.
            lost_count += 1

        # Show the lost message on the screen for 4 seconds. When the time is up, the 'continue' is not gonna be executed and the loop:
        # 'for event in pygame.event.get():' is going to close the game.
        if lost:
            if lost_count > FPS * 4:
                run = False
            else:
                continue    # Jump at the top of the while loop.

        # If there are no enemies left, add another level and increment the next enemies wave.
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            # Create a random wave of enemies.
            for i in range(wave_length):
                enemy = Enemy(random.randrange(
                    50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # If the player pressed the X in the game window, close the game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Key behaviour.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:    
            player.x -= player_vel  # left
        if keys[pygame.K_d] and (player.x + player.get_width()) + player_vel < WIDTH:    
            player.x += player_vel  # right
        if keys[pygame.K_w] and player.y - player_vel > 0:    
            player.y -= player_vel  # forward
        if keys[pygame.K_s] and (player.y + player.get_height()) + player_vel < HEIGHT:
            player.y += player_vel  # backwards

        # If any enemy touched the bottom of the screen, the player lost a live.
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if (enemy.y + enemy.get_height()) > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


main()
