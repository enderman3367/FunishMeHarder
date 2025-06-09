"""
Stage Select - Battle Arena Selection Interface
===============================================

Stage selection screen where Player 1 chooses the battle arena.
Features stage previews, descriptions, and selection controls.

Features:
- Stage preview images and descriptions
- Player 1 only controls (WASD + Space to select)
- Stage-specific information and hazard warnings
- Key hints for controls

Controls:
- Player 1: WASD to move cursor, Space to select
- ESC to go back to character select

Available Stages:
- Plains: Simple flat stage, good for beginners
- Battlefield: Platform stage with hazards and ledges
"""

import pygame
from src.core.state_manager import GameState, GameStateType
from enum import Enum

class StageSelectState(GameState):
    """
    Stage selection screen controlled by Player 1
    """
    
    def __init__(self, state_manager):
        """
        Initialize stage select screen
        """
        super().__init__(state_manager)
        
        # Available stages
        self.stages = [
            {
                "name": "Plains",
                "description": "A simple flat battlefield perfect for beginners",
                "features": ["Flat ground", "No hazards", "Easy recovery"],
                "difficulty": "Beginner",
                "type": "plains"
            },
            {
                "name": "Battlefield", 
                "description": "Classic platform stage with ledges and hazards",
                "features": ["Multiple platforms", "Ledge grabbing", "Fall-off zones"],
                "difficulty": "Intermediate",
                "type": "battlefield"
            }
        ]
        
        # Selection state
        self.current_selection = 0
        self.confirmed_selection = None
        self.transition_timer = 0.0
        
        # Visual properties
        self.stage_box_width = 400
        self.stage_box_height = 300
        self.stage_spacing = 100
        self.grid_start_x = 640 - (len(self.stages) * (self.stage_box_width + self.stage_spacing) - self.stage_spacing) // 2
        self.grid_y = 150
        
        # Colors
        self.selection_color = (255, 200, 0)  # Gold
        self.confirmed_color = (100, 255, 100)  # Green
        self.background_color = (20, 25, 40)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.stage_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 24)
        self.hint_font = pygame.font.Font(None, 20)
    
    def enter(self):
        """
        Called when entering stage select
        """
        self.current_selection = 0
        self.confirmed_selection = None
        self.transition_timer = 0.0
        print("Entering stage select screen")
    
    def exit(self):
        """
        Called when leaving stage select
        """
        print("Exiting stage select screen")
    
    def handle_event(self, event):
        """
        Handle stage select input events
        """
        if event.type == pygame.KEYDOWN:
            if self.confirmed_selection is None:
                # Player 1 controls only
                if event.key == pygame.K_f:  # Left
                    self.current_selection = (self.current_selection - 1) % len(self.stages)
                    self.play_navigate_sound()
                elif event.key == pygame.K_j:  # Right
                    self.current_selection = (self.current_selection + 1) % len(self.stages)
                    self.play_navigate_sound()
                elif event.key == pygame.K_SPACE:  # Confirm
                    self.confirmed_selection = self.current_selection
                    self.transition_timer = 1.0
                    self.play_confirm_sound()
                    print(f"Selected stage: {self.stages[self.confirmed_selection]['name']}")
            
            # Global controls
            if event.key == pygame.K_ESCAPE:
                # Go back to character select
                self.state_manager.change_state(GameStateType.CHARACTER_SELECT)
                return True
        
        return False
    
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
        Update stage select logic
        """
        if self.confirmed_selection is not None:
            self.transition_timer -= delta_time
            if self.transition_timer <= 0:
                # Store stage selection and proceed to the versus screen
                self.state_manager.selected_stage = self.stages[self.confirmed_selection]
                self.state_manager.change_state(GameStateType.VERSUS_SCREEN)
    
    def render(self, screen):
        """
        Render the stage select screen
        """
        screen.fill(self.background_color)
        
        # Render title
        title_text = self.title_font.render("SELECT STAGE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(640, 60))
        screen.blit(title_text, title_rect)
        
        # Render stage boxes
        for i, stage in enumerate(self.stages):
            self.render_stage_box(screen, stage, i)
        
        # Render selection cursor
        self.render_selection_cursor(screen)
        
        # Render stage details
        self.render_stage_details(screen)
        
        # Render control hints
        self.render_control_hints(screen)
        
        # Render transition overlay
        if self.confirmed_selection is not None:
            self.render_transition_overlay(screen)
    
    def render_stage_box(self, screen, stage, index):
        """
        Render individual stage selection box
        """
        box_x = self.grid_start_x + index * (self.stage_box_width + self.stage_spacing)
        box_y = self.grid_y
        
        # Stage box background
        box_rect = pygame.Rect(box_x, box_y, self.stage_box_width, self.stage_box_height)
        pygame.draw.rect(screen, (50, 55, 70), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        
        # Stage preview (large colored area representing the stage)
        preview_rect = pygame.Rect(box_x + 20, box_y + 20, 360, 180)
        stage_colors = {
            "Plains": (100, 200, 100),      # Green plains
            "Battlefield": (100, 100, 200)  # Blue battlefield
        }
        preview_color = stage_colors.get(stage["name"], (150, 150, 150))
        pygame.draw.rect(screen, preview_color, preview_rect)
        pygame.draw.rect(screen, (255, 255, 255), preview_rect, 2)
        
        # Draw stage-specific preview elements
        if stage["name"] == "Plains":
            # Simple flat ground
            ground_rect = pygame.Rect(box_x + 20, box_y + 170, 360, 30)
            pygame.draw.rect(screen, (80, 160, 80), ground_rect)
        elif stage["name"] == "Battlefield":
            # Multiple platforms
            main_platform = pygame.Rect(box_x + 100, box_y + 170, 200, 20)
            left_platform = pygame.Rect(box_x + 40, box_y + 120, 100, 15)
            right_platform = pygame.Rect(box_x + 260, box_y + 120, 100, 15)
            
            pygame.draw.rect(screen, (80, 80, 160), main_platform)
            pygame.draw.rect(screen, (60, 60, 140), left_platform)
            pygame.draw.rect(screen, (60, 60, 140), right_platform)
        
        # Stage name
        name_text = self.stage_font.render(stage["name"], True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(box_x + self.stage_box_width // 2, box_y + 220))
        screen.blit(name_text, name_rect)
        
        # Difficulty indicator
        difficulty_text = self.info_font.render(f"Difficulty: {stage['difficulty']}", True, (200, 200, 200))
        difficulty_rect = difficulty_text.get_rect(center=(box_x + self.stage_box_width // 2, box_y + 250))
        screen.blit(difficulty_text, difficulty_rect)
    
    def render_selection_cursor(self, screen):
        """
        Render selection cursor around current stage
        """
        if self.confirmed_selection is None:
            cursor_x = self.grid_start_x + self.current_selection * (self.stage_box_width + self.stage_spacing)
            cursor_rect = pygame.Rect(cursor_x - 5, self.grid_y - 5, self.stage_box_width + 10, self.stage_box_height + 10)
            pygame.draw.rect(screen, self.selection_color, cursor_rect, 5)
        else:
            # Show confirmed selection
            cursor_x = self.grid_start_x + self.confirmed_selection * (self.stage_box_width + self.stage_spacing)
            cursor_rect = pygame.Rect(cursor_x - 5, self.grid_y - 5, self.stage_box_width + 10, self.stage_box_height + 10)
            pygame.draw.rect(screen, self.confirmed_color, cursor_rect, 8)
    
    def render_stage_details(self, screen):
        """
        Render detailed information about the selected stage
        """
        selected_index = self.confirmed_selection if self.confirmed_selection is not None else self.current_selection
        stage = self.stages[selected_index]
        
        # Details panel
        panel_rect = pygame.Rect(100, 500, 1080, 150)
        pygame.draw.rect(screen, (40, 45, 60), panel_rect)
        pygame.draw.rect(screen, (255, 255, 255), panel_rect, 2)
        
        # Stage name and description
        name_text = self.stage_font.render(stage["name"], True, (255, 255, 255))
        screen.blit(name_text, (120, 520))
        
        desc_text = self.info_font.render(stage["description"], True, (200, 200, 200))
        screen.blit(desc_text, (120, 550))
        
        # Features list
        features_title = self.info_font.render("Features:", True, (255, 255, 255))
        screen.blit(features_title, (120, 580))
        
        for i, feature in enumerate(stage["features"]):
            feature_text = self.hint_font.render(f"• {feature}", True, (180, 180, 180))
            screen.blit(feature_text, (130, 605 + i * 18))
        
        # Show selected characters
        if hasattr(self.state_manager, 'selected_characters'):
            chars = self.state_manager.selected_characters
            char_info = self.info_font.render(
                f"P1: {chars['player1']['name']} vs P2: {chars['player2']['name']}", 
                True, (150, 150, 255)
            )
            char_rect = char_info.get_rect()
            screen.blit(char_info, (1280 - char_rect.width - 120, 520))
    
    def render_control_hints(self, screen):
        """
        Render control hints
        """
        hints = [
            "Player 1 Controls:",
            "F/J - Select stage",
            "Space - Confirm",
            "ESC - Back to character select"
        ]
        
        for i, hint in enumerate(hints):
            color = self.selection_color if i == 0 else (180, 180, 180)
            text = self.hint_font.render(hint, True, color)
            screen.blit(text, (20, 20 + i * 22))
    
    def render_transition_overlay(self, screen):
        """
        Render transition overlay when stage is confirmed
        """
        overlay = pygame.Surface((1280, 720))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Confirmation message
        stage_name = self.stages[self.confirmed_selection]['name']
        confirm_text = self.title_font.render(f"STAGE SELECTED: {stage_name.upper()}", True, self.confirmed_color)
        confirm_rect = confirm_text.get_rect(center=(640, 300))
        screen.blit(confirm_text, confirm_rect)
        
        # Starting message
        start_text = self.stage_font.render("Starting battle...", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(640, 360))
        screen.blit(start_text, start_rect) 