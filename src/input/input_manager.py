"""
Input Manager - Player Input Handling System
=============================================

Handles all player input including keyboard controls for both players.
Supports configurable key mappings and input buffering for fighting game mechanics.

Player Controls (Smash-style):
- Player 1: WASD movement + Q for attack (direction + Q = different attacks)
- Player 2: IJKL movement + U for attack (direction + U = different attacks)

Attack Types:
- No direction + Attack = Neutral attack
- Side + Attack = Side attack
- Up + Attack = Up attack  
- Down + Attack = Down attack

Key Features:
- Input buffering for frame-perfect combo execution
- "Just pressed" and "just released" detection
- Smooth input handling for responsive movement
- Directional attack detection like Smash Bros

TODO:
- Implement input buffering for combo execution
- Add input recording for replay system
- Handle simultaneous inputs properly
- Add configurable key bindings
- Implement input lag compensation
- Add gamepad support for future expansion

Fighting Game Input Concepts:
- Input buffering: Allow inputs to be registered slightly before they can be executed
- Input priority: Handle conflicting inputs (e.g., left+right pressed simultaneously)
- Special move detection: Quarter circle, half circle, and charge motions
"""

import pygame
from enum import Enum

class InputAction(Enum):
    """
    All possible input actions in the game
    """
    # Movement
    MOVE_LEFT = "left"
    MOVE_RIGHT = "right"
    JUMP = "up"
    CROUCH = "down"
    
    # Attacks (Smash-style)
    ATTACK = "attack"
    
    # System actions
    PAUSE = "pause"
    GRAB = "grab"

class PlayerInput:
    """
    Represents the current input state for a single player with buffering
    """
    
    def __init__(self):
        """
        Initialize player input state with buffering system
        """
        # Current frame input states
        self.current_inputs = {}
        self.previous_inputs = {}
        
        # Initialize all inputs to False
        for action in ['left', 'right', 'up', 'down', 'attack', 'grab']:
            self.current_inputs[action] = False
            self.previous_inputs[action] = False
        
        # Input buffer for frame-perfect inputs (stores last 6 frames)
        self.input_buffer = []
        self.buffer_size = 6
        
        # Direction input for analog-style movement
        self.horizontal_axis = 0.0  # -1.0 to 1.0
        self.vertical_axis = 0.0    # -1.0 to 1.0
    
    def update(self, key_states, key_mapping):
        """
        Update input state based on current key presses
        """
        # Store previous frame inputs
        self.previous_inputs = self.current_inputs.copy()
        
        # Update current inputs based on key states
        self.current_inputs['left'] = key_states[key_mapping['left']]
        self.current_inputs['right'] = key_states[key_mapping['right']]
        self.current_inputs['up'] = key_states[key_mapping['up']]
        self.current_inputs['down'] = key_states[key_mapping['down']]
        self.current_inputs['attack'] = key_states[key_mapping['attack']]
        self.current_inputs['grab'] = key_states[key_mapping['grab']]
        
        # Update directional axes for smooth movement
        self.horizontal_axis = 0.0
        if self.current_inputs['left']:
            self.horizontal_axis -= 1.0
        if self.current_inputs['right']:
            self.horizontal_axis += 1.0
        
        self.vertical_axis = 0.0
        if self.current_inputs['up']:
            self.vertical_axis -= 1.0
        if self.current_inputs['down']:
            self.vertical_axis += 1.0
        
        # Add current frame to input buffer
        self.input_buffer.append(self.current_inputs.copy())
        if len(self.input_buffer) > self.buffer_size:
            self.input_buffer.pop(0)
    
    def is_pressed(self, action):
        """
        Check if an action is currently pressed
        """
        return self.current_inputs.get(action, False)
    
    def was_just_pressed(self, action):
        """
        Check if an action was pressed this frame (rising edge)
        """
        current = self.current_inputs.get(action, False)
        previous = self.previous_inputs.get(action, False)
        return current and not previous
    
    def was_just_released(self, action):
        """
        Check if an action was released this frame (falling edge)
        """
        current = self.current_inputs.get(action, False)
        previous = self.previous_inputs.get(action, False)
        return not current and previous
    
    def get_attack_direction(self):
        """
        Get the direction for attack input (like Smash Bros)
        Returns: 'neutral', 'side', 'up', 'down'
        """
        if self.is_pressed('up'):
            return 'up'
        elif self.is_pressed('down'):
            return 'down'
        elif self.is_pressed('left') or self.is_pressed('right'):
            return 'side'
        else:
            return 'neutral'
    
    def was_pressed_in_buffer(self, action, frames_back=None):
        """
        Check if an action was pressed within the input buffer window
        """
        if frames_back is None:
            frames_back = self.buffer_size
        
        frames_to_check = min(frames_back, len(self.input_buffer))
        for i in range(frames_to_check):
            frame_inputs = self.input_buffer[-(i+1)]
            if frame_inputs.get(action, False):
                return True
        return False
    
    def get_horizontal_axis(self):
        """
        Get horizontal input as a float (-1.0 to 1.0)
        """
        return self.horizontal_axis
    
    def get_vertical_axis(self):
        """
        Get vertical input as a float (-1.0 to 1.0)
        """
        return self.vertical_axis

