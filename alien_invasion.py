import pygame

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
BG_COLOR = (186, 191, 148)  # HEX #BABF94

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Invasion")

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with background color
    screen.fill(BG_COLOR)
    
    # Update the display
    pygame.display.flip()

pygame.quit()
