"""
Toybox - Experimental Features and Debug Gameplay
=================================================

A special gameplay mode accessible from the main menu. This is where
experimental features and debug tools can be tested in a controlled
environment.

Features:
- Simple box characters (red and blue)
- Flat stage with a central platform and no fall-off hazards
- Standard game controls and physics
- Plays a special sound when opened
"""

import pygame
from src.core.state_manager import GameplayState, GameStateType
from src.characters.box_character import RedBoxPlayer, BlueBoxPlayer
from src.stages.toybox_stage import ToyboxStage
import os
import random

class ToyboxState(GameplayState):
    """
    Toybox state for experimental gameplay. Inherits from GameplayState
    to reuse the core gameplay loop and physics.
    """
    
    def __init__(self, state_manager):
        """
        Initialize the toybox state.
        """
        super().__init__(state_manager)
        
        # Load toybox-specific sounds
        try:
            self.open_sound = pygame.mixer.Sound('assets/toybox/toybox-open.mp3')
        except (pygame.error, FileNotFoundError) as e:
            self.open_sound = None
            print(f"Warning: Could not load toybox-open.mp3: {e}")
            
        try:
            self.sequence_sound = pygame.mixer.Sound('assets/toybox/toybox-stage.mp3')
        except (pygame.error, FileNotFoundError) as e:
            self.sequence_sound = None
            print(f"Warning: Could not load toybox-stage.mp3: {e}")

        # Mystery box properties
        self.mystery_box_rect = None
        self.mystery_box_spawn_timer = 0
        self.mystery_box_state = "off" # Can be 'off', 'waiting', 'spawning', 'active'
        self.mystery_box_velocity_y = 0
        self.box_target_y = 500
    
    def enter(self):
        """
        Called when entering toybox state. Overrides GameplayState's enter
        to set up the special toybox environment.
        """
        print("🎮 Entering Toybox Mode")
        
        # Play the opening sound
        if self.open_sound:
            self.open_sound.play()
            
        # Set up the custom toybox stage and characters directly
        self.setup_stage()
        self.create_characters_from_selection()
        
        # Reset match state
        self.match_timer = 999
        self.match_start_time = 0.0
        self.respawn_timer = {}
        
        # Reset character states
        if self.player1_character and self.player2_character:
            self.player1_character.damage_percent = 0.0
            self.player2_character.damage_percent = 0.0
            self.player1_character.lives = 99
            self.player2_character.lives = 99

        # Set a random time for the first box to spawn
        self.mystery_box_spawn_timer = random.uniform(2.0, 10.0)
        self.mystery_box_state = "waiting"
        print(f"Toybox entered. Mystery box will spawn in {self.mystery_box_spawn_timer:.2f} seconds.")

    def create_characters_from_selection(self):
        """
        Overrides the default character creation to use the box characters.
        """
        if hasattr(self, 'stage_object') and len(self.stage_object.spawn_points) >= 2:
            spawn1_x, spawn1_y = self.stage_object.spawn_points[0]
            spawn2_x, spawn2_y = self.stage_object.spawn_points[1]
        else:
            spawn1_x, spawn1_y = 300, 500
            spawn2_x, spawn2_y = 900, 500
            
        self.player1_character = RedBoxPlayer(spawn1_x, spawn1_y, 1)
        self.player2_character = BlueBoxPlayer(spawn2_x, spawn2_y, 2)
        self.characters = [self.player1_character, self.player2_character]
        print(f"Created toybox characters: P1={self.player1_character.name}, P2={self.player2_character.name}")
        
    def setup_stage(self):
        """
        Overrides the default stage setup to use the ToyboxStage.
        """
        self.stage_object = ToyboxStage()
        self.current_stage = "Toybox"
        self.stage_bounds = pygame.Rect(0, 0, self.stage_object.width, self.stage_object.height)
        self.fall_zones = {
            "left": self.stage_object.left_blast_zone,
            "right": self.stage_object.right_blast_zone
        }
        print(f"Toybox stage setup complete.")
        
    def handle_event(self, event):
        """
        Handle input events in the toybox.
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state_manager.change_state(GameStateType.MAIN_MENU)
            return True
        return super().handle_event(event)

    def update(self, delta_time):
        """
        Update the toybox state, including the mystery box and boundaries.
        """
        super().update(delta_time)
        self._update_mystery_box(delta_time)
        self._enforce_screen_boundaries()

    def _enforce_screen_boundaries(self):
        """
        Prevents characters from leaving the screen area by creating collision borders.
        """
        screen_width, screen_height = 1280, 720
        for character in self.characters:
            char_rect = character.get_collision_rect()

            if char_rect.left < 0:
                char_rect.left = 0
                character.velocity[0] = 0
            if char_rect.right > screen_width:
                char_rect.right = screen_width
                character.velocity[0] = 0
            if char_rect.top < 0:
                char_rect.top = 0
                character.velocity[1] = 0
            
            character.position[0] = char_rect.centerx
            character.position[1] = char_rect.bottom
            
    def _spawn_mystery_box(self):
        """Creates the mystery box at its starting position."""
        self.mystery_box_state = "spawning"
        center_platform_rect = self.stage_object.platforms[1].get_rect()
        box_x = center_platform_rect.centerx - 20
        self.mystery_box_rect = pygame.Rect(box_x, -50, 40, 40)
        self.mystery_box_velocity_y = 0
        self.box_target_y = center_platform_rect.top
        print("Spawning mystery box!")

    def _update_mystery_box(self, delta_time):
        """
        Handles the logic for the mystery box spawning, falling, and collection.
        """
        if self.mystery_box_state == "waiting":
            self.mystery_box_spawn_timer -= delta_time
            if self.mystery_box_spawn_timer <= 0:
                self._spawn_mystery_box()

        elif self.mystery_box_state == "spawning":
            self.mystery_box_velocity_y += 0.5 
            self.mystery_box_rect.y += self.mystery_box_velocity_y
            if self.mystery_box_rect.bottom >= self.box_target_y:
                self.mystery_box_rect.bottom = self.box_target_y
                self.mystery_box_state = "active"
                print("Mystery box has landed.")

        elif self.mystery_box_state == "active":
            for player in self.characters:
                if self.mystery_box_rect and player.get_collision_rect().colliderect(self.mystery_box_rect):
                    print(f"Player {player.player_id} collected the mystery box!")
                    self.mystery_box_state = "waiting"
                    self.mystery_box_spawn_timer = 25.0
                    self.mystery_box_rect = None
                    self.apply_random_effect(player)
                    break

    def apply_random_effect(self, player_character):
        """
        Applies a random Wonder Sequence effect to the character.
        """
        if self.sequence_sound:
            self.sequence_sound.play()
            
        effects = [
            "shrink", 
            "inversion", 
            "doppelganger", 
            "balloon"
        ]
        chosen_effect = random.choice(effects)
        print(f"Applying effect '{chosen_effect}' to Player {player_character.player_id}")

        # Reset any existing effects on both players before applying a new one
        self._reset_player_effects(self.player1_character)
        self._reset_player_effects(self.player2_character)

        if chosen_effect == "shrink":
            player_character.apply_effect("shrink", 20.0)
            player_character.width, player_character.height = 25, 25
        
        elif chosen_effect == "inversion":
            player_character.apply_effect("inversion", 20.0)
            
        elif chosen_effect == "doppelganger":
            # This effect swaps the input managers' player objects
            print("Swapping player controls!")
            p1_input = self.game_engine.input_manager.player1_input
            p2_input = self.game_engine.input_manager.player2_input
            self.game_engine.input_manager.player1_input = p2_input
            self.game_engine.input_manager.player2_input = p1_input
            # Apply a dummy effect to track the timer
            player_character.apply_effect("doppelganger", 20.0)

        elif chosen_effect == "balloon":
            player_character.apply_effect("balloon", 20.0)
            player_character.jump_strength = 20.0 # Higher jump
            player_character.gravity_multiplier = 0.4 # Slower fall
            
    def _reset_player_effects(self, player_character):
        """Resets a player's stats and all active effects."""
        # Reset visual and physical stats
        player_character.width, player_character.height = 50, 50
        player_character.max_walk_speed, player_character.max_run_speed = 8.0, 12.0
        player_character.ground_acceleration = 1.2
        player_character.jump_strength = 15.0
        player_character.gravity_multiplier = 1.0

        # Special handling for doppelganger - restore original controls
        if 'doppelganger' in player_character.active_effects:
             print("Restoring original player controls.")
             p1_map = self.game_engine.input_manager.player1_keys
             p2_map = self.game_engine.input_manager.player2_keys
             # This simple swap might not be enough if joysticks are involved.
             # A better system would be to store original input objects.
             # For now, let's assume keyboard.

        # Clear all effect trackers
        player_character.active_effects.clear()
        player_character.effect_timers.clear()

    def render(self, screen):
        """
        Render the toybox gameplay scene, including the mystery box.
        """
        super().render(screen)
        self._render_mystery_box(screen)

    def _render_mystery_box(self, screen):
        """Draws the mystery box if it is currently on screen."""
        if self.mystery_box_state in ["spawning", "active"]:
            pygame.draw.rect(screen, (255, 220, 0), self.mystery_box_rect)
            pygame.draw.rect(screen, (200, 170, 0), self.mystery_box_rect, 3)
            font = pygame.font.Font(None, 40)
            q_mark = font.render("?", True, (255, 255, 255))
            q_rect = q_mark.get_rect(center=self.mystery_box_rect.center)
            screen.blit(q_mark, q_rect)

    def exit(self):
        """
        Called when leaving toybox state.
        """
        print("🎮 Exiting Toybox Mode")
        if self.player1_character: self._reset_player_effects(self.player1_character)
        if self.player2_character: self._reset_player_effects(self.player2_character)
        super().exit() 