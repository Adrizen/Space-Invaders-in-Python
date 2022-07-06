from turtle import width
import pygame
import os
import time
import random
pygame.font.init()

# Game dimension.
WIDTH, HEIGHT = 1024, 768

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images.
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
GRENN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))

# Player's ship.
RED_SPACE_SHIP = pygame.image.load(
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

class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0
    def draw(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50), 0)

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    level = 1
    lives = 5
    main_font = pygame.font.Font(os.path.join("assets", "fonts/Silver.ttf"), 50)

    ship = Ship(300,650)

    def redraw_window():
        WIN.blit((BG), (0, 0))
        # Draw text
        lives_label = main_font.render(f"Lives: {level}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {lives}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, ( WIDTH - level_label.get_width() - 10 , 10))

        ship.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
