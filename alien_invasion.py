import pygame
from settings import Settings
from ship import Ship

# Initialize Pygame
pygame.init()

# Create a settings object
settings = Settings()

# Set up the display
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Alien Invasion")

# Create the ship
ship = Ship(screen, settings)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with background color
    screen.fill(settings.bg_color)
    
    # Draw the ship
    ship.blitme()
    
    # Update the display
    pygame.display.flip()

pygame.quit()
