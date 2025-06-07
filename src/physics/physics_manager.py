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
        Update physics for a single character with stage-specific modifications
        
        This method now integrates with stage-specific gravity and physics systems
        to create unique gameplay experiences on different stages.
        
        Physics Integration:
        ===================
        - Checks if stage has custom gravity methods
        - Falls back to standard physics if stage doesn't override
        - Maintains consistent base physics while allowing stage customization
        - Ensures competitive balance across all stages
        
        Args:
            character: Character object to update physics for
            delta_time (float): Time in seconds since last frame
            stage: Stage object that may have custom physics methods
        """
        
        print(f"🔧 Physics Update P{character.player_id}: dt={delta_time:.3f}, pos=({character.position[0]:.1f}, {character.position[1]:.1f}), vel=({character.velocity[0]:.2f}, {character.velocity[1]:.2f}), on_ground={character.on_ground}")
        
        # === STAGE-SPECIFIC GRAVITY APPLICATION ===
        # Check if the stage has custom gravity mechanics
        if hasattr(stage, 'apply_stage_gravity') and callable(stage.apply_stage_gravity):
            print(f"🌍 Applying {stage.name} stage gravity to P{character.player_id}")
            # Use stage-specific gravity system (Battlefield, Plains, etc.)
            stage.apply_stage_gravity(character, delta_time)
        else:
            print(f"⚠️ Using fallback physics for P{character.player_id} (no stage gravity)")
            # === FALLBACK TO STANDARD PHYSICS ===
            # Apply standard gravity when stage doesn't have custom physics
            if not character.is_on_ground():
                print(f"🌊 Applying standard gravity to P{character.player_id}: {self.gravity}")
                # Standard gravity application
                character.velocity[1] += self.gravity
                
                # Standard air friction
                character.velocity[0] *= (1.0 - self.air_friction)
                
                # Standard terminal velocity cap
                if character.velocity[1] > self.terminal_velocity:
                    character.velocity[1] = self.terminal_velocity
            else:
                print(f"🏃 Applying ground friction to P{character.player_id}: {self.ground_friction}")
                # Standard ground friction
                character.velocity[0] *= (1.0 - self.ground_friction)
        
        # === UNIVERSAL POSITION UPDATE ===
        # Update position based on velocity (works for all stages)
        # Using 60fps normalization for consistent physics regardless of framerate
        old_position = character.position.copy()
        
        # Calculate movement with 60fps normalization
        x_movement = character.velocity[0] * 60.0 * delta_time
        y_movement = character.velocity[1] * 60.0 * delta_time
        
        new_x = character.position[0] + x_movement
        new_y = character.position[1] + y_movement
        
        print(f"📍 Position update P{character.player_id}: ({character.position[0]:.1f}, {character.position[1]:.1f}) -> ({new_x:.1f}, {new_y:.1f})")
        print(f"🚀 Movement calculation: vel_x({character.velocity[0]:.2f}) * 60 * dt({delta_time:.4f}) = {x_movement:.4f}")
        print(f"🚀 Movement calculation: vel_y({character.velocity[1]:.2f}) * 60 * dt({delta_time:.4f}) = {y_movement:.4f}")
        
        character.position[0] = new_x
        character.position[1] = new_y
        
        # === STAGE COLLISION HANDLING ===
        # Handle collisions with stage elements
        print(f"🎯 Checking stage collision for P{character.player_id}")
        self.handle_stage_collision(character, stage, old_position)
    
    def handle_stage_collision(self, character, stage, old_position):
        """
        Handle collision between character and stage elements with proper blast zones
        
        This method now properly handles:
        - Platform collision detection
        - Stage-specific platform layouts
        - Blast zone checking for KOs
        - No artificial boundaries that prevent falling off-stage
        
        Args:
            character: Character object to check collisions for
            stage: Stage object (either Stage class or pygame.Rect for legacy)
            old_position: Character's previous position before movement
        """
        
        # === HANDLE MODERN STAGE OBJECTS ===
        # New stage system with proper platform and blast zone support
        if hasattr(stage, 'platforms') and hasattr(stage, 'name'):
            # This is a proper Stage object (Battlefield, Plains, etc.)
            self.handle_modern_stage_collision(character, stage)
            
        # === HANDLE LEGACY STAGE SYSTEM ===
        # For backwards compatibility with old pygame.Rect stages
        elif isinstance(stage, pygame.Rect):
            self.handle_legacy_stage_collision(character, stage)
        
        # === BLAST ZONE CHECKING ===
        # Check if character has gone beyond the stage boundaries and should be KO'd
        self.check_blast_zone_ko(character, stage)
    
    def handle_modern_stage_collision(self, character, stage):
        """
        Handle collision with modern Stage objects (Battlefield, Plains, etc.)
        
        Args:
            character: Character to check collisions for
            stage: Modern Stage object with platforms
        """
        print(f"🏗️ Modern stage collision check for P{character.player_id} on {stage.name}")
        character_rect = character.get_collision_rect()
        character_on_platform = False
        
        print(f"🎪 Character P{character.player_id} rect: {character_rect}, checking {len(stage.platforms)} platforms")
        
        # Check collision with each platform
        for i, platform in enumerate(stage.platforms):
            platform_id = getattr(platform, 'platform_id', f'platform_{i}')
            print(f"🧱 Checking platform {platform_id}: pos=({platform.x}, {platform.y}), size=({platform.width}, {platform.height})")
            
            if self.check_platform_landing(character, platform):
                print(f"✅ P{character.player_id} landed on platform {platform_id}")
                character_on_platform = True
                break
            else:
                print(f"❌ P{character.player_id} not on platform {platform_id}")
        
        # CRITICAL FIX: Actually update the character's ground state
        if not character_on_platform:
            print(f"🌫️ P{character.player_id} not on any platform - setting to airborne")
            character.on_ground = False
            # Make sure the character knows they're falling
            if hasattr(character, 'change_state') and character.velocity[1] >= 0:
                from src.characters.base_character import CharacterState
                character.change_state(CharacterState.FALLING)
        else:
            print(f"🏠 P{character.player_id} is on a platform - staying grounded")
            character.on_ground = True
    
    def handle_legacy_stage_collision(self, character, stage):
        """
        Handle collision with legacy pygame.Rect stages
        
        Args:
            character: Character to check collisions for  
            stage: pygame.Rect representing the stage
        """
        # Determine stage type by dimensions (this is hacky but works for now)
        is_battlefield = stage.width == 1080  # Battlefield has smaller bounds
        
        if is_battlefield:
            self.handle_battlefield_platforms(character)
        else:
            # Plains - only has ground collision, no artificial boundaries
            self.handle_plains_ground_collision(character)
    
    def check_platform_landing(self, character, platform):
        """
        Check if character is landing on or standing on a platform
        
        Args:
            character: Character object
            platform: Platform object to check collision with
            
        Returns:
            bool: True if character is on this platform
        """
        # Get character position and bounds
        char_bottom = character.position[1]
        char_left = character.position[0] - character.width / 2
        char_right = character.position[0] + character.width / 2
        
        platform_id = getattr(platform, 'platform_id', 'unknown')
        
        print(f"🔍 Platform collision check P{character.player_id} vs {platform_id}:")
        print(f"   Character: bottom={char_bottom:.1f}, left={char_left:.1f}, right={char_right:.1f}")
        print(f"   Platform: top={platform.y}, left={platform.x}, right={platform.x + platform.width}")
        print(f"   Velocity: ({character.velocity[0]:.2f}, {character.velocity[1]:.2f})")
        
        # Check if character is at platform level and overlapping horizontally
        vertical_collision = (char_bottom >= platform.y - 5 and char_bottom <= platform.y + 10)
        horizontal_collision = (char_right > platform.x + 5 and char_left < platform.x + platform.width - 5)
        
        print(f"   Vertical collision (bottom {char_bottom:.1f} in range {platform.y - 5:.1f}-{platform.y + 10:.1f}): {vertical_collision}")
        print(f"   Horizontal collision (overlap {char_left:.1f}-{char_right:.1f} with {platform.x + 5:.1f}-{platform.x + platform.width - 5:.1f}): {horizontal_collision}")
        
        if vertical_collision and horizontal_collision:
            print(f"✅ Collision detected! P{character.player_id} on {platform_id}")
            
            # Character is landing on or standing on this platform
            if character.velocity[1] > 0:  # Only if falling
                print(f"🛬 P{character.player_id} landing: setting Y to {platform.y}, stopping fall")
                character.position[1] = platform.y
                character.velocity[1] = 0
                character.on_ground = True
            else:
                print(f"🏠 P{character.player_id} standing on {platform_id}")
            
            character.on_ground = True
            return True
        else:
            print(f"❌ No collision: P{character.player_id} not on {platform_id}")
        
        return False
    
    def handle_plains_ground_collision(self, character):
        """
        Handle ground collision for Plains stage (simple flat ground)
        
        Args:
            character: Character to check ground collision for
        """
        ground_level = 500  # Plains ground level
        
        # Only land on ground if character is falling and at ground level
        if (character.position[1] >= ground_level and character.velocity[1] > 0):
            character.position[1] = ground_level
            character.velocity[1] = 0
            character.on_ground = True
        elif character.position[1] < ground_level:
            character.on_ground = False
    
    def check_blast_zone_ko(self, character, stage):
        """
        Check if character has entered a blast zone and should be KO'd
        
        This replaces artificial boundaries with proper blast zone mechanics.
        Characters can now fall off-stage and die as intended in fighting games.
        
        Args:
            character: Character to check blast zones for
            stage: Stage object or pygame.Rect
        """
        character_x = character.position[0]
        character_y = character.position[1]
        
        # === GET BLAST ZONE BOUNDARIES ===
        blast_zones = self.get_stage_blast_zones(stage)
        
        # === CHECK EACH BLAST ZONE ===
        ko_direction = None
        
        # Left blast zone
        if character_x < blast_zones['left']:
            ko_direction = "left"
        # Right blast zone
        elif character_x > blast_zones['right']:
            ko_direction = "right"
        # Top blast zone  
        elif character_y < blast_zones['top']:
            ko_direction = "top"
        # Bottom blast zone
        elif character_y > blast_zones['bottom']:
            ko_direction = "bottom"
        
        # === HANDLE KO ===
        if ko_direction:
            self.ko_character(character, ko_direction)
    
    def get_stage_blast_zones(self, stage):
        """
        Get blast zone boundaries for a stage
        
        Args:
            stage: Stage object or pygame.Rect
            
        Returns:
            dict: Blast zone boundaries with 'left', 'right', 'top', 'bottom' keys
        """
        if hasattr(stage, 'left_blast_zone'):
            # Modern stage object with defined blast zones
            return {
                'left': stage.left_blast_zone,
                'right': stage.right_blast_zone,
                'top': stage.top_blast_zone,
                'bottom': stage.bottom_blast_zone
            }
        else:
            # Legacy stage or fallback blast zones
            if isinstance(stage, pygame.Rect):
                # Determine blast zones based on stage type
                if stage.width == 1080:  # Battlefield
                    return {
                        'left': -200,
                        'right': 1480,
                        'top': -200,
                        'bottom': 920
                    }
                else:  # Plains
                    return {
                        'left': -300,
                        'right': 1580,
                        'top': -200,
                        'bottom': 920
                    }
            else:
                # Default blast zones
                return {
                    'left': -300,
                    'right': 1580,
                    'top': -200,
                    'bottom': 920
                }
    
    def ko_character(self, character, direction):
        """
        Handle character KO when they enter a blast zone
        
        Args:
            character: Character that was KO'd
            direction: Direction of the blast zone ('left', 'right', 'top', 'bottom')
        """
        print(f"💀 Player {character.player_id} KO'd by {direction} blast zone!")
        
        # Mark character as KO'd
        character.is_ko = True
        character.ko_direction = direction
        
        # Reset character position to respawn point
        if character.player_id == 1:
            character.position = [300, 400]  # Player 1 respawn
        else:
            character.position = [900, 400]  # Player 2 respawn
        
        # Reset character velocity
        character.velocity = [0, 0]
        character.on_ground = False
        
        # Add respawn invincibility
        character.respawn_invincibility = 120  # 2 seconds at 60 FPS
        
        print(f"🔄 Player {character.player_id} respawning...")
        
        # TODO: Add visual effects for KO and respawn
        # TODO: Add stock/lives system
        # TODO: Add respawn animation
    
    def handle_battlefield_platforms(self, character):
        """
        Handle collision with battlefield platforms
        """
        # Define platform positions (must match the rendering in state_manager.py)
        main_platform = pygame.Rect(240, 500, 800, 40)
        left_platform = pygame.Rect(150, 400, 300, 30)  
        right_platform = pygame.Rect(830, 400, 300, 30)
        
        platforms = [main_platform, left_platform, right_platform]
        
        # Check if character is standing on any platform
        char_bottom = character.position[1]
        char_left = character.position[0] - character.width / 2
        char_right = character.position[0] + character.width / 2
        
        character_on_platform = False
        
        # Check collision with each platform
        for platform in platforms:
            # Check if character is standing on this platform
            if (char_bottom >= platform.top - 5 and  # At platform level
                char_bottom <= platform.top + 10 and  # Not too far below
                char_right > platform.left + 5 and  # Character overlaps platform
                char_left < platform.right - 5):  # Character overlaps platform
                
                # Character is on this platform
                character_on_platform = True
                
                # If character is falling, land them properly
                if character.velocity[1] > 0:
                    character.position[1] = platform.top
                    character.velocity[1] = 0
                    if not character.on_ground:  # Only print when first landing
                        print(f"Player {character.player_id} landed on battlefield platform at {platform.topleft}")
                
                character.on_ground = True
                return  # Only land on one platform
        
        # If not on any platform, character is in air
        if not character_on_platform:
            character.on_ground = False
        
        # If no platform collision, character continues falling
        # No ground collision for battlefield - let them fall off!
    
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
            hitboxes_to_remove = []
            
            for hitbox in attacker.active_hitboxes:
                hit_someone = False
                
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
                        # Handle multi-hit attacks differently
                        is_multihit = hitbox.get('is_multihit', False)
                        
                        if is_multihit:
                            # For multi-hit attacks, check if enough time has passed since last hit
                            current_frame = attacker.attack_state_frames
                            last_hit = hitbox.get('last_hit_frame', 0)
                            hit_interval = hitbox.get('hit_interval', 4)
                            
                            if current_frame - last_hit >= hit_interval:
                                self.apply_hit(hitbox, defender)
                                hitbox['last_hit_frame'] = current_frame
                                hit_someone = True
                        else:
                            # Regular attacks hit once then remove hitbox
                            self.apply_hit(hitbox, defender)
                            hit_someone = True
                            # Mark for removal (but don't remove immediately to avoid iteration issues)
                            if hitbox not in hitboxes_to_remove:
                                hitboxes_to_remove.append(hitbox)
                            break
                
                # Update projectiles
                if hitbox.get('is_projectile', False):
                    # Move projectile
                    hitbox['x'] += hitbox.get('velocity_x', 0)
                    hitbox['y'] += hitbox.get('velocity_y', 0)
                    
                    # Decrease lifetime
                    hitbox['lifetime'] -= 1
                    
                    # Mark for removal if expired or off-screen
                    if (hitbox['lifetime'] <= 0 or 
                        hitbox['x'] < -100 or hitbox['x'] > 1380 or
                        hitbox['y'] > 800):
                        if hitbox not in hitboxes_to_remove:
                            hitboxes_to_remove.append(hitbox)
            
            # Remove hitboxes that should be removed
            for hitbox in hitboxes_to_remove:
                if hitbox in attacker.active_hitboxes:
                    attacker.active_hitboxes.remove(hitbox)
    
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
        
        knockback_vector = [knockback_x, knockback_y]
        
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