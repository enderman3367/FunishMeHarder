"""
Base Character - Foundation for all fighters
=============================================

This module contains the base Character class that all fighters inherit from.
Defines common properties, methods, and behaviors shared by all characters.

Key Features for Smooth Movement:
- Acceleration/deceleration-based movement (no instant velocity changes)
- Frame-based animation system with interpolation
- State machine for seamless action transitions
- Input buffering for responsive controls
- Physics-based momentum conservation
"""

import pygame
import numpy as np
from enum import Enum

class CharacterState(Enum):
    """
    All possible character states for animation and behavior
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
    Base class for all playable characters with smooth movement physics
    """
    
    def __init__(self, x, y, player_id):
        """
        Initialize a character with smooth physics system
        """
        # Position and physics
        self.position = np.array([float(x), float(y)])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.facing_right = True if player_id == 1 else False
        
        # Movement physics constants for smooth gameplay
        self.max_walk_speed = 3.0
        self.max_run_speed = 6.0
        self.ground_acceleration = 0.4  # How quickly we reach max speed
        self.ground_deceleration = 0.6  # How quickly we stop
        self.air_acceleration = 0.2     # Slower air control
        self.air_deceleration = 0.1     # Maintain momentum in air
        self.jump_strength = 15.0
        self.short_hop_strength = 8.0   # For light jump inputs
        
        # Character stats (Smash Bros style - damage goes UP from 0%)
        self.damage_percent = 0.0  # Starts at 0%, goes up when hit
        self.max_damage_percent = 999.0  # Theoretical max (usually KO'd before this)
        self.weight = 1.0  # Affects knockback and fall speed
        
        # Ground and collision state
        self.on_ground = True
        self.can_jump = True
        self.coyote_time = 0.0  # Brief time after leaving ground where you can still jump
        self.coyote_time_max = 0.1  # 6 frames at 60fps
        
        # State management
        self.current_state = CharacterState.IDLE
        self.previous_state = CharacterState.IDLE
        self.state_timer = 0.0
        self.can_act = True
        self.can_cancel = False  # For combo canceling
        
        # Combat properties
        self.is_attacking = False
        self.attack_state_frames = 0  # Current frame of attack
        self.hit_stun_timer = 0.0
        self.invincibility_timer = 0.0
        self.active_hitboxes = []
        self.current_attack = None  # Stores current attack data
        self.attack_hitbox_created = False  # Track if hitbox was created this attack
        
        # Animation system for smooth visuals
        self.animation_frame = 0.0  # Float for smooth interpolation
        self.animation_speed = 0.2   # Animation playback speed
        self.sprite_scale = 1.0      # For hit effects, etc.
        
        # Input buffering for responsive controls
        self.input_buffer = []
        self.buffer_time = 6  # frames to buffer inputs
        
        # Visual effects
        self.hit_flash_timer = 0.0
        self.screen_shake_intensity = 0.0
        
        self.player_id = player_id
        
        # Size for collision (will be overridden by sprites later)
        self.width = 60
        self.height = 80
    
    def update(self, delta_time, player_input, stage):
        """
        Main update loop with smooth physics and responsive controls
        """
        # Update timers
        self.state_timer += delta_time
        self.hit_stun_timer = max(0, self.hit_stun_timer - delta_time)
        self.invincibility_timer = max(0, self.invincibility_timer - delta_time)
        self.coyote_time = max(0, self.coyote_time - delta_time)
        
        # Update visual effects
        self.hit_flash_timer = max(0, self.hit_flash_timer - delta_time)
        self.screen_shake_intensity *= 0.9  # Decay screen shake
        
        # Process input only if we can act (not in hitstun, etc.)
        if self.can_act and self.hit_stun_timer <= 0:
            self.handle_input(player_input)
        
        # Update physics
        self.update_physics(delta_time)
        
        # Update animations
        self.update_animations(delta_time)
        
        # Handle state transitions
        self.update_state_machine(delta_time)
        
        # Update attack frames
        if self.is_attacking:
            self.attack_state_frames += 1
            self.update_attack_timing()
    
    def handle_input(self, player_input):
        """
        Process player input with smooth movement and Smash-style attacks
        """
        # Movement input with smooth acceleration
        horizontal_input = 0.0
        if player_input.is_pressed('left'):
            horizontal_input -= 1.0
            if self.facing_right:
                self.facing_right = False
        if player_input.is_pressed('right'):
            horizontal_input += 1.0
            if not self.facing_right:
                self.facing_right = True
        
        # Apply movement based on ground state
        if self.on_ground:
            self.apply_ground_movement(horizontal_input)
        else:
            self.apply_air_movement(horizontal_input)
        
        # Jumping with coyote time and short hops
        if player_input.was_just_pressed('up'):
            if self.on_ground or self.coyote_time > 0:
                # Short hop if released quickly, full jump if held
                jump_power = self.short_hop_strength if not player_input.is_pressed('up') else self.jump_strength
                self.velocity[1] = -jump_power
                self.on_ground = False
                self.can_jump = False
                self.coyote_time = 0
                self.change_state(CharacterState.JUMPING)
        
        # Variable jump height - cut jump short if button released
        if not player_input.is_pressed('up') and self.velocity[1] < 0 and self.current_state == CharacterState.JUMPING:
            self.velocity[1] *= 0.5  # Cut jump height
        
        # Crouching
        if player_input.is_pressed('down') and self.on_ground:
            if self.current_state != CharacterState.CROUCHING:
                self.change_state(CharacterState.CROUCHING)
        elif self.current_state == CharacterState.CROUCHING:
            self.change_state(CharacterState.IDLE)
        
        # Smash-style attack system (one button + direction)
        if player_input.was_just_pressed('attack'):
            attack_direction = player_input.get_attack_direction()
            self.perform_attack(attack_direction)
    
    def apply_ground_movement(self, horizontal_input):
        """
        Apply smooth ground movement with acceleration/deceleration
        """
        if horizontal_input != 0:
            # Accelerate towards max speed
            target_speed = horizontal_input * self.max_walk_speed
            # Use different speed for running (holding direction for extended time)
            if abs(self.velocity[0]) > self.max_walk_speed * 0.8 and horizontal_input * self.velocity[0] > 0:
                target_speed = horizontal_input * self.max_run_speed
            
            # Smooth acceleration
            speed_diff = target_speed - self.velocity[0]
            acceleration = self.ground_acceleration if abs(speed_diff) > 0.1 else self.ground_deceleration
            self.velocity[0] += np.sign(speed_diff) * min(abs(speed_diff), acceleration)
            
            # Update movement state
            if abs(self.velocity[0]) > self.max_walk_speed * 1.2:
                self.change_state(CharacterState.RUNNING)
            elif abs(self.velocity[0]) > 0.5:
                self.change_state(CharacterState.WALKING)
        else:
            # Smooth deceleration when no input
            if abs(self.velocity[0]) > 0.1:
                self.velocity[0] *= (1.0 - self.ground_deceleration)
            else:
                self.velocity[0] = 0
                if self.current_state in [CharacterState.WALKING, CharacterState.RUNNING]:
                    self.change_state(CharacterState.IDLE)
    
    def apply_air_movement(self, horizontal_input):
        """
        Apply smooth air movement with momentum conservation
        """
        if horizontal_input != 0:
            target_speed = horizontal_input * self.max_walk_speed * 0.8  # Reduced air speed
            speed_diff = target_speed - self.velocity[0]
            
            # Less air control for more realistic physics
            self.velocity[0] += np.sign(speed_diff) * min(abs(speed_diff), self.air_acceleration)
        else:
            # Very slow air deceleration to maintain momentum
            if abs(self.velocity[0]) > 0.1:
                self.velocity[0] *= (1.0 - self.air_deceleration)
    
    def update_physics(self, delta_time):
        """
        Update character physics with gravity and collision
        """
        # Apply gravity when in air
        if not self.on_ground:
            gravity = 0.8 * self.weight  # Heavier characters fall faster
            self.velocity[1] += gravity
            # Terminal velocity
            if self.velocity[1] > 20.0:
                self.velocity[1] = 20.0
        
        # Update position
        old_position = self.position.copy()
        self.position[0] += self.velocity[0] * 60.0 * delta_time  # 60fps normalization
        self.position[1] += self.velocity[1] * 60.0 * delta_time
        
        # Basic ground collision (will be replaced with proper stage collision)
        if self.position[1] > 500:  # Ground level
            self.position[1] = 500
            if not self.on_ground and self.velocity[1] > 0:
                self.on_ground = True
                self.can_jump = True
                self.velocity[1] = 0
                self.change_state(CharacterState.LANDING)
        else:
            if self.on_ground and self.velocity[1] != 0:
                self.on_ground = False
                self.coyote_time = self.coyote_time_max
    
    def change_state(self, new_state):
        """
        Change character state with proper transitions and animation resets
        """
        if new_state == self.current_state:
            return
        
        # Store previous state for combo/cancel checking
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_timer = 0.0
        self.animation_frame = 0.0
        
        # State-specific initialization
        if new_state == CharacterState.LANDING:
            # Brief landing lag
            self.can_act = False
            # Auto-transition to idle after short time
            if self.state_timer > 0.2:
                self.change_state(CharacterState.IDLE)
        elif new_state in [CharacterState.IDLE, CharacterState.WALKING, CharacterState.RUNNING]:
            self.can_act = True
            self.is_attacking = False
            self.attack_state_frames = 0
        elif new_state == CharacterState.FALLING:
            self.on_ground = False
    
    def perform_attack(self, direction):
        """
        Execute attack based on direction (Smash-style)
        """
        if not self.can_act or self.is_attacking:
            return
        
        print(f"Player {self.player_id} performing {direction} attack!")  # Debug
        
        self.is_attacking = True
        self.attack_state_frames = 0
        self.can_act = False
        
        # Set attack properties based on direction
        if direction == 'neutral':
            self.change_state(CharacterState.LIGHT_ATTACK)
            self.current_attack = {
                'type': 'neutral',
                'startup_frames': 6,
                'active_frames': 4,
                'recovery_frames': 8,
                'damage': 8,
                'knockback': 5
            }
        elif direction == 'side':
            self.change_state(CharacterState.HEAVY_ATTACK)
            self.current_attack = {
                'type': 'side',
                'startup_frames': 8,
                'active_frames': 5,
                'recovery_frames': 12,
                'damage': 12,
                'knockback': 8
            }
        elif direction == 'up':
            self.change_state(CharacterState.UP_SPECIAL)
            self.current_attack = {
                'type': 'up',
                'startup_frames': 10,
                'active_frames': 6,
                'recovery_frames': 15,
                'damage': 10,
                'knockback': 12
            }
        elif direction == 'down':
            self.change_state(CharacterState.DOWN_SPECIAL)
            self.current_attack = {
                'type': 'down',
                'startup_frames': 12,
                'active_frames': 3,
                'recovery_frames': 20,
                'damage': 15,
                'knockback': 10
            }
        
        # Store attack data for frame timing
        self.attack_hitbox_created = False
    
    def take_damage(self, damage, knockback_vector, attacker):
        """
        Handle taking damage with Smash Bros style percentage and scaling knockback
        """
        if self.invincibility_timer > 0:
            return  # Invincible
        
        # Apply damage (increase percentage)
        self.damage_percent += damage
        
        # Scale knockback based on damage percentage (like Smash Bros)
        damage_multiplier = 1.0 + (self.damage_percent * 0.01)  # More damage = more knockback
        scaled_knockback = [knockback_vector[0] * damage_multiplier / self.weight,
                           knockback_vector[1] * damage_multiplier / self.weight]
        self.velocity[0] += scaled_knockback[0]
        self.velocity[1] += scaled_knockback[1]
        
        # Enter hitstun (also scales with damage)
        hitstun_duration = (damage + self.damage_percent * 0.02) * 0.01
        self.hit_stun_timer = hitstun_duration
        self.can_act = False
        
        # Visual effects
        self.hit_flash_timer = 0.2
        self.screen_shake_intensity = damage * 0.5
        
        # Brief invincibility
        self.invincibility_timer = 0.3
        
        self.change_state(CharacterState.HIT_STUN)
        
        print(f"Player {self.player_id} took {damage} damage! Now at {self.damage_percent:.0f}%")
    
    def update_animations(self, delta_time):
        """
        Update animation frames for smooth visual feedback
        """
        self.animation_frame += self.animation_speed * 60 * delta_time
        
        # Loop animation based on state
        max_frames = self.get_animation_frame_count(self.current_state)
        if max_frames > 0 and self.animation_frame >= max_frames:
            if self.current_state in [CharacterState.IDLE, CharacterState.WALKING, CharacterState.RUNNING]:
                self.animation_frame = 0  # Loop these animations
            else:
                self.animation_frame = max_frames - 1  # Hold last frame
    
    def get_animation_frame_count(self, state):
        """
        Get number of animation frames for a state
        """
        frame_counts = {
            CharacterState.IDLE: 8,
            CharacterState.WALKING: 6,
            CharacterState.RUNNING: 8,
            CharacterState.JUMPING: 4,
            CharacterState.FALLING: 2,
            CharacterState.LIGHT_ATTACK: 6,
            CharacterState.HEAVY_ATTACK: 10,
        }
        return frame_counts.get(state, 1)
    
    def update_state_machine(self, delta_time):
        """
        Handle automatic state transitions
        """
        # Auto-transition from landing to idle
        if self.current_state == CharacterState.LANDING and self.state_timer > 0.2:
            self.change_state(CharacterState.IDLE)
            self.can_act = True
        
        # Transition from jumping to falling
        if self.current_state == CharacterState.JUMPING and self.velocity[1] > 0:
            self.change_state(CharacterState.FALLING)
        
        # End hitstun
        if self.current_state == CharacterState.HIT_STUN and self.hit_stun_timer <= 0:
            self.can_act = True
            if self.on_ground:
                self.change_state(CharacterState.IDLE)
            else:
                self.change_state(CharacterState.FALLING)
    
    def render(self, screen, camera_offset=(0, 0)):
        """
        Render character with smooth animations and effects
        """
        # Apply camera offset
        screen_x = self.position[0] - camera_offset[0]
        screen_y = self.position[1] - camera_offset[1]
        
        # Calculate sprite flipping
        flip_horizontal = not self.facing_right
        
        # Hit flash effect
        color_mod = (255, 255, 255) if self.hit_flash_timer <= 0 else (255, 200, 200)
        
        # Simple rectangle rendering (replace with sprite rendering later)
        character_rect = pygame.Rect(
            screen_x - self.width // 2,
            screen_y - self.height,
            self.width,
            self.height
        )
        
        # Character body
        pygame.draw.rect(screen, color_mod, character_rect)
        
        # Direction indicator
        face_color = (0, 255, 0) if self.facing_right else (255, 0, 0)
        face_rect = pygame.Rect(
            screen_x + (10 if self.facing_right else -20),
            screen_y - self.height + 10,
            10, 10
        )
        pygame.draw.rect(screen, face_color, face_rect)
        
        # Debug: Show velocity as arrow
        if abs(self.velocity[0]) > 0.1 or abs(self.velocity[1]) > 0.1:
            end_x = screen_x + self.velocity[0] * 3
            end_y = screen_y + self.velocity[1] * 3
            pygame.draw.line(screen, (255, 255, 0), 
                           (screen_x, screen_y), (end_x, end_y), 2)
        
        # Debug: Show attack hitboxes
        for hitbox in self.active_hitboxes:
            hitbox_rect = pygame.Rect(
                hitbox['x'] - camera_offset[0] - hitbox['width'] // 2,
                hitbox['y'] - camera_offset[1] - hitbox['height'] // 2,
                hitbox['width'],
                hitbox['height']
            )
            pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 3)  # Red hitbox
        
        # Debug: Show attack state
        if self.is_attacking and self.current_attack:
            attack_text = f"{self.current_attack['type']} F{self.attack_state_frames}"
            # This would need a font, but we'll add it to debug info later
    
    def get_collision_rect(self):
        """
        Get the character's collision rectangle.
        """
        return pygame.Rect(
            self.position[0] - self.width // 2,
            self.position[1] - self.height,
            self.width,
            self.height
        )
    
    def is_on_ground(self):
        """
        Check if the character is on the ground
        """
        return self.on_ground
    
    def get_hurtboxes(self):
        """
        Get current vulnerability hurtboxes
        """
        # Simple single hurtbox for now
        return [pygame.Rect(
            self.position[0] - self.width // 2,
            self.position[1] - self.height,
            self.width,
            self.height
        )]
    
    def get_character_specific_stats(self):
        """
        Return character stats for UI display
        """
        return {
            "name": "Base Character",
            "health": f"{self.damage_percent:.0f}%",
            "state": self.current_state.value,
            "on_ground": self.on_ground,
            "velocity": f"({self.velocity[0]:.1f}, {self.velocity[1]:.1f})"
        }
    
    def update_attack_timing(self):
        """
        Handle attack frame timing and hitbox creation
        """
        if not self.current_attack:
            return
        
        startup = self.current_attack['startup_frames']
        active = self.current_attack['active_frames']
        recovery = self.current_attack['recovery_frames']
        
        # Check which phase we're in
        if self.attack_state_frames < startup:
            # Startup phase - no hitbox yet
            pass
        elif self.attack_state_frames < startup + active:
            # Active phase - create hitbox if not already created
            if not self.attack_hitbox_created:
                self.create_attack_hitbox()
                self.attack_hitbox_created = True
        elif self.attack_state_frames >= startup + active + recovery:
            # End attack
            self.end_attack()
    
    def create_attack_hitbox(self):
        """
        Create hitbox for the current attack
        """
        if not self.current_attack:
            return
        
        # Calculate hitbox position based on attack type and facing direction
        hitbox_offset_x = 60 if self.facing_right else -60
        hitbox_offset_y = -40
        
        # Different hitbox positions for different attacks
        if self.current_attack['type'] == 'up':
            hitbox_offset_x = 0
            hitbox_offset_y = -80
        elif self.current_attack['type'] == 'down':
            hitbox_offset_x = 0
            hitbox_offset_y = -10
        
        hitbox_x = self.position[0] + hitbox_offset_x
        hitbox_y = self.position[1] + hitbox_offset_y
        
        # Create hitbox data
        hitbox = {
            'x': hitbox_x,
            'y': hitbox_y,
            'width': 50,
            'height': 50,
            'damage': self.current_attack['damage'],
            'knockback': self.current_attack['knockback'],
            'knockback_angle': self.get_knockback_angle(),
            'owner': self,
            'frames_remaining': self.current_attack['active_frames']
        }
        
        self.active_hitboxes.append(hitbox)
        print(f"Created {self.current_attack['type']} attack hitbox!")  # Debug
    
    def get_knockback_angle(self):
        """
        Get knockback angle based on attack type
        """
        if self.current_attack['type'] == 'up':
            return -75  # Upward angle
        elif self.current_attack['type'] == 'down':
            return 45   # Downward angle
        else:
            return 0    # Horizontal
    
    def end_attack(self):
        """
        End the current attack and return to normal state
        """
        self.is_attacking = False
        self.can_act = True
        self.current_attack = None
        self.attack_hitbox_created = False
        self.active_hitboxes.clear()
        
        # Return to appropriate state
        if self.on_ground:
            self.change_state(CharacterState.IDLE)
        else:
            self.change_state(CharacterState.FALLING)
        
        print(f"Player {self.player_id} attack ended")  # Debug 