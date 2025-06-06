"""
Base Character - Foundation for all fighters
=============================================

This module contains the base Character class that all fighters inherit from.
Defines common properties, methods, and behaviors shared by all characters.

TODO:
- Implement physics-based movement with smooth animations
- Add hitbox/hurtbox system for attacks and collisions
- Implement state machine for character actions (idle, walking, attacking, etc.)
- Add health and damage system
- Create animation system with sprite sheets
- Implement special move system with input requirements

Animation States to implement:
- Idle, Walking, Running, Jumping, Falling
- Light Attack, Heavy Attack, Special Attacks
- Hit Stun, Block Stun, Knockdown
- Grabbing, Being Grabbed
"""

import pygame
import numpy as np
from enum import Enum

class CharacterState(Enum):
    """
    All possible character states for animation and behavior
    
    TODO: Expand as needed for more complex actions
    """
    IDLE = "idle"
    WALKING = "walking"
    RUNNING = "running"
    JUMPING = "jumping"
    FALLING = "falling"
    LANDING = "landing"
    CROUCHING = "crouching"
    
    # Attack states
    LIGHT_ATTACK = "light_attack"
    HEAVY_ATTACK = "heavy_attack"
    SIDE_SPECIAL = "side_special"
    UP_SPECIAL = "up_special"
    DOWN_SPECIAL = "down_special"
    NEUTRAL_SPECIAL = "neutral_special"
    
    # Defensive states
    BLOCKING = "blocking"
    HIT_STUN = "hit_stun"
    KNOCKDOWN = "knockdown"
    
    # Grab system
    GRABBING = "grabbing"
    GRABBED = "grabbed"

class Character:
    """
    Base class for all playable characters
    
    TODO: Implement core character functionality that all fighters share
    """
    
    def __init__(self, x, y, player_id):
        """
        Initialize a character
        
        TODO:
        - Set up position, physics, and stats
        - Initialize animation system
        - Set up hitbox/hurtbox system
        - Load character-specific data
        """
        # Position and physics
        self.position = np.array([float(x), float(y)])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.facing_right = True if player_id == 1 else False
        
        # Character stats (TODO: Load from character data files)
        self.max_health = 100
        self.current_health = self.max_health
        self.weight = 1.0  # Affects knockback
        self.walk_speed = 3.0
        self.run_speed = 6.0
        self.jump_strength = 15.0
        self.air_speed = 4.0
        
        # State management
        self.current_state = CharacterState.IDLE
        self.state_timer = 0.0
        self.can_act = True
        
        # Combat properties
        self.is_attacking = False
        self.is_blocking = False
        self.hit_stun_timer = 0.0
        self.invincibility_timer = 0.0
        
        # Animation properties (TODO: Implement sprite animation system)
        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0.0
        
        # Player identification
        self.player_id = player_id
    
    def update(self, delta_time, player_input, stage_bounds):
        """
        Update character logic each frame
        
        TODO:
        - Update physics and movement
        - Process player input
        - Update animations
        - Handle state transitions
        - Update timers (hit stun, invincibility, etc.)
        - Apply gravity and collision detection
        """
        pass
    
    def handle_input(self, player_input):
        """
        Process player input and trigger appropriate actions
        
        TODO:
        - Check if character can act (not in hit stun, etc.)
        - Handle movement inputs (left, right, jump, crouch)
        - Handle attack inputs (light, heavy, specials)
        - Handle defensive inputs (block, grab)
        - Queue actions if character is busy
        """
        pass
    
    def update_physics(self, delta_time, stage_bounds):
        """
        Update character physics and collision with stage
        
        TODO:
        - Apply gravity when in air
        - Update velocity based on acceleration
        - Update position based on velocity
        - Handle collision with stage boundaries
        - Handle collision with platforms
        - Apply friction when on ground
        """
        pass
    
    def change_state(self, new_state):
        """
        Change character state with proper transitions
        
        TODO:
        - Validate state transition is allowed
        - Clean up current state
        - Initialize new state
        - Reset state timer
        - Update animation
        """
        pass
    
    def perform_attack(self, attack_type):
        """
        Execute an attack action
        
        TODO:
        - Check if attack is allowed in current state
        - Set attack state and animation
        - Create hitboxes for the attack
        - Set attack properties (damage, knockback, etc.)
        - Handle attack startup, active, and recovery frames
        """
        pass
    
    def take_damage(self, damage, knockback_vector, attacker):
        """
        Handle taking damage from an attack
        
        TODO:
        - Reduce health by damage amount
        - Apply knockback based on weight and damage
        - Enter hit stun state
        - Play damage animation and sound effects
        - Check for KO condition
        """
        pass
    
    def render(self, screen, camera_offset):
        """
        Render the character to the screen
        
        TODO:
        - Draw character sprite with current animation frame
        - Handle sprite flipping based on facing direction
        - Draw hitboxes/hurtboxes in debug mode
        - Draw health bar and damage indicators
        - Apply screen shake or other visual effects
        """
        pass
    
    def get_hitboxes(self):
        """
        Get current attack hitboxes
        
        TODO:
        - Return list of active hitboxes for current attack
        - Include position, size, damage, and knockback data
        - Handle different hitbox types (damage, grab, etc.)
        """
        pass
    
    def get_hurtboxes(self):
        """
        Get current vulnerability hurtboxes
        
        TODO:
        - Return list of hurtboxes that can be hit
        - Handle invincibility frames
        - Different hurtbox types (body, head, limbs)
        """
        pass
    
    def reset_to_spawn(self, spawn_x, spawn_y):
        """
        Reset character to spawn position (after KO or round start)
        
        TODO:
        - Reset position to spawn point
        - Reset health to maximum
        - Reset all timers and states
        - Clear any status effects
        """
        pass 