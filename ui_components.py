"""
Modern UI Components for AI Physiotherapy System
"""
import pygame
import time
from typing import Optional, Tuple

# Import colors from main file
COLOR_BG = (15, 15, 25)
COLOR_PRIMARY = (100, 200, 255)
COLOR_SECONDARY = (150, 100, 255)
COLOR_SUCCESS = (100, 255, 150)
COLOR_WARNING = (255, 200, 100)
COLOR_TEXT = (220, 220, 230)

class ModernButton:
    """Modern card-style button with hover effect"""
    
    def __init__(self, x, y, width, height, text, icon=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = icon
        self.hover_start = None
        self.duration = 1.5
        self.activated = False
        
    def update(self, cursor_pos: Optional[Tuple[int, int]]) -> bool:
        """Returns True when button is activated"""
        if cursor_pos is None:
            self.hover_start = None
            return False
        
        if self.rect.collidepoint(cursor_pos):
            if self.hover_start is None:
                self.hover_start = time.time()
            
            elapsed = time.time() - self.hover_start
            if elapsed >= self.duration:
                self.hover_start = None
                return True
        else:
            self.hover_start = None
        
        return False
    
    def draw(self, screen, font_large, font_small):
        """Draw modern button with card style"""
        is_hovering = self.hover_start is not None
        
        # Card background with gradient effect
        if is_hovering:
            color = (40, 50, 70)
            border_color = COLOR_PRIMARY
        else:
            color = (25, 30, 45)
            border_color = (60, 70, 90)
        
        # Draw card
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=15)
        
        # Draw icon
        if self.icon:
            icon_surf = font_large.render(self.icon, True, COLOR_PRIMARY)
            icon_rect = icon_surf.get_rect(center=(self.rect.centerx, self.rect.centery - 20))
            screen.blit(icon_surf, icon_rect)
        
        # Draw text
        text_surf = font_small.render(self.text, True, COLOR_TEXT)
        text_y = self.rect.centery + 25 if self.icon else self.rect.centery
        text_rect = text_surf.get_rect(center=(self.rect.centerx, text_y))
        screen.blit(text_surf, text_rect)
        
        # Progress bar
        if is_hovering:
            elapsed = time.time() - self.hover_start
            progress = min(elapsed / self.duration, 1.0)
            
            bar_width = self.rect.width - 20
            bar_height = 6
            bar_x = self.rect.x + 10
            bar_y = self.rect.bottom - 12
            
            pygame.draw.rect(screen, (40, 40, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=3)
            filled = int(bar_width * progress)
            if filled > 0:
                pygame.draw.rect(screen, COLOR_SUCCESS, (bar_x, bar_y, filled, bar_height), border_radius=3)


class LevelCard:
    """Level selection card with stats"""
    
    def __init__(self, x, y, width, height, level_num, title, best_score=0, stars=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.level_num = level_num
        self.title = title
        self.best_score = best_score
        self.stars = stars
        self.hover_start = None
        self.duration = 1.5
        
    def update(self, cursor_pos: Optional[Tuple[int, int]]) -> bool:
        """Returns True when card is activated"""
        if cursor_pos is None:
            self.hover_start = None
            return False
        
        if self.rect.collidepoint(cursor_pos):
            if self.hover_start is None:
                self.hover_start = time.time()
            
            elapsed = time.time() - self.hover_start
            if elapsed >= self.duration:
                self.hover_start = None
                return True
        else:
            self.hover_start = None
        
        return False
    
    def draw(self, screen, font_large, font_medium, font_small):
        """Draw level card"""
        is_hovering = self.hover_start is not None
        
        # Card background
        if is_hovering:
            color = (40, 50, 70)
            border_color = COLOR_PRIMARY
        else:
            color = (25, 30, 45)
            border_color = (60, 70, 90)
        
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=12)
        
        # Level number
        level_text = font_large.render(f"LEVEL {self.level_num}", True, COLOR_PRIMARY)
        level_rect = level_text.get_rect(center=(self.rect.centerx, self.rect.y + 40))
        screen.blit(level_text, level_rect)
        
        # Title
        title_text = font_small.render(self.title, True, COLOR_TEXT)
        title_rect = title_text.get_rect(center=(self.rect.centerx, self.rect.y + 75))
        screen.blit(title_text, title_rect)
        
        # Stars
        star_y = self.rect.y + 110
        star_spacing = 30
        start_x = self.rect.centerx - star_spacing
        for i in range(3):
            star_color = COLOR_WARNING if i < self.stars else (60, 60, 70)
            star_text = font_medium.render("★", True, star_color)
            star_rect = star_text.get_rect(center=(start_x + i * star_spacing, star_y))
            screen.blit(star_text, star_rect)
        
        # Best score
        best_text = font_small.render(f"Best: {self.best_score}", True, (150, 150, 160))
        best_rect = best_text.get_rect(center=(self.rect.centerx, self.rect.y + 145))
        screen.blit(best_text, best_rect)
        
        # Play button
        play_rect = pygame.Rect(self.rect.centerx - 50, self.rect.bottom - 50, 100, 35)
        pygame.draw.rect(screen, COLOR_SUCCESS if is_hovering else (60, 120, 80), play_rect, border_radius=8)
        play_text = font_small.render("PLAY", True, COLOR_TEXT)
        play_text_rect = play_text.get_rect(center=play_rect.center)
        screen.blit(play_text, play_text_rect)
        
        # Progress bar
        if is_hovering:
            elapsed = time.time() - self.hover_start
            progress = min(elapsed / self.duration, 1.0)
            
            bar_width = 100
            bar_height = 4
            bar_x = self.rect.centerx - 50
            bar_y = self.rect.bottom - 10
            
            pygame.draw.rect(screen, (40, 40, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=2)
            filled = int(bar_width * progress)
            if filled > 0:
                pygame.draw.rect(screen, COLOR_SUCCESS, (bar_x, bar_y, filled, bar_height), border_radius=2)


class BackButton:
    """Simple back button"""
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 120, 40)
        self.hover_start = None
        self.duration = 0.8
        
    def update(self, cursor_pos: Optional[Tuple[int, int]]) -> bool:
        if cursor_pos is None:
            self.hover_start = None
            return False
        
        if self.rect.collidepoint(cursor_pos):
            if self.hover_start is None:
                self.hover_start = time.time()
            
            elapsed = time.time() - self.hover_start
            if elapsed >= self.duration:
                self.hover_start = None
                return True
        else:
            self.hover_start = None
        
        return False
    
    def draw(self, screen, font):
        is_hovering = self.hover_start is not None
        
        color = (50, 60, 80) if is_hovering else (30, 40, 60)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_PRIMARY if is_hovering else (70, 80, 100), self.rect, 2, border_radius=8)
        
        text = font.render("← BACK", True, COLOR_TEXT)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        
        if is_hovering:
            elapsed = time.time() - self.hover_start
            progress = min(elapsed / self.duration, 1.0)
            bar_width = self.rect.width - 10
            bar_x = self.rect.x + 5
            bar_y = self.rect.bottom - 6
            filled = int(bar_width * progress)
            if filled > 0:
                pygame.draw.rect(screen, COLOR_PRIMARY, (bar_x, bar_y, filled, 3), border_radius=2)
