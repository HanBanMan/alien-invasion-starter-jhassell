import pygame
import random
from pygame.sprite import Sprite


class Enemy(Sprite):
    """A class to manage an enemy (grade)."""
    
    # Grade options for enemies
    GRADES = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F+", "F", "F-"]
    GRADE_COLORS = {
        "A+": (160, 255, 160),
        "A": (130, 240, 100),
        "A-": (100, 210, 80),
        "B+": (120, 180, 255),
        "B": (90, 150, 220),
        "B-": (70, 130, 190),
        "C+": (255, 210, 100),
        "C": (235, 180, 70),
        "C-": (210, 135, 45),
        "D+": (255, 175, 105),
        "D": (220, 150, 70),
        "D-": (190, 115, 55),
        "F+": (255, 120, 120),
        "F": (240, 90, 90),
        "F-": (210, 60, 60),
    }
    
    def __init__(self, ai_game, x, y, grade_index, color=(255, 100, 100), scale=1.0):
        """Create an enemy at the given position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Create the enemy surface and rect
        self.grade = self.GRADES[grade_index % len(self.GRADES)]
        self.scale = scale
        self.base_size = 40
        self.size = int(self.base_size * scale)
        
        self.color = self.GRADE_COLORS.get(self.grade, color)
        font_size = max(20, int(28 * scale))
        font = pygame.font.Font(None, font_size)
        grade_text = font.render(self.grade, True, self.color)
        shadow = font.render(self.grade, True, (30, 30, 30))
        padding_x = 14
        padding_y = 10
        width = grade_text.get_width() + padding_x * 2
        height = grade_text.get_height() + padding_y * 2
        self.size = width
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        
        shadow_rect = shadow.get_rect(center=(width // 2 + 1, height // 2 + 1))
        grade_rect = grade_text.get_rect(center=(width // 2, height // 2))
        self.image.blit(shadow, shadow_rect)
        self.image.blit(grade_text, grade_rect)
        
        self.rect = self.image.get_rect()
        self.starting_x = x  # Store starting position for formation
        self.starting_y = y
        self.rect.x = x
        self.rect.y = y
        
        # Movement
        self.vx = 0
        self.vy = 0
        self.state = 'formation'  # 'formation', 'regrouping', 'breakoff'
        self.breakoff_timer = 0
        self.regroup_target_x = x
        self.regroup_target_y = y
    
    def start_regroup(self, target_x, target_y):
        """Send the enemy toward a tighter regroup position."""
        self.state = 'regrouping'
        self.regroup_target_x = target_x
        self.regroup_target_y = target_y
        self.vx = 0
        self.vy = 0
    
    def start_breakoff(self):
        """Start the enemy’s breakoff movement with a random direction."""
        self.state = 'breakoff'
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = 0
        self.breakoff_timer = random.randint(90, 180)
    
    def update(self, fleet_x_offset=None):
        """Update enemy position based on movement state."""
        if self.state == 'formation' and fleet_x_offset is not None:
            self.rect.x = self.starting_x + fleet_x_offset
            self.rect.y = self.starting_y
        elif self.state == 'regrouping':
            self.rect.x += (self.regroup_target_x - self.rect.x) * 0.09
            self.rect.y += (self.regroup_target_y - self.rect.y) * 0.09
            if abs(self.rect.x - self.regroup_target_x) < 2 and abs(self.rect.y - self.regroup_target_y) < 2:
                self.state = 'formation'
                self.starting_x = self.regroup_target_x
                self.starting_y = self.regroup_target_y
                self.rect.x = self.regroup_target_x
                self.rect.y = self.regroup_target_y
        elif self.state == 'breakoff':
            self.rect.x += self.vx
            
            # Slow horizontal jitter only; never move vertically during breakoff.
            if random.random() < 0.03:
                self.vx += random.uniform(-0.6, 0.6)
            self.vx = max(-2.0, min(2.0, self.vx))

            if self.rect.left <= 0 or self.rect.right >= self.screen_rect.width:
                self.vx *= -1
            self.rect.x = max(0, min(self.rect.x, self.screen_rect.width - self.size))
            self.rect.y = max(50, min(self.rect.y, self.screen_rect.height - 80))
    
    def draw(self):
        """Draw the enemy to the screen."""
        self.screen.blit(self.image, self.rect)
