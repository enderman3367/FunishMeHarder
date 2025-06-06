"""
Character Select - Two-Player Fighter Selection Interface
=========================================================

Character selection screen where both players choose their fighters.
Features character portraits, stats display, and smooth selection animations.

Features:
- Two-player simultaneous character selection
- Red (Player 1) and Blue (Player 2) selection cursors
- Character preview with stats and descriptions
- Key hints for both players
- Confirmation system before proceeding

Controls:
- Player 1: WASD to move cursor, Q to select/confirm
- Player 2: IJKL to move cursor, U to select/confirm
"""

import pygame
from src.core.state_manager import GameState, GameStateType
from src.characters.warrior import Warrior
from src.characters.speedster import Speedster
from src.characters.heavy import Heavy
from enum import Enum

class SelectionState(Enum):
    """
    Current state of character selection process
    """
    SELECTING = "selecting"
    BOTH_CONFIRMED = "both_confirmed"
    TRANSITIONING = "transitioning"

class CharacterSelectState(GameState):
    """
    Two-player character selection screen
    """
    
    def __init__(self, state_manager):
        """
        Initialize character select screen
        """
        super().__init__(state_manager)
        
        # Available characters
        self.characters = [
            {"name": "Warrior", "class": Warrior, "archetype": "Balanced", "difficulty": "Beginner"},
            {"name": "Speedster", "class": Speedster, "archetype": "Rushdown", "difficulty": "Advanced"}, 
            {"name": "Heavy", "class": Heavy, "archetype": "Grappler", "difficulty": "Intermediate"}
        ]
        
        # Player selections
        self.player1_cursor = 0  # Current cursor position
        self.player2_cursor = 0
        self.player1_selection = None  # Confirmed selection
        self.player2_selection = None
        
        # Selection state
        self.current_state = SelectionState.SELECTING
        self.transition_timer = 0.0
        
        # Visual properties
        self.character_box_width = 200
        self.character_box_height = 250
        self.character_spacing = 50
        self.grid_start_x = 640 - (len(self.characters) * (self.character_box_width + self.character_spacing) - self.character_spacing) // 2
        self.grid_y = 200
        
        # Colors
        self.player1_color = (255, 100, 100)  # Red
        self.player2_color = (100, 150, 255)  # Blue
        self.confirmed_color = (100, 255, 100)  # Green
        self.background_color = (30, 30, 50)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.character_font = pygame.font.Font(None, 32)
        self.info_font = pygame.font.Font(None, 24)
        self.hint_font = pygame.font.Font(None, 20)
    
    def enter(self):
        """
        Called when entering character select
        """
        # Reset selections
        self.player1_cursor = 0
        self.player2_cursor = 0
        self.player1_selection = None
        self.player2_selection = None
        self.current_state = SelectionState.SELECTING
        
        print("Entering character select screen")
    
    def exit(self):
        """
        Called when leaving character select
        """
        print("Exiting character select screen")
    
    def handle_event(self, event):
        """
        Handle character select input events
        """
        if event.type == pygame.KEYDOWN:
            # Player 1 controls (WASD + Q)
            if event.key == pygame.K_a:  # Left
                if self.player1_selection is None:
                    self.player1_cursor = (self.player1_cursor - 1) % len(self.characters)
                    self.play_navigate_sound()
            elif event.key == pygame.K_d:  # Right
                if self.player1_selection is None:
                    self.player1_cursor = (self.player1_cursor + 1) % len(self.characters)
                    self.play_navigate_sound()
            elif event.key == pygame.K_q:  # Confirm/Select
                if self.player1_selection is None:
                    self.player1_selection = self.player1_cursor
                    self.play_confirm_sound()
                    print(f"Player 1 selected {self.characters[self.player1_selection]['name']}")
                    self.check_both_selected()
            
            # Player 2 controls (IJKL + U)
            elif event.key == pygame.K_j:  # Left
                if self.player2_selection is None:
                    self.player2_cursor = (self.player2_cursor - 1) % len(self.characters)
                    self.play_navigate_sound()
            elif event.key == pygame.K_l:  # Right
                if self.player2_selection is None:
                    self.player2_cursor = (self.player2_cursor + 1) % len(self.characters)
                    self.play_navigate_sound()
            elif event.key == pygame.K_u:  # Confirm/Select
                if self.player2_selection is None:
                    self.player2_selection = self.player2_cursor
                    self.play_confirm_sound()
                    print(f"Player 2 selected {self.characters[self.player2_selection]['name']}")
                    self.check_both_selected()
            
            # Global controls
            elif event.key == pygame.K_ESCAPE:
                # Go back to main menu
                self.state_manager.change_state(GameStateType.MAIN_MENU)
                return True
        
        return False
    
    def check_both_selected(self):
        """
        Check if both players have selected and proceed
        """
        if self.player1_selection is not None and self.player2_selection is not None:
            self.current_state = SelectionState.BOTH_CONFIRMED
            self.transition_timer = 1.0  # 1 second delay before transition
            print("Both players selected! Proceeding to stage select...")
    
    def play_navigate_sound(self):
        """
        Play navigation sound effect
        """
        # TODO: Add sound effect
        pass
    
    def play_confirm_sound(self):
        """
        Play confirmation sound effect
        """
        # TODO: Add sound effect
        pass
    
    def update(self, delta_time):
        """
        Update character select logic
        """
        if self.current_state == SelectionState.BOTH_CONFIRMED:
            self.transition_timer -= delta_time
            if self.transition_timer <= 0:
                # Store selections in state manager for later use
                self.state_manager.selected_characters = {
                    'player1': self.characters[self.player1_selection],
                    'player2': self.characters[self.player2_selection]
                }
                # Proceed to stage select
                self.state_manager.change_state(GameStateType.STAGE_SELECT)
    
    def render(self, screen):
        """
        Render the character select screen
        """
        screen.fill(self.background_color)
        
        # Render title
        title_text = self.title_font.render("SELECT YOUR FIGHTER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(640, 80))
        screen.blit(title_text, title_rect)
        
        # Render character boxes
        for i, character in enumerate(self.characters):
            self.render_character_box(screen, character, i)
        
        # Render player cursors
        self.render_player_cursors(screen)
        
        # Render player info panels
        self.render_player_panels(screen)
        
        # Render controls hints
        self.render_control_hints(screen)
        
        # Render transition state
        if self.current_state == SelectionState.BOTH_CONFIRMED:
            self.render_transition_overlay(screen)
    
    def render_character_box(self, screen, character, index):
        """
        Render individual character selection box
        """
        box_x = self.grid_start_x + index * (self.character_box_width + self.character_spacing)
        box_y = self.grid_y
        
        # Character box background
        box_rect = pygame.Rect(box_x, box_y, self.character_box_width, self.character_box_height)
        pygame.draw.rect(screen, (60, 60, 80), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        
        # Character portrait placeholder (large colored rectangle)
        portrait_rect = pygame.Rect(box_x + 25, box_y + 20, 150, 120)
        character_colors = {
            "Warrior": (200, 150, 100),
            "Speedster": (255, 255, 100), 
            "Heavy": (150, 100, 200)
        }
        portrait_color = character_colors.get(character["name"], (150, 150, 150))
        pygame.draw.rect(screen, portrait_color, portrait_rect)
        pygame.draw.rect(screen, (255, 255, 255), portrait_rect, 2)
        
        # Character name
        name_text = self.character_font.render(character["name"], True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(box_x + self.character_box_width // 2, box_y + 160))
        screen.blit(name_text, name_rect)
        
        # Character archetype
        archetype_text = self.info_font.render(character["archetype"], True, (200, 200, 200))
        archetype_rect = archetype_text.get_rect(center=(box_x + self.character_box_width // 2, box_y + 185))
        screen.blit(archetype_text, archetype_rect)
        
        # Character difficulty
        difficulty_text = self.info_font.render(f"Difficulty: {character['difficulty']}", True, (150, 150, 150))
        difficulty_rect = difficulty_text.get_rect(center=(box_x + self.character_box_width // 2, box_y + 210))
        screen.blit(difficulty_text, difficulty_rect)
    
    def render_player_cursors(self, screen):
        """
        Render selection cursors for both players
        """
        # Player 1 cursor (Red)
        if self.player1_selection is None:
            p1_box_x = self.grid_start_x + self.player1_cursor * (self.character_box_width + self.character_spacing)
            p1_cursor_rect = pygame.Rect(p1_box_x - 5, self.grid_y - 5, self.character_box_width + 10, self.character_box_height + 10)
            pygame.draw.rect(screen, self.player1_color, p1_cursor_rect, 4)
        else:
            # Show confirmed selection
            p1_box_x = self.grid_start_x + self.player1_selection * (self.character_box_width + self.character_spacing)
            p1_cursor_rect = pygame.Rect(p1_box_x - 5, self.grid_y - 5, self.character_box_width + 10, self.character_box_height + 10)
            pygame.draw.rect(screen, self.confirmed_color, p1_cursor_rect, 6)
        
        # Player 2 cursor (Blue)
        if self.player2_selection is None:
            p2_box_x = self.grid_start_x + self.player2_cursor * (self.character_box_width + self.character_spacing)
            p2_cursor_rect = pygame.Rect(p2_box_x - 8, self.grid_y - 8, self.character_box_width + 16, self.character_box_height + 16)
            pygame.draw.rect(screen, self.player2_color, p2_cursor_rect, 4)
        else:
            # Show confirmed selection  
            p2_box_x = self.grid_start_x + self.player2_selection * (self.character_box_width + self.character_spacing)
            p2_cursor_rect = pygame.Rect(p2_box_x - 8, self.grid_y - 8, self.character_box_width + 16, self.character_box_height + 16)
            pygame.draw.rect(screen, self.confirmed_color, p2_cursor_rect, 6)
    
    def render_player_panels(self, screen):
        """
        Render information panels for both players
        """
        # Player 1 panel (left side)
        self.render_player_panel(screen, 1, 50, 500, self.player1_cursor, self.player1_selection)
        
        # Player 2 panel (right side)
        self.render_player_panel(screen, 2, 1280 - 350, 500, self.player2_cursor, self.player2_selection)
    
    def render_player_panel(self, screen, player, x, y, cursor_pos, selection):
        """
        Render information panel for a specific player
        """
        # Panel background
        panel_rect = pygame.Rect(x, y, 300, 180)
        pygame.draw.rect(screen, (40, 40, 60), panel_rect)
        pygame.draw.rect(screen, (255, 255, 255), panel_rect, 2)
        
        # Player title
        color = self.player1_color if player == 1 else self.player2_color
        if selection is not None:
            color = self.confirmed_color
            
        title_text = self.character_font.render(f"Player {player}", True, color)
        screen.blit(title_text, (x + 10, y + 10))
        
        # Status
        if selection is not None:
            status_text = self.info_font.render("READY!", True, self.confirmed_color)
            character_name = self.characters[selection]['name']
            selected_text = self.info_font.render(f"Selected: {character_name}", True, (255, 255, 255))
            screen.blit(selected_text, (x + 10, y + 40))
        else:
            status_text = self.info_font.render("Selecting...", True, (200, 200, 200))
            current_char = self.characters[cursor_pos]['name']
            preview_text = self.info_font.render(f"Preview: {current_char}", True, (150, 150, 150))
            screen.blit(preview_text, (x + 10, y + 40))
        
        screen.blit(status_text, (x + 10, y + 65))
        
        # Character stats preview
        char_index = selection if selection is not None else cursor_pos
        character = self.characters[char_index]
        
        stats_title = self.info_font.render("Stats:", True, (255, 255, 255))
        screen.blit(stats_title, (x + 10, y + 95))
        
        # Mock stats based on character
        if character['name'] == 'Warrior':
            stats = ["Speed: ●●●○○", "Power: ●●●●○", "Defense: ●●●●○"]
        elif character['name'] == 'Speedster':
            stats = ["Speed: ●●●●●", "Power: ●●○○○", "Defense: ●●○○○"]
        else:  # Heavy
            stats = ["Speed: ●●○○○", "Power: ●●●●●", "Defense: ●●●●●"]
        
        for i, stat in enumerate(stats):
            stat_text = self.hint_font.render(stat, True, (200, 200, 200))
            screen.blit(stat_text, (x + 15, y + 115 + i * 18))
    
    def render_control_hints(self, screen):
        """
        Render control hints for both players
        """
        # Player 1 controls (left side)
        p1_hints = [
            "Player 1 Controls:",
            "WASD - Move cursor",
            "Q - Select/Confirm",
            "ESC - Back to menu"
        ]
        
        for i, hint in enumerate(p1_hints):
            color = self.player1_color if i == 0 else (180, 180, 180)
            text = self.hint_font.render(hint, True, color)
            screen.blit(text, (20, 20 + i * 22))
        
        # Player 2 controls (right side)
        p2_hints = [
            "Player 2 Controls:",
            "IJKL - Move cursor", 
            "U - Select/Confirm"
        ]
        
        for i, hint in enumerate(p2_hints):
            color = self.player2_color if i == 0 else (180, 180, 180)
            text = self.hint_font.render(hint, True, color)
            text_rect = text.get_rect()
            screen.blit(text, (1280 - text_rect.width - 20, 20 + i * 22))
    
    def render_transition_overlay(self, screen):
        """
        Render transition overlay when both players are ready
        """
        overlay = pygame.Surface((1280, 720))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Ready message
        ready_text = self.title_font.render("BOTH PLAYERS READY!", True, self.confirmed_color)
        ready_rect = ready_text.get_rect(center=(640, 300))
        screen.blit(ready_text, ready_rect)
        
        # Countdown or transition message
        transition_text = self.character_font.render("Proceeding to stage select...", True, (255, 255, 255))
        transition_rect = transition_text.get_rect(center=(640, 360))
        screen.blit(transition_text, transition_rect) 