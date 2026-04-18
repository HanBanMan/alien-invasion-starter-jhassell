import pygame
import random
from pygame.sprite import Group
from types import SimpleNamespace
from settings import Settings
from ship import Ship
from bullet import Bullet


def _check_events(ship, bullets, settings, screen, last_bullet_time):
    """Handle all events and key presses."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, last_bullet_time
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False
    
    # Check for continuous spacebar press with fire rate limit
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    if keys[pygame.K_SPACE]:
        if len(bullets) < 3 and (current_time - last_bullet_time) >= settings.bullet_fire_rate:
            ai_game = SimpleNamespace(screen=screen, settings=settings, ship=ship)
            new_bullet = Bullet(ai_game)
            bullets.add(new_bullet)
            last_bullet_time = current_time
    
    return True, last_bullet_time


def _update_bullets(bullets):
    """Update bullet positions and remove bullets that have gone off screen."""
    bullets.update()


def _update_screen(screen, settings, ship, bullets):
    """Draw all game objects and update the display."""
    # Fill the screen with chalkboard background color
    screen.fill(settings.bg_color)

    # Add a subtle chalkboard texture overlay
    chalk_overlay = pygame.Surface((settings.screen_width, settings.screen_height), pygame.SRCALPHA)
    chalk_overlay.fill((0, 0, 0, 0))
    chalk_line_color = (120, 150, 115, 25)
    chalk_spot_color = (220, 240, 205, 18)

    for y in range(30, settings.screen_height, 70):
        pygame.draw.line(chalk_overlay, chalk_line_color, (0, y), (settings.screen_width, y), 1)
    for _ in range(35):
        start_x = random.randint(0, settings.screen_width)
        start_y = random.randint(0, settings.screen_height)
        end_x = start_x + random.randint(-18, 18)
        end_y = start_y + random.randint(-4, 4)
        pygame.draw.line(chalk_overlay, chalk_spot_color, (start_x, start_y), (end_x, end_y), 1)
        pygame.draw.circle(chalk_overlay, chalk_spot_color, (start_x, start_y), 1)
    screen.blit(chalk_overlay, (0, 0))

    # Draw the ship
    ship.blitme()

    # Draw bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw bullet count
    font = pygame.font.Font(None, 36)
    bullet_count_text = font.render(f"Bullets: {len(bullets)}/3", True, (240, 240, 240))
    screen.blit(bullet_count_text, (10, 10))

    # Update the display
    pygame.display.flip()


# Initialize Pygame
pygame.init()

# Create a settings object
settings = Settings()

# Set up the display
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Alien Invasion")

# Create the ship
ship = Ship(screen, settings)

# Create a group to store active bullets
bullets = Group()

# Track bullet fire rate
last_bullet_time = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    
    # Check events
    running, last_bullet_time = _check_events(ship, bullets, settings, screen, last_bullet_time)
    
    # Update ship position
    ship.update()
    
    # Update bullets
    _update_bullets(bullets)
    
    # Update screen
    _update_screen(screen, settings, ship, bullets)

pygame.quit()