class InputManager:
    """
    Manages input for all players and global game inputs
    """
    
    def __init__(self):
        """
        Initialize the input manager with Smash-style key mappings
        """
        # Smash-style controls for Player 1
        self.player1_keys = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'up': pygame.K_w,
            'down': pygame.K_s,
            'attack': pygame.K_q,      # One attack button
            'grab': pygame.K_e
        }
        
        # Smash-style controls for Player 2
        self.player2_keys = {
            'left': pygame.K_j,
            'right': pygame.K_l,
            'up': pygame.K_i,
            'down': pygame.K_k,
            'attack': pygame.K_u,      # One attack button
            'grab': pygame.K_o
        }
        
        # Global keys
        self.global_keys = {
            'pause': pygame.K_ESCAPE
        }
        
        # Player input objects
        self.player1_input = PlayerInput()
        self.player2_input = PlayerInput()
        
        # Current keyboard state
        self.keys_pressed = pygame.key.get_pressed()
        
        # Global input states
        self.pause_pressed = False
        self.pause_just_pressed = False
    
    def handle_event(self, event):
        """
        Handle pygame input events for immediate response actions
        """
        if event.type == pygame.KEYDOWN:
            # Handle global pause
            if event.key == self.global_keys['pause']:
                self.pause_just_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == self.global_keys['pause']:
                self.pause_just_pressed = False
    
    def update(self):
        """
        Update input system each frame
        """
        # Get current keyboard state
        self.keys_pressed = pygame.key.get_pressed()
        
        # Update global inputs
        self.pause_pressed = self.keys_pressed[self.global_keys['pause']]
        
        # Update player inputs
        self.player1_input.update(self.keys_pressed, self.player1_keys)
        self.player2_input.update(self.keys_pressed, self.player2_keys)
    
    def get_player_input(self, player_id):
        """
        Get input state for a specific player (1 or 2)
        """
        if player_id == 1:
            return self.player1_input
        elif player_id == 2:
            return self.player2_input
        else:
            raise ValueError(f"Invalid player_id: {player_id}. Must be 1 or 2.")
    
    def is_pause_pressed(self):
        """
        Check if pause is currently pressed
        """
        return self.pause_pressed
    
    def was_pause_just_pressed(self):
        """
        Check if pause was just pressed this frame
        """
        return self.pause_just_pressed
    
    def configure_keys(self, player_id, key_mapping):
        """
        Configure key mappings for a player
        """
        if player_id == 1:
            self.player1_keys.update(key_mapping)
        elif player_id == 2:
            self.player2_keys.update(key_mapping)
        else:
            raise ValueError(f"Invalid player_id: {player_id}. Must be 1 or 2.")
    
    def detect_special_move(self, player_id, move_pattern):
        """
        Detect special move input patterns (quarter circles, etc.)
        
        TODO: Implement complex motion detection
        - Quarter circle forward (236): Down, Down-Forward, Forward + Attack
        - Quarter circle back (214): Down, Down-Back, Back + Attack
        - Dragon punch (623): Forward, Down, Down-Forward + Attack
        - Half circle (63214 or 41236): complex motions
        """
        player_input = self.get_player_input(player_id)
        
        # For now, return simple detection
        # This would be expanded with complex motion detection
        if move_pattern == "quarter_circle_forward":
            # Simplified: just check if down and forward were pressed recently
            return (player_input.was_pressed_in_buffer('down', 4) and 
                   player_input.was_pressed_in_buffer('right', 2))
        elif move_pattern == "quarter_circle_back":
            return (player_input.was_pressed_in_buffer('down', 4) and 
                   player_input.was_pressed_in_buffer('left', 2))
        
        return False
    
    def get_input_display_string(self, player_id):
        """
        Get a string representation of current inputs (for debugging/training mode)
        """
        player_input = self.get_player_input(player_id)
        display = []
        
        if player_input.is_pressed('left'):
            display.append('←')
        if player_input.is_pressed('right'):
            display.append('→')
        if player_input.is_pressed('up'):
            display.append('↑')
        if player_input.is_pressed('down'):
            display.append('↓')
        
        if player_input.is_pressed('attack'):
            display.append('A')
        if player_input.is_pressed('grab'):
            display.append('G')
        
        return ''.join(display) if display else '·'
    
    def reset_player_input(self, player_id):
        """
        Reset a player's input state (useful for cutscenes, etc.)
        """
        if player_id == 1:
            self.player1_input = PlayerInput()
        elif player_id == 2:
            self.player2_input = PlayerInput()
    
    def get_all_current_inputs(self):
        """
        Get all current input states for both players (useful for replay system)
        """
        return {
            'player1': self.player1_input.current_inputs.copy(),
            'player2': self.player2_input.current_inputs.copy(),
            'global': {
                'pause': self.pause_pressed
            }
        } 