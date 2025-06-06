"""
Physics Manager - Game Physics and Collision System
====================================================

Handles all physics simulation including movement, gravity, and collision detection.
Designed specifically for fighting game mechanics with precise frame-based physics.

Key Features:
- Frame-perfect collision detection
- Hitbox/hurtbox system for combat
- Platform collision with different types
- Gravity and air physics
- Knockback and hitstun mechanics

TODO:
- Implement precise collision detection algorithms
- Create hitbox/hurtbox management system
- Add frame-perfect physics for competitive play
- Implement knockback calculation system
- Add ledge detection for recovery mechanics
"""

import pygame
import numpy as np
from enum import Enum
import math

class CollisionType(Enum):
    """
    Types of collision interactions
    
    TODO: Expand for different collision behaviors
    """
    NONE = "none"
    PLATFORM_TOP = "platform_top"    # Land on top of platform
    PLATFORM_SIDE = "platform_side"  # Hit side of platform
    STAGE_BOUNDARY = "stage_boundary"
    HITBOX = "hitbox"                 # Attack collision
    HURTBOX = "hurtbox"              # Damage collision

class Hitbox:
    """
    Attack hitbox for combat system
    
    TODO: Implement complete hitbox system
    """
    
    def __init__(self, x, y, width, height, damage, knockback, owner):
        """
        Initialize a hitbox
        
        TODO:
        - Set position and size
        - Define damage and knockback properties
        - Set owner and frame data
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.damage = damage
        self.knockback = knockback
        self.owner = owner
        
        # Frame data
        self.startup_frames = 0
        self.active_frames = 0
        self.recovery_frames = 0
        self.current_frame = 0
        
        # Hit properties
        self.hit_targets = set()  # Characters already hit by this attack
        self.is_active = False
    
    def update(self):
        """
        Update hitbox state
        
        TODO:
        - Advance frame counter
        - Update active state based on frame data
        - Handle hit target tracking
        """
        pass
    
    def get_rect(self):
        """
        Get collision rectangle
        
        TODO:
        - Return pygame Rect for collision testing
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Hurtbox:
    """
    Vulnerability hitbox for taking damage
    
    TODO: Implement hurtbox system
    """
    
    def __init__(self, x, y, width, height, owner):
        """
        Initialize a hurtbox
        
        TODO:
        - Set position and size
        - Link to character owner
        - Set vulnerability properties
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.owner = owner
        self.is_vulnerable = True
    
    def get_rect(self):
        """
        Get collision rectangle
        
        TODO:
        - Return pygame Rect for collision testing
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

