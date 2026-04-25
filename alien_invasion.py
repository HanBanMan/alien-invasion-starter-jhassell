import math
import pygame
import random
from pygame.sprite import Group
from types import SimpleNamespace
from settings import Settings
from ship import Ship
from bullet import Bullet
from enemy import Enemy
from enemy_bullet import EnemyBullet


def create_fleet(screen, settings, round_num):
    """Create a new fleet of enemies with increasing difficulty."""
    enemies = Group()
    import random
    
    # Determine formation size based on round
    base_configs = [
        [[9, 7, 5]],
        [[11, 9, 7]],
        [[13, 11, 9]]
    ]
    base_enemies_config = base_configs[min(round_num - 1, 2)]
    colors = [(255, 100, 100), (100, 200, 255), (100, 255, 100)][min(round_num - 1, 2)]
    scale = max(0.7, 1.0 - ((round_num - 1) // 4) * 0.1)  # Larger at start (1.0), smaller every 4 rounds
    sample_width = 0
    sample_height = 0
    for idx in range(len(Enemy.GRADES)):
        sample_enemy = Enemy(
            SimpleNamespace(screen=screen, settings=settings),
            0, 0, idx, colors, scale
        )
        sample_width = max(sample_width, sample_enemy.rect.width)
        sample_height = max(sample_height, sample_enemy.rect.height)
    enemy_size = sample_width
    grid_step = enemy_size + 20
    row_height = sample_height + 16
    
    # Choose formation pattern
    if round_num >= 4 and random.random() < 0.33:
        pattern_choice = 'poly1203'
    else:
        pattern_choice = random.choice(['pyramid', 'circles', 'triangles', 'smiley'])
    
    enemy_index = 0
    
    if pattern_choice == 'pyramid':
        # Original pyramid formation
        y_positions = [120, 120 + row_height, 120 + row_height * 2]
        for row_idx, enemy_count in enumerate(base_enemies_config[0]):
            min_spacing = enemy_size + 10
            available_width = settings.screen_width - 80
            x_spacing = min(grid_step, max(min_spacing, (available_width - enemy_size) // max(enemy_count - 1, 1)))
            row_width = enemy_size + (enemy_count - 1) * x_spacing
            x_start = max(20, (settings.screen_width - row_width) // 2)
            for i in range(enemy_count):
                x = x_start + i * x_spacing
                y = y_positions[row_idx]
                enemy = Enemy(
                    SimpleNamespace(screen=screen, settings=settings),
                    x, y, enemy_index, colors, scale
                )
                enemies.add(enemy)
                enemy_index += 1
    
    elif pattern_choice == 'circles':
        # Three circular groups
        centers = [(150, 130), (400, 150), (650, 130)]
        enemies_per_circle = [7, 6, 5]
        for center_idx, (cx, cy) in enumerate(centers):
            circle_radius = min(140, max(90, grid_step * 1.2))
            for i in range(enemies_per_circle[center_idx]):
                angle = (i / enemies_per_circle[center_idx]) * 2 * math.pi
                x = int(cx + circle_radius * math.cos(angle))
                y = int(cy + circle_radius * math.sin(angle))
                enemy = Enemy(
                    SimpleNamespace(screen=screen, settings=settings),
                    x, y, enemy_index, colors, scale
                )
                enemies.add(enemy)
                enemy_index += 1
    
    elif pattern_choice == 'triangles':
        # Two triangles
        base_centers = [(200, 130), (600, 140)]
        triangle_rows = [[4, 3, 1], [4, 3]]
        for center, rows in zip(base_centers, triangle_rows):
            cx, cy = center
            for row_idx, row_count in enumerate(rows):
                x_start = int(cx - (row_count - 1) * grid_step / 2)
                y = int(cy + row_idx * row_height * 0.9)
                for i in range(row_count):
                    x = x_start + i * grid_step
                    enemy = Enemy(
                        SimpleNamespace(screen=screen, settings=settings),
                        x, y, enemy_index, colors, scale
                    )
                    enemies.add(enemy)
                    enemy_index += 1
    
    elif pattern_choice == 'smiley':
        # Smiley face pattern
        # Head circle
        head_center = (400, 150)
        head_radius = min(140, max(90, grid_step * 1.0))
        for i in range(10):
            angle = (i / 10) * 2 * math.pi
            x = int(head_center[0] + head_radius * math.cos(angle))
            y = int(head_center[1] + head_radius * math.sin(angle))
            enemy = Enemy(
                SimpleNamespace(screen=screen, settings=settings),
                x, y, enemy_index, colors, scale
            )
            enemies.add(enemy)
            enemy_index += 1
        
        # Eyes
        eye_offset = min(40, grid_step // 2)
        for eye_x in [head_center[0] - eye_offset, head_center[0] + eye_offset]:
            enemy = Enemy(
                SimpleNamespace(screen=screen, settings=settings),
                eye_x, head_center[1] - int(head_radius * 0.4), enemy_index, colors, scale
            )
            enemies.add(enemy)
            enemy_index += 1
        
        # Smile
        smile_width = min(140, grid_step * 3)
        for i in range(5):
            x = head_center[0] - smile_width // 2 + i * (smile_width // 4)
            y = head_center[1] + int(head_radius * 0.4) + int((i - 2) ** 2 * 1.2)
            enemy = Enemy(
                SimpleNamespace(screen=screen, settings=settings),
                x, y, enemy_index, colors, scale
            )
            enemies.add(enemy)
            enemy_index += 1

    elif pattern_choice == 'poly1203':
        # Spell out POLY 1203 using enemy positions
        letter_map = {
            'P': [
                (0,0),(1,0),(2,0),
                (0,1),(0,2),(1,2),(2,2),
                (0,3),(0,4)
            ],
            'O': [
                (1,0),(2,0),
                (0,1),(3,1),
                (0,2),(3,2),
                (0,3),(3,3),
                (1,4),(2,4)
            ],
            'L': [
                (0,0),
                (0,1),
                (0,2),
                (0,3),
                (0,4),(1,4),(2,4)
            ],
            'Y': [
                (0,0),(3,0),
                (0,1),(3,1),
                (1,2),(2,2),
                (2,3),(2,4)
            ],
            '1': [
                (1,0),
                (0,1),(1,1),
                (1,2),
                (1,3),
                (0,4),(1,4),(2,4)
            ],
            '2': [
                (0,0),(1,0),(2,0),
                (3,1),
                (0,2),(1,2),(2,2),
                (0,3),
                (0,4),(1,4),(2,4),(3,4)
            ],
            '0': [
                (1,0),(2,0),
                (0,1),(3,1),
                (0,2),(3,2),
                (0,3),(3,3),
                (1,4),(2,4)
            ],
            '3': [
                (0,0),(1,0),(2,0),
                (3,1),
                (1,2),(2,2),
                (3,3),
                (0,4),(1,4),(2,4)
            ]
        }
        text = 'POLY1203'
        cell_w = min(grid_step, max(14, settings.screen_width // 42))
        cell_h = cell_w
        char_spacing = cell_w * 5
        total_width = len(text) * (4 * cell_w) + (len(text) - 1) * (char_spacing - 4 * cell_w)
        start_x = max(20, (settings.screen_width - total_width) // 2)
        start_y = 170
        for char_idx, char in enumerate(text):
            positions = letter_map.get(char, [])
            x_offset = start_x + char_idx * char_spacing
            for pos in positions:
                x = x_offset + pos[0] * cell_w
                y = start_y + pos[1] * cell_h
                x = max(0, min(x, settings.screen_width - grid_step))
                y = max(60, min(y, settings.screen_height - 140))
                enemy = Enemy(
                    SimpleNamespace(screen=screen, settings=settings),
                    x, y, enemy_index, colors, scale
                )
                enemies.add(enemy)
                enemy_index += 1
    
    return enemies


def _generate_regroup_positions(count, settings, grid_step, round_num):
    """Generate a new regroup formation for remaining enemies."""
    patterns = ['pyramid', 'staggered', 'arc']
    pattern = patterns[(round_num - 1) % len(patterns)]
    positions = []
    spacing = max(grid_step, int(grid_step * 1.4))
    if pattern == 'pyramid':
        columns = min(6, max(3, (count + 1) // 2))
        row_gap = spacing
        start_y = 130
        for idx in range(count):
            row = idx // columns
            col = idx % columns
            row_width = (columns - 1) * spacing
            offset_x = (row * (spacing // 2)) if row % 2 else 0
            x = (settings.screen_width - row_width) // 2 + col * spacing - offset_x
            y = start_y + row * row_gap
            x = max(0, min(x, settings.screen_width - spacing))
            y = max(60, min(y, settings.screen_height - 140))
            positions.append((x, y))
    elif pattern == 'staggered':
        columns = min(7, max(3, (count + 1) // 2))
        start_x = (settings.screen_width - (columns - 1) * spacing) // 2
        start_y = 130
        for idx in range(count):
            row = idx // columns
            col = idx % columns
            x = start_x + col * spacing + (spacing // 2 if row % 2 else 0)
            y = start_y + row * spacing
            x = max(0, min(x, settings.screen_width - spacing))
            y = max(60, min(y, settings.screen_height - 140))
            positions.append((x, y))
    else:
        center_x = settings.screen_width // 2
        center_y = 160
        radius = min(180, spacing * (count / 3))
        for idx in range(count):
            angle = math.pi * idx / max(count - 1, 1) + 0.6
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            x = max(0, min(x, settings.screen_width - spacing))
            y = max(60, min(y, settings.screen_height - 140))
            positions.append((x, y))
    return positions


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


def _update_fleet(enemies, fleet_state, settings, screen, enemy_bullets, round_num, total_enemies):
    """Update enemy fleet movement and handle shooting."""
    # Update fleet position
    fleet_state['x_offset'] += fleet_state['direction'] * settings.enemy_speed
    
    # Check for edge collision and handle enemy states
    edge_hit = False
    for enemy in enemies:
        if enemy.state == 'formation':
            enemy.update(fleet_state['x_offset'])
            if enemy.rect.right >= settings.screen_width or enemy.rect.left <= 0:
                edge_hit = True
        else:
            enemy.update()
    
    if edge_hit:
        fleet_state['direction'] *= -1
        for enemy in enemies:
            if enemy.state == 'formation':
                enemy.starting_y += settings.enemy_drop
    
    # Check if half enemies are destroyed - trigger regroup
    if not fleet_state['regrouped'] and len(enemies) <= total_enemies // 2 and total_enemies > 0:
        fleet_state['regrouped'] = True
        surviving = list(enemies)
        sample_step = surviving[0].rect.width + 32
        targets = _generate_regroup_positions(len(surviving), settings, sample_step, round_num)
        fleet_state['x_offset'] = 0
        fleet_state['direction'] = 1
        for enemy, (target_x, target_y) in zip(surviving, targets):
            enemy.state = 'regrouping'
            enemy.regroup_target_x = target_x
            enemy.regroup_target_y = target_y
            enemy.starting_x = target_x
            enemy.starting_y = target_y

    # If regrouped, start breakoff mechanics after survivors return to formation
    if fleet_state['regrouped']:
        formation_enemies = [e for e in enemies if e.state == 'formation']
        if formation_enemies and not fleet_state['breakoff_enemy']:
            fleet_state['breakoff_enemy'] = random.choice(formation_enemies)
            fleet_state['breakoff_enemy'].start_breakoff()
            fleet_state['breakoff_shoot_timer'] = 30
            fleet_state['breakoff_bullets'] = 0

    # Handle breakoff enemy
    if fleet_state['breakoff_enemy']:
        if fleet_state['breakoff_enemy'] not in enemies:
            fleet_state['breakoff_enemy'] = None
        else:
            fleet_state['breakoff_timer'] -= 1
            fleet_state['breakoff_shoot_timer'] -= 1
            
            # Have breakoff enemy shoot 3 bullets in a spread pattern
            if fleet_state['breakoff_shoot_timer'] <= 0:
                for offset in (-12, 0, 12):
                    bullet = EnemyBullet(
                        SimpleNamespace(screen=screen, settings=settings),
                        fleet_state['breakoff_enemy'].rect.centerx + offset,
                        fleet_state['breakoff_enemy'].rect.bottom,
                        color=fleet_state['breakoff_enemy'].color
                    )
                    enemy_bullets.add(bullet)
                fleet_state['breakoff_shoot_timer'] = 40
        
            # If timer expires, send enemy back to regroup
            if fleet_state['breakoff_timer'] <= 0:
                fleet_state['breakoff_enemy'].start_regroup(
                    fleet_state['breakoff_enemy'].starting_x,
                    fleet_state['breakoff_enemy'].starting_y
                )
                fleet_state['breakoff_enemy'] = None
                fleet_state['breakoff_bullets'] = 0
    
    # Enemy shooting continues even after regrouping
    fleet_state['shoot_timer'] -= 1
    if fleet_state['shoot_timer'] <= 0 and len(enemies) > 0:
        shooting_candidates = [e for e in enemies if e.state != 'breakoff']
        if shooting_candidates:
            shooting_enemy = random.choice(shooting_candidates)
        else:
            shooting_enemy = random.choice(list(enemies))
        bullet = EnemyBullet(
            SimpleNamespace(screen=screen, settings=settings),
            shooting_enemy.rect.centerx,
            shooting_enemy.rect.bottom,
            color=shooting_enemy.color
        )
        enemy_bullets.add(bullet)
        fleet_state['shoot_timer'] = random.randint(30, 120)


def _update_bullets(bullets, enemies, score, total_enemies):
    """Update player bullet positions and check collisions."""
    bullets.update()
    
    # Check for collisions between bullets and enemies
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if collisions:
        score[0] += len(collisions)
    
    return score


def _update_enemy_bullets(enemy_bullets, ship, ship_rect, game_state):
    """Update enemy bullet positions and check collisions with ship."""
    enemy_bullets.update()
    
    # Check for collisions with ship
    hits = pygame.sprite.spritecollide(ship, enemy_bullets, True)
    if hits:
        for hit in hits:
            game_state['hp'] -= game_state['settings'].enemy_bullet_damage
    
    return game_state


def _draw_screen(screen, settings, ship, bullets, enemies, enemy_bullets, score, total_enemies, game_state, round_num, game_over_message):
    """Draw all game objects and update the display."""
    # Fill the screen with chalkboard background color
    screen.fill(settings.bg_color)

    # Add a chalkboard header and classroom notes
    title_font = pygame.font.Font(None, 40)
    subtitle_font = pygame.font.Font(None, 20)
    title_text = title_font.render("POLY 1203 RULES!", True, (235, 235, 210))
    title_shadow = title_font.render("POLY 1203 RULES!", True, (40, 45, 35))
    title_rect = title_text.get_rect(topright=(settings.screen_width - 24, 24))
    title_shadow_rect = title_shadow.get_rect(topleft=(title_rect.left + 2, title_rect.top + 2))
    screen.blit(title_shadow, title_shadow_rect)
    screen.blit(title_text, title_rect)
    pygame.draw.line(screen, (210, 230, 180), (title_rect.left, title_rect.bottom + 6), (title_rect.right, title_rect.bottom + 6), 2)
    subtitle = subtitle_font.render("No tardies. No excuses. Beat the grade swarm!", True, (220, 235, 180))
    screen.blit(subtitle, (title_rect.left, title_rect.bottom + 12))

    # Add chalk dust and faint smudges around the title
    chalk_dust = pygame.Surface((title_rect.width + 16, title_rect.height + 16), pygame.SRCALPHA)
    for _ in range(12):
        dust_x = random.randint(0, chalk_dust.get_width() - 1)
        dust_y = random.randint(0, chalk_dust.get_height() - 1)
        pygame.draw.circle(chalk_dust, (245, 245, 220, 40), (dust_x, dust_y), random.randint(1, 2))
    screen.blit(chalk_dust, (title_rect.left - 8, title_rect.top - 4))

    # Add a subtle chalkboard texture overlay
    chalk_overlay = pygame.Surface((settings.screen_width, settings.screen_height), pygame.SRCALPHA)
    chalk_overlay.fill((0, 0, 0, 0))
    chalk_line_color = (120, 150, 115, 25)
    chalk_spot_color = (220, 240, 205, 18)

    for y in range(30, settings.screen_height, 70):
        pygame.draw.line(chalk_overlay, chalk_line_color, (0, y), (settings.screen_width, y), 1)
    for _ in range(22):
        start_x = random.randint(0, settings.screen_width)
        start_y = random.randint(0, settings.screen_height)
        end_x = start_x + random.randint(-12, 12)
        end_y = start_y + random.randint(-3, 3)
        pygame.draw.line(chalk_overlay, chalk_spot_color, (start_x, start_y), (end_x, end_y), 1)
    screen.blit(chalk_overlay, (0, 0))

    # Draw the ship
    ship.blitme()

    # Draw enemies
    for enemy in enemies.sprites():
        enemy.draw()

    # Draw player bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    # Draw enemy bullets
    for bullet in enemy_bullets.sprites():
        bullet.draw()

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score[0]}/{total_enemies}", True, (240, 240, 240))
    screen.blit(score_text, (550, 10))

    # Draw bullet count
    bullet_count_text = font.render(f"Bullets: {len(bullets)}/3", True, (240, 240, 240))
    screen.blit(bullet_count_text, (10, 10))
    
    # Draw round number
    round_text = font.render(f"Round: {round_num}", True, (240, 240, 240))
    screen.blit(round_text, (300, 10))

    # Draw HP bar
    hp_bar_width = 200
    hp_bar_height = 20
    hp_bar_x = settings.screen_width - hp_bar_width - 10
    hp_bar_y = settings.screen_height - hp_bar_height - 10
    
    # HP background
    pygame.draw.rect(screen, (50, 50, 50), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
    
    # HP fill
    hp_percentage = max(0, game_state['hp'] / settings.max_hp)
    hp_fill_width = hp_bar_width * hp_percentage
    hp_color = (0, 200, 0) if hp_percentage > 0.3 else (200, 50, 0) if hp_percentage > 0.1 else (200, 0, 0)
    pygame.draw.rect(screen, hp_color, (hp_bar_x, hp_bar_y, hp_fill_width, hp_bar_height))
    
    # HP border
    pygame.draw.rect(screen, (200, 200, 200), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 2)
    
    # HP text
    hp_text = font.render(f"HP: {max(0, game_state['hp'])}/100", True, (240, 240, 240))
    screen.blit(hp_text, (hp_bar_x, hp_bar_y - 30))
    
    # Draw game over message if applicable
    if game_over_message:
        # Use a smaller font that fits the screen width better
        large_font = pygame.font.Font(None, 48)
        message_text = large_font.render(game_over_message, True, (255, 255, 100))
        text_rect = message_text.get_rect(center=(settings.screen_width // 2, settings.screen_height // 2 - 30))
        
        # Draw semi-transparent background
        bg_rect = text_rect.inflate(60, 60)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 200))
        screen.blit(bg_surface, bg_rect)
        
        screen.blit(message_text, text_rect)
        
        # Draw help message in small font
        small_font = pygame.font.Font(None, 24)
        if "held back" in game_over_message:
            help_text = small_font.render("Press the space bar to start the semester over.", True, (200, 200, 200))
        else:
            help_text = small_font.render("Press the Space Bar to advance to the next round", True, (200, 200, 200))
        help_rect = help_text.get_rect(center=(settings.screen_width // 2, settings.screen_height // 2 + 40))
        screen.blit(help_text, help_rect)

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

# Game state
round_num = 1
game_state = {'hp': 100, 'settings': settings}

# Create initial fleet
bullets = Group()
enemies = create_fleet(screen, settings, round_num)
enemy_bullets = Group()

# Calculate total enemies for this round
total_enemies = len(enemies)

# Track bullet fire rate
last_bullet_time = 0

# Track score
score = [0]

# Fleet state
fleet_state = {
    'x_offset': 0,
    'direction': 1,
    'shoot_timer': 0,
    'regrouped': False,
    'regroup_finished': False,
    'breakoff_enemy': None,
    'breakoff_timer': 0,
    'breakoff_shoot_timer': 0
}

# Game over message
game_over_message = None
game_over_type = None  # Track if it's 'win' or 'loss'

# Game loop
running = True
clock = pygame.time.Clock()
waiting_for_next_round = False

while running:
    clock.tick(60)
    
    # Check events
    running, last_bullet_time = _check_events(ship, bullets, settings, screen, last_bullet_time)
    
    # If waiting for next round, check for spacebar press
    if waiting_for_next_round:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state['hp'] = 100
            
            # Only increment round if it was a win
            if game_over_type == 'win':
                round_num += 1
            # If loss, keep same round_num to retry the round
            
            # Update settings for increased difficulty
            settings.enemy_bullet_damage = 10 + (round_num - 1) * 5
            settings.enemy_speed = 1 + (round_num - 1) * 0.2
            settings.bullet_fire_rate = max(100, 300 - (round_num - 1) * 50)
            
            # Create new fleet
            enemies = create_fleet(screen, settings, round_num)
            total_enemies = len(enemies)
            
            bullets.empty()
            enemy_bullets.empty()
            fleet_state = {
                'x_offset': 0,
                'direction': 1,
                'shoot_timer': 0,
                'regrouped': False,
                'regroup_finished': False,
                'breakoff_enemy': None,
                'breakoff_timer': 0,
                'breakoff_shoot_timer': 0
            }
            score = [0]
            game_over_message = None
            game_over_type = None
            waiting_for_next_round = False
    elif game_over_message is None:
        # Update ship position
        ship.update()
        
        # Update enemies
        _update_fleet(enemies, fleet_state, settings, screen, enemy_bullets, round_num, total_enemies)
        
        # Update player bullets
        score = _update_bullets(bullets, enemies, score, total_enemies)
        
        # Update enemy bullets
        game_state = _update_enemy_bullets(enemy_bullets, ship, ship.rect, game_state)
        
        # Check win condition
        if len(enemies) == 0 and game_state['hp'] > 0:
            game_over_message = "Congrats, You've completed the semester!"
            game_over_type = 'win'
            waiting_for_next_round = True
        
        # Check lose condition
        elif game_state['hp'] <= 0:
            game_over_message = "Womp Womp, You've been held back"
            game_over_type = 'loss'
            waiting_for_next_round = True
    
    # Draw screen
    _draw_screen(screen, settings, ship, bullets, enemies, enemy_bullets, score, total_enemies, game_state, round_num, game_over_message)

pygame.quit()