class PhysicsManager:
    """
    Main physics manager for the game
    
    TODO: Implement comprehensive physics system
    """
    
    def __init__(self):
        """
        Initialize the physics manager
        
        TODO:
        - Set up physics constants
        - Initialize collision detection systems
        - Set up spatial partitioning for performance
        """
        # Physics constants
        self.gravity = 0.8  # Pixels per frame squared
        self.air_friction = 0.02
        self.ground_friction = 0.15
        self.terminal_velocity = 20.0
        
        # Collision detection
        self.active_hitboxes = []
        self.character_hurtboxes = []
        
        # Performance optimization
        self.spatial_grid = {}  # TODO: Implement spatial hashing
    
    def update(self, delta_time, characters, stage):
        """
        Update all physics simulation
        
        TODO:
        - Update character physics
        - Handle collisions between characters and stage
        - Process hitbox vs hurtbox collisions
        - Apply gravity and friction
        """
        # Update character physics
        for character in characters:
            self.update_character_physics(character, delta_time, stage)
        
        # Check combat collisions
        self.check_combat_collisions(characters)
        
        # Update hitboxes and hurtboxes
        self.update_hitboxes()
    
    def update_character_physics(self, character, delta_time, stage):
        """
        Update physics for a single character
        
        TODO:
        - Apply gravity when in air
        - Handle platform collisions
        - Apply friction when appropriate
        - Check stage boundaries
        """
        # Apply gravity
        if not character.is_on_ground():
            character.velocity[1] += self.gravity
            
            # Apply air friction
            character.velocity[0] *= (1.0 - self.air_friction)
            
            # Cap terminal velocity
            if character.velocity[1] > self.terminal_velocity:
                character.velocity[1] = self.terminal_velocity
        else:
            # Apply ground friction
            character.velocity[0] *= (1.0 - self.ground_friction)
        
        # Update position based on velocity
        old_position = character.position.copy()
        character.position += character.velocity * delta_time
        
        # Check collisions with stage
        self.handle_stage_collision(character, stage, old_position)
    
    def handle_stage_collision(self, character, stage, old_position):
        """
        Handle collision between character and stage elements
        
        TODO:
        - Test collision with all platforms
        - Handle different platform types (solid, pass-through)
        - Implement ledge detection
        - Handle blast zone detection
        """
        character_rect = character.get_collision_rect()
        
        # For now, handle simple ground collision if stage is just bounds
        if hasattr(stage, 'platforms'):
            # Check collision with each platform
            for platform in stage.platforms:
                if self.check_platform_collision(character, platform, character_rect):
                    self.resolve_platform_collision(character, platform, old_position)
        
        # Simple ground collision for basic setup
        ground_level = 500  # Simple ground level
        if character.position[1] > ground_level:
            character.position[1] = ground_level
            if character.velocity[1] > 0:
                character.velocity[1] = 0
                character.on_ground = True
        
        # Check blast zones (simple bounds checking)
        if hasattr(stage, 'check_blast_zones'):
            if stage.check_blast_zones(character.position):
                # TODO: Handle character KO
                pass
        else:
            # Simple boundary checking
            if isinstance(stage, pygame.Rect):
                # Keep character within basic bounds
                if character.position[0] < 50:
                    character.position[0] = 50
                elif character.position[0] > stage.width - 50:
                    character.position[0] = stage.width - 50
    
    def check_platform_collision(self, character, platform, character_rect):
        """
        Check if character is colliding with a platform
        
        TODO:
        - Test rectangle collision
        - Handle different platform types
        - Consider character state (falling, rising, etc.)
        """
        platform_rect = platform.get_collision_rect()
        
        if character_rect.colliderect(platform_rect):
            # TODO: More sophisticated collision detection
            # - Check if character is falling onto platform
            # - Handle pass-through platforms properly
            # - Consider platform movement
            return True
        
        return False
    
    def resolve_platform_collision(self, character, platform, old_position):
        """
        Resolve collision between character and platform
        
        TODO:
        - Move character to valid position
        - Set appropriate flags (on_ground, etc.)
        - Handle platform-specific behaviors
        """
        # TODO: Implement proper collision resolution
        # - Separate character from platform
        # - Set ground state if landing on top
        # - Handle wall collisions
        pass
    
    def check_combat_collisions(self, characters):
        """
        Check collisions between attack hitboxes and character hurtboxes
        """
        for attacker in characters:
            for hitbox in attacker.active_hitboxes:
                for defender in characters:
                    if defender == attacker:
                        continue  # Can't hit yourself
                    
                    # Check collision between hitbox and defender's hurtbox
                    hitbox_rect = pygame.Rect(
                        hitbox['x'] - hitbox['width'] // 2,
                        hitbox['y'] - hitbox['height'] // 2,
                        hitbox['width'],
                        hitbox['height']
                    )
                    
                    defender_rect = defender.get_collision_rect()
                    
                    if hitbox_rect.colliderect(defender_rect):
                        self.apply_hit(hitbox, defender)
                        # Remove hitbox after hitting to prevent multi-hits
                        if hitbox in attacker.active_hitboxes:
                            attacker.active_hitboxes.remove(hitbox)
                        break
    
    def apply_hit(self, hitbox, target_character):
        """
        Apply hit effects to target character
        """
        # Calculate knockback direction based on attacker position and angle
        attacker = hitbox['owner']
        knockback_angle = hitbox['knockback_angle']
        knockback_force = hitbox['knockback']
        
        # Calculate knockback vector
        angle_rad = math.radians(knockback_angle)
        
        # Determine horizontal direction based on attacker position
        if attacker.position[0] < target_character.position[0]:
            # Attacker is on the left, knock right
            horizontal_direction = 1
        else:
            # Attacker is on the right, knock left
            horizontal_direction = -1
        
        # Calculate knockback components
        knockback_x = horizontal_direction * knockback_force * abs(math.cos(angle_rad))
        knockback_y = -knockback_force * math.sin(angle_rad)  # Negative because up is negative Y
        
        knockback_vector = np.array([knockback_x, knockback_y])
        
        # Apply damage and knockback
        target_character.take_damage(
            hitbox['damage'], 
            knockback_vector, 
            attacker
        )
        
        print(f"Hit! {hitbox['damage']} damage, knockback: ({knockback_x:.1f}, {knockback_y:.1f})")  # Debug
    
    def add_hitbox(self, hitbox):
        """
        Add a hitbox to the active list
        
        TODO:
        - Add to active hitboxes
        - Set up frame data
        - Initialize hit tracking
        """
        self.active_hitboxes.append(hitbox)
    
    def remove_hitbox(self, hitbox):
        """
        Remove a hitbox from the active list
        
        TODO:
        - Remove from active list
        - Clean up references
        """
        if hitbox in self.active_hitboxes:
            self.active_hitboxes.remove(hitbox)
    
    def update_hitboxes(self):
        """
        Update all active hitboxes
        
        TODO:
        - Update frame counters
        - Remove expired hitboxes
        - Update positions for moving attacks
        """
        for hitbox in self.active_hitboxes[:]:  # Copy list to allow removal
            hitbox.update()
            
            # Remove expired hitboxes
            if not hitbox.is_active:
                self.remove_hitbox(hitbox)
    
    def debug_render(self, screen, camera_offset):
        """
        Render physics debug information
        
        TODO:
        - Draw hitboxes and hurtboxes
        - Show collision information
        - Display physics vectors
        """
        # Draw active hitboxes (red)
        for hitbox in self.active_hitboxes:
            rect = hitbox.get_rect()
            rect.x -= camera_offset[0]
            rect.y -= camera_offset[1]
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)
        
        # TODO: Draw hurtboxes (blue)
        # TODO: Draw velocity vectors
        # TODO: Show collision normals 