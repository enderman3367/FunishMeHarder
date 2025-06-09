"""
Plains Stage - Wide Open Battlefield Arena
==========================================

The Plains stage offers a completely different gameplay experience from Battlefield,
emphasizing ground-based combat and horizontal movement over vertical platform play.
This stage is perfect for characters who excel in neutral game and spacing.

Stage Design Philosophy:
========================
- Extremely wide main platform encourages ground-based neutral game
- Minimal vertical elements keep focus on horizontal spacing
- Open design rewards precise movement and positioning
- Long-range combat and projectile play are emphasized
- Perfect for teaching fundamental fighting game concepts

Unique Features:
===============
- Extra-wide main platform (largest fighting surface)
- Small side platforms for minimal vertical options
- Enhanced gravity effects that favor grounded play
- Rolling terrain with subtle elevation changes
- Natural grass and dirt visual theme

Gravity Mechanics Differences:
=============================
- Slightly increased gravity encourages staying grounded
- Reduced air time makes jumping more committal
- Enhanced ground friction for precise movement control
- Modified air friction affects projectile physics
- Platform magnetism helps with precise positioning

Visual Theme:
============
- Rolling grasslands with natural terrain
- Distant mountains and horizon for depth
- Dynamic sky with weather effects
- Realistic lighting that changes throughout the match
- Organic, natural aesthetic contrasts with Battlefield's floating platforms
"""

from .base_stage import Stage, Platform, PlatformType
import pygame
import numpy as np
import math
import random

class Plains(Stage):
    """
    Plains Stage Implementation
    
    This stage creates a fundamentally different fighting experience focused
    on ground-based combat, spacing, and neutral game rather than platform
    movement and aerial mixups.
    """
    
    def __init__(self):
        """
        Initialize the Plains stage with ground-focused design
        
        Stage Dimensions:
        - Width: 1400 pixels (wider than Battlefield for more spacing)
        - Height: 700 pixels (less vertical space emphasizes ground game)
        
        The increased width and reduced height create a 2:1 aspect ratio
        that emphasizes horizontal movement and spacing over vertical play.
        """
        # Call parent constructor with ground-focused dimensions
        super().__init__("Plains", 1400, 700)
        
        # === STAGE METADATA ===
        # Describes the stage's role and characteristics
        self.description = "Wide open grasslands perfect for ground-based combat and spacing"
        self.theme = "Natural Grasslands"
        self.music_track = "plains_winds.ogg"
        self.competitive_legal = True  # Tournament legal but different from Battlefield
        self.difficulty_rating = "Intermediate"  # Requires good spacing and neutral game
        
        # === UNIQUE GRAVITY SETTINGS ===
        # These values create a heavier, more grounded feel
        self.gravity_multiplier = 1.15     # 15% stronger gravity than Battlefield
        self.air_friction_modifier = 1.3   # 30% more air resistance
        self.terminal_velocity_cap = 16.0  # Lower terminal velocity
        self.platform_magnetism = 1.2      # Stronger "stickiness" when landing
        
        # === GROUND-FOCUSED PHYSICS ===
        # Enhanced properties for ground-based gameplay
        self.wind_resistance = 0.05        # Slight wind affects aerial movement
        self.surface_friction = 0.08       # Less ground friction for smoother movement
        self.ledge_grab_distance = 15      # Shorter ledge grab range (fewer platforms)
        self.platform_drop_frames = 12    # Longer drop-through time (more committal)
        
        # === TERRAIN PROPERTIES ===
        # Natural terrain affects movement slightly
        self.terrain_variation = 5         # Height variation in terrain (pixels)
        self.grass_friction_zones = []     # Areas with different friction
        self.elevation_changes = []        # Subtle slopes and hills
        self.natural_boundaries = True     # Organic-looking stage edges
        
        # === WEATHER SYSTEM ===
        # Dynamic weather effects that don't affect gameplay
        self.weather_enabled = True
        self.wind_direction = random.choice([-1, 1])  # Wind direction for effects
        self.wind_strength = random.uniform(0.3, 0.7)  # Wind intensity
        self.cloud_coverage = random.uniform(0.2, 0.8)  # Sky cloud density
        
        # === VISUAL EFFECTS SETTINGS ===
        # Natural, organic visual elements
        self.enable_parallax = True        # Mountain/horizon parallax
        self.grass_animation_speed = 0.3   # Swaying grass animation
        self.ambient_particle_count = 25   # More particles for natural feel
        self.lighting_intensity = 0.9      # Brighter natural lighting
        self.time_of_day = "midday"       # Affects lighting and shadows
        
        # Initialize all stage components
        self.setup_platforms()     # Create minimal platform layout
        self.setup_spawn_points()  # Define symmetric spawn positions
        self.setup_blast_zones()   # Set wide blast zone boundaries
        self.setup_terrain()       # Create natural ground variations
        self.setup_visuals()       # Initialize natural graphics
        self.setup_camera_bounds() # Define camera for wide stage
        self.setup_weather_system() # Initialize dynamic weather
        
        print(f"✓ Plains stage initialized with {len(self.platforms)} platforms")
        print(f"✓ Wind blowing {['left', 'right'][self.wind_direction == 1]} at {self.wind_strength:.1f} strength")
    
    def setup_platforms(self):
        """
        Create the minimalist Plains platform layout
        
        Platform Design Philosophy:
        ===========================
        1. One massive main platform for ground-based combat
        2. Small side platforms provide minimal vertical options
        3. Wide spacing emphasizes horizontal movement
        4. No central high platform (keeps action grounded)
        
        This layout forces players to engage in ground-based neutral game
        rather than relying on platform movement for escapes.
        """
        
        # === MAIN PLATFORM (Massive Ground Level) ===
        # This platform is much wider than Battlefield's to encourage spacing
        main_platform_width = 1000  # Much wider than Battlefield (800px)
        main_platform_height = 50   # Slightly thicker for visual weight
        main_platform_x = (self.width - main_platform_width) // 2  # Perfect center
        main_platform_y = self.height - 100  # Standard ground level
        
        self.main_platform = Platform(
            x=main_platform_x,
            y=main_platform_y,
            width=main_platform_width,
            height=main_platform_height,
            platform_type=PlatformType.SOLID  # Solid foundation for ground game
        )
        
        # Add natural platform properties
        self.main_platform.has_ledges = True      # Ledges for recovery
        self.main_platform.surface_grip = 1.0     # Full traction on natural ground
        self.main_platform.is_main_stage = True   # Primary fighting surface
        self.main_platform.terrain_type = "grass" # Natural grass surface
        self.main_platform.has_elevation_changes = True  # Subtle height variations
        
        self.platforms.append(self.main_platform)
        print(f"✓ Main platform created: {main_platform_width}x{main_platform_height} (much wider than Battlefield)")
        
        # === SIDE PLATFORMS (Minimal Vertical Options) ===
        # Small platforms on the far sides provide limited vertical gameplay
        # Positioned much further apart than Battlefield to discourage platform camping
        
        side_platform_width = 120    # Smaller than Battlefield for less camping
        side_platform_height = 18    # Thinner to feel less substantial
        side_platform_y = main_platform_y - 120  # Lower than Battlefield (less vertical play)
        
        # Left side platform (far from center)
        left_platform_x = main_platform_x + 80  # Further inset than Battlefield
        left_platform = Platform(
            x=left_platform_x,
            y=side_platform_y,
            width=side_platform_width,
            height=side_platform_height,
            platform_type=PlatformType.PASS_THROUGH  # Can still drop through
        )
        
        # Natural platform properties
        left_platform.drop_through_enabled = True
        left_platform.has_ledges = False          # No ledges (discourages camping)
        left_platform.terrain_type = "rock"       # Stone outcropping
        left_platform.platform_id = "left_outcrop"
        
        self.platforms.append(left_platform)
        
        # Right side platform (mirror positioning)
        right_platform_x = main_platform_x + main_platform_width - side_platform_width - 80
        right_platform = Platform(
            x=right_platform_x,
            y=side_platform_y,
            width=side_platform_width,
            height=side_platform_height,
            platform_type=PlatformType.PASS_THROUGH
        )
        
        # Mirror properties from left platform
        right_platform.drop_through_enabled = True
        right_platform.has_ledges = False
        right_platform.terrain_type = "rock"
        right_platform.platform_id = "right_outcrop"
        
        self.platforms.append(right_platform)
        
        print(f"✓ Side platforms created: small stone outcroppings at {side_platform_y}")
        print(f"✓ Platform layout emphasizes ground-based combat over vertical play")
        
        # === PLATFORM MEASUREMENT STORAGE ===
        # Store measurements for gameplay systems
        self.platform_heights = {
            'main': main_platform_y,
            'side': side_platform_y,
            'difference': main_platform_y - side_platform_y
        }
        
        # Calculate spacing for AI and movement systems
        self.platform_distances = {
            'side_to_side': right_platform_x - (left_platform_x + side_platform_width),
            'main_width': main_platform_width,
            'total_fighting_area': main_platform_width + (side_platform_width * 2)
        }
    
    def setup_terrain(self):
        """
        Create natural terrain variations and features
        
        Terrain Philosophy:
        ==================
        - Subtle elevation changes add visual interest without affecting gameplay
        - Different surface types provide variety in movement feel
        - Natural boundaries feel organic rather than artificial
        - Terrain guides players toward center stage combat
        """
        
        # === ELEVATION VARIATIONS ===
        # Subtle height changes across the main platform
        self.elevation_changes = []
        
        # Create gentle rolling hills across the stage
        num_elevation_points = 20
        for i in range(num_elevation_points):
            x_position = (self.width / num_elevation_points) * i
            # Use sine wave for natural rolling terrain
            elevation_offset = math.sin(i * 0.5) * self.terrain_variation
            
            self.elevation_changes.append({
                'x': x_position,
                'height_offset': elevation_offset,
                'terrain_type': 'grass'
            })
        
        # === SURFACE FRICTION ZONES ===
        # Different areas have slightly different movement properties
        self.grass_friction_zones = [
            {
                'x': self.main_platform.x,
                'width': self.main_platform.width * 0.3,
                'friction_modifier': 0.9,  # Slightly less friction (fresher grass)
                'type': 'fresh_grass'
            },
            {
                'x': self.main_platform.x + (self.main_platform.width * 0.35),
                'width': self.main_platform.width * 0.3,
                'friction_modifier': 1.0,  # Standard friction
                'type': 'normal_grass'
            },
            {
                'x': self.main_platform.x + (self.main_platform.width * 0.7),
                'width': self.main_platform.width * 0.3,
                'friction_modifier': 0.9,  # Slightly less friction
                'type': 'fresh_grass'
            }
        ]
        
        print("✓ Natural terrain variations created for visual and tactical variety")
    
    def setup_spawn_points(self):
        """
        Define spawn points optimized for ground-based combat
        
        Spawn Philosophy:
        ================
        - Greater distance between players emphasizes neutral game
        - Positioned on main platform for immediate ground access
        - Wider spacing requires more commitment to approach
        - Equal distance from center maintains competitive balance
        """
        
        # Calculate spawn positions with extra spacing for ground-focused play
        main_platform_center = self.main_platform.x + (self.main_platform.width // 2)
        spawn_distance_from_center = 320  # Much wider than Battlefield (250px)
        spawn_height_offset = -60         # Slightly higher above platform
        
        # Player 1 spawn point (left side)
        player1_spawn_x = main_platform_center - spawn_distance_from_center
        player1_spawn_y = self.main_platform.y + spawn_height_offset
        
        self.add_spawn_point(player1_spawn_x, player1_spawn_y)
        
        # Player 2 spawn point (right side)
        player2_spawn_x = main_platform_center + spawn_distance_from_center
        player2_spawn_y = self.main_platform.y + spawn_height_offset
        
        self.add_spawn_point(player2_spawn_x, player2_spawn_y)
        
        print(f"✓ Spawn points set with wider spacing ({spawn_distance_from_center}px) for neutral game")
        
        # Store spawn information for respawning and camera setup
        self.spawn_info = {
            'center_x': main_platform_center,
            'center_y': player1_spawn_y,
            'distance': spawn_distance_from_center,
            'spacing_philosophy': 'wide_neutral_game',
            'facing_inward': True
        }
    
    def setup_blast_zones(self):
        """
        Define blast zones optimized for the wider stage
        
        Blast Zone Philosophy:
        =====================
        - Wider horizontal blast zones match the increased stage width
        - Closer vertical blast zones compensate for enhanced gravity
        - Bottom blast zone positioned for spike/meteor opportunities
        - Balanced to prevent excessive camping or stalling
        """
        
        # Horizontal blast zones (adjusted for wider stage)
        horizontal_distance = 320  # Wider than Battlefield (280px)
        self.left_blast_zone = -horizontal_distance
        self.right_blast_zone = self.width + horizontal_distance
        
        # Vertical blast zones (adjusted for gravity changes)
        top_distance = 220        # Closer than Battlefield (compensates for stronger gravity)
        bottom_distance = 300     # Closer than Battlefield (easier spike KOs)
        
        self.top_blast_zone = -top_distance
        self.bottom_blast_zone = self.height + bottom_distance
        
        print(f"✓ Blast zones adjusted for wider stage: X±{horizontal_distance}, Y+{top_distance}/-{bottom_distance}")
        
        # Store blast zone information
        self.blast_zone_info = {
            'horizontal_distance': horizontal_distance,
            'top_distance': top_distance,
            'bottom_distance': bottom_distance,
            'width_advantage': horizontal_distance - 280,  # Compared to Battlefield
            'total_width': self.right_blast_zone - self.left_blast_zone,
            'total_height': self.bottom_blast_zone - self.top_blast_zone
        }
    
    def setup_weather_system(self):
        """
        Initialize dynamic weather effects
        
        Weather Philosophy:
        ==================
        - Weather provides atmosphere without affecting gameplay balance
        - Visual effects enhance the natural theme
        - Subtle environmental storytelling
        - Adds variety to multiple matches on the same stage
        """
        
        # === WIND SYSTEM ===
        # Affects visual elements but not gameplay physics
        self.wind_system = {
            'direction': self.wind_direction,
            'strength': self.wind_strength,
            'gusts': {
                'enabled': True,
                'frequency': random.uniform(0.1, 0.3),  # Gusts per second
                'strength_multiplier': random.uniform(1.5, 2.5)
            },
            'affects_grass': True,
            'affects_clouds': True,
            'affects_particles': True
        }
        
        # === CLOUD SYSTEM ===
        # Dynamic cloud coverage and movement
        self.cloud_system = {
            'coverage': self.cloud_coverage,
            'movement_speed': 0.4 * self.wind_strength,
            'types': ['cumulus', 'cirrus', 'stratus'],
            'weather_chance': {
                'clear': 0.4,
                'partly_cloudy': 0.4,
                'overcast': 0.2
            }
        }
        
        # === LIGHTING SYSTEM ===
        # Natural lighting that changes throughout the match
        self.lighting_system = {
            'time_of_day': self.time_of_day,
            'sun_angle': 45,  # Degrees above horizon
            'shadow_length': 0.6,  # Relative to object height
            'color_temperature': 5500,  # Kelvin (daylight)
            'atmospheric_scattering': True
        }
        
        print(f"✓ Weather system initialized: {['cloudy', 'clear'][self.cloud_coverage < 0.5]} skies")
    
    def setup_camera_bounds(self):
        """
        Define camera bounds optimized for the wider Plains stage
        
        Camera Philosophy:
        =================
        - Wider camera bounds accommodate the larger fighting area
        - Camera follows action while keeping the natural horizon visible
        - Smooth movement prevents motion sickness during long matches
        - Zoom limits ensure players never lose track of the action
        """
        
        # Camera movement bounds (adjusted for wider stage)
        camera_margin = 150  # Larger margins for the wider stage
        
        self.camera_bounds = pygame.Rect(
            camera_margin,                    # Left bound
            camera_margin,                    # Top bound
            self.width - (camera_margin * 2), # Width
            self.height - (camera_margin * 2) # Height
        )
        
        # Camera zoom limits (adjusted for ground-focused gameplay)
        self.min_camera_zoom = 0.6   # Zoomed out more (shows full wide stage)
        self.max_camera_zoom = 1.2   # Less zoomed in (maintains spacing visibility)
        self.default_camera_zoom = 0.8  # Slightly zoomed out by default
        
        # Camera movement smoothing (slower for the larger stage)
        self.camera_follow_speed = 0.04    # Slightly slower following
        self.camera_zoom_speed = 0.025     # Slower zoom changes
        
        print(f"✓ Camera bounds set for wide stage with {camera_margin}px margins")
    
    def setup_visuals(self):
        """
        Initialize natural visual elements and atmospheric effects
        
        Visual Design Goals:
        ===================
        - Natural, organic aesthetic contrasts with Battlefield's clean look
        - Rich environmental details create immersive atmosphere
        - Dynamic weather and lighting add variety to repeated matches
        - Performance-optimized effects maintain smooth gameplay
        """
        
        # === BACKGROUND LAYERS ===
        # Natural parallax layers for depth and atmosphere
        self.background_layers = [
            {
                "name": "sky_gradient",           # Dynamic sky based on weather
                "type": "gradient",
                "colors": [(135, 206, 235), (176, 224, 230)],  # Sky blue to light blue
                "scroll_speed": 0.0,              # Static background
                "opacity": 255,
                "weather_affected": True          # Changes with cloud coverage
            },
            {
                "name": "distant_mountains",      # Far mountain range
                "type": "mountains",
                "scroll_speed": 0.05,             # Very slow parallax
                "color": (80, 100, 120),          # Blue-gray silhouette
                "opacity": 180,
                "layer_depth": "far"
            },
            {
                "name": "rolling_hills",          # Mid-distance hills
                "type": "hills",
                "scroll_speed": 0.15,             # Moderate parallax
                "color": (60, 120, 60),           # Dark green
                "opacity": 120,
                "layer_depth": "mid"
            },
            {
                "name": "foreground_grass",       # Nearby grass details
                "type": "grass_details",
                "scroll_speed": 0.8,              # Fast parallax (close)
                "color": (34, 139, 34),           # Grass green
                "opacity": 80,
                "layer_depth": "near",
                "animated": True                  # Sways with wind
            }
        ]
        
        # === PARTICLE EFFECTS ===
        # Natural atmospheric particles
        self.particle_system = {
            "enabled": True,
            "max_particles": self.ambient_particle_count,
            "spawn_rate": 0.15,               # Particles per frame
            "wind_affected": True,            # Particles move with wind
            "particle_types": [
                {
                    "type": "pollen",
                    "size_range": (1, 2),
                    "color": (255, 255, 150, 40),  # Yellow pollen
                    "speed_range": (0.2, 0.8),
                    "lifetime_range": (400, 800),   # Longer lifetime
                    "wind_sensitivity": 1.5         # Strongly affected by wind
                },
                {
                    "type": "grass_seeds",
                    "size_range": (1, 3),
                    "color": (200, 180, 120, 30),  # Brown seeds
                    "speed_range": (0.1, 0.6),
                    "lifetime_range": (300, 600),
                    "wind_sensitivity": 2.0         # Very wind-sensitive
                },
                {
                    "type": "dust_motes",
                    "size_range": (1, 2),
                    "color": (255, 255, 255, 20),  # Light dust
                    "speed_range": (0.05, 0.3),
                    "lifetime_range": (500, 1000),
                    "wind_sensitivity": 0.8         # Moderately wind-affected
                }
            ]
        }
        
        # === LIGHTING SYSTEM ===
        # Natural lighting that changes with weather and time
        self.lighting = {
            "ambient_light": {
                "color": (255, 255, 240),        # Warm natural light
                "intensity": self.lighting_intensity,
                "direction": "omnidirectional",
                "weather_affected": True          # Dims with clouds
            },
            "sun_light": {
                "color": (255, 250, 200),        # Warm sunlight
                "intensity": 0.8,
                "angle": 60,                     # Higher sun angle
                "creates_shadows": True,         # Natural shadows
                "shadow_softness": 0.6          # Soft natural shadows
            },
            "atmospheric_scattering": {
                "enabled": True,
                "intensity": 0.3,               # Subtle atmospheric haze
                "color": (200, 220, 255),       # Blue atmospheric tint
                "distance_fade": True           # Objects fade with distance
            }
        }
        
        # === PLATFORM VISUAL PROPERTIES ===
        # Natural materials and textures
        self.platform_visuals = {
            "main_platform": {
                "base_color": (101, 67, 33),     # Rich earth brown
                "grass_color": (34, 139, 34),    # Vibrant grass green
                "edge_color": (80, 50, 20),      # Darker earth edges
                "texture": "natural_earth",      # Organic texture
                "has_grass": True,               # Grass layer on top
                "grass_density": 0.8,            # Thick grass coverage
                "shadow_opacity": 100,
                "weathering": True               # Shows natural wear
            },
            "side_platforms": {
                "base_color": (120, 120, 120),   # Gray stone
                "highlight_color": (150, 150, 150), # Lighter stone
                "edge_color": (90, 90, 90),      # Darker stone edges
                "texture": "rough_stone",        # Rocky texture
                "has_moss": True,                # Moss growth on stone
                "moss_color": (60, 100, 60),     # Dark green moss
                "shadow_opacity": 90,
                "weathering": True               # Natural stone weathering
            }
        }
        
        # === ANIMATION STATE TRACKING ===
        # Track timing for all animated elements
        self.animation_state = {
            "grass_sway_phase": 0.0,          # Grass swaying animation
            "particle_spawn_timer": 0.0,     # Particle spawning timing
            "lighting_flicker_phase": 0.0,   # Natural lighting variation
            "wind_gust_timer": 0.0,           # Wind gust timing
            "cloud_movement_offset": 0.0,    # Cloud position tracking
            "total_elapsed_time": 0.0,       # Total time for effects
            "weather_transition_timer": 0.0  # Weather change timing
        }
        
        # Initialize total elapsed time for immediate use
        self.total_elapsed_time = 0.0
        
        # Initialize grass animation phase
        self.grass_sway_phase = 0.0
        
        print("✓ Natural visual system initialized with weather effects and terrain animation")
    
    def apply_stage_gravity(self, character, delta_time):
        """
        Apply Plains-specific gravity effects to characters
        
        === PLAINS PHYSICS PHILOSOPHY ===
        Plains is designed as the "ground-focused" alternative to Battlefield.
        While Battlefield emphasizes aerial combat, Plains rewards ground game:
        
        Key Differences from Battlefield:
        - Enhanced gravity (1.15x multiplier vs 1.0x) keeps players grounded longer
        - Reduced terminal velocity (16.0 vs 18.0) for more controlled falls
        - Increased air friction (1.3x vs 0.8x) makes aerial movement more committal
        - Wind resistance affects horizontal air movement
        - Different terrain zones provide subtle movement variations
        
        Gameplay Impact:
        - Shorter combos due to faster falling
        - More emphasis on ground-based neutral game
        - Air approaches are riskier and more committal
        - Favors characters with strong ground options
        
        This creates a heavier, more deliberate feel that emphasizes
        ground-based combat and precise spacing over aerial mixups.
        
        Args:
            character: The character object to apply gravity to
            delta_time (float): Time in seconds since last frame
        """
        
        print(f"🌾 Plains gravity for P{character.player_id}: on_ground={character.on_ground}, dt={delta_time:.3f}")
        
        # Get base gravity and apply Plains modifications
        base_gravity = 0.8  # Standard gravity value
        stage_gravity = base_gravity * self.gravity_multiplier  # 15% stronger
        
        print(f"   Base gravity: {base_gravity}, multiplier: {self.gravity_multiplier}, stage gravity: {stage_gravity}")
        
        # === TERRAIN-BASED GRAVITY VARIATIONS ===
        # Different areas of the stage have slightly different gravity
        character_x = character.position[0]
        character_y = character.position[1]
        
        # Check if character is over different terrain types
        terrain_gravity_modifier = 1.0
        
        # Slightly stronger gravity near the edges (encourages center stage play)
        if character_x < self.main_platform.x + 100 or character_x > self.main_platform.x + self.main_platform.width - 100:
            terrain_gravity_modifier = 1.05  # 5% stronger gravity near edges
            print(f"   🏔️ Edge gravity boost: {terrain_gravity_modifier}x")
        
        # Apply terrain modification
        stage_gravity *= terrain_gravity_modifier
        
        # === WIND RESISTANCE EFFECTS ===
        # Subtle wind affects aerial movement (visual/atmospheric, minimal gameplay impact)
        wind_effect = 0.0
        if not character.is_on_ground() and self.weather_enabled:
            # Very subtle horizontal push based on wind direction
            wind_effect = self.wind_direction * self.wind_strength * 0.02  # Minimal effect
            print(f"   💨 Wind effect: {wind_effect:.3f}")
        
        # === APPLY MODIFIED GRAVITY ===
        if not character.is_on_ground():
            print(f"   🌊 Applying enhanced gravity {stage_gravity} to airborne P{character.player_id}")
            old_vel_y = character.velocity[1]
            
            # Apply enhanced gravity acceleration
            character.velocity[1] += stage_gravity
            
            print(f"   📈 Velocity Y: {old_vel_y:.2f} -> {character.velocity[1]:.2f}")
            
            # Apply enhanced air friction (makes jumping more committal)
            air_friction = 0.02 * self.air_friction_modifier  # 30% more air friction
            old_vel_x = character.velocity[0]
            character.velocity[0] *= (1.0 - air_friction)
            
            print(f"   🌬️ Enhanced air friction {air_friction:.4f}: vel_x {old_vel_x:.2f} -> {character.velocity[0]:.2f}")
            
            # Apply subtle wind resistance
            if wind_effect != 0.0:
                old_vel_x2 = character.velocity[0]
                character.velocity[0] += wind_effect
                print(f"   💨 Wind resistance: vel_x {old_vel_x2:.2f} -> {character.velocity[0]:.2f}")
            
            # Enforce lower terminal velocity (falls feel more controlled)
            if character.velocity[1] > self.terminal_velocity_cap:
                character.velocity[1] = self.terminal_velocity_cap
                print(f"   🏁 Terminal velocity cap applied: {self.terminal_velocity_cap}")
        else:
            print(f"   🏃 P{character.player_id} on ground")
            
            # === GROUND FRICTION VARIATIONS ===
            # Different terrain zones have slightly different friction
            ground_friction = self.surface_friction
            
            # Check if character is in a special friction zone
            for zone in self.grass_friction_zones:
                if zone['x'] <= character_x <= zone['x'] + zone['width']:
                    ground_friction *= zone['friction_modifier']
                    print(f"   🌱 Special friction zone: {ground_friction:.3f}")
                    break
            
            # Apply ground friction
            old_vel_x = character.velocity[0]
            character.velocity[0] *= (1.0 - ground_friction)
            print(f"   🏔️ Ground friction {ground_friction:.3f}: vel_x {old_vel_x:.2f} -> {character.velocity[0]:.2f}")
        
        # === ENHANCED PLATFORM MAGNETISM ===
        # Make platforms feel more "sticky" for precise positioning
        if character.is_on_ground() and hasattr(character, 'just_landed') and character.just_landed:
            # Stronger reduction of horizontal momentum when landing
            magnetism_effect = self.platform_magnetism * 0.15  # Stronger than Battlefield
            old_vel_x = character.velocity[0]
            character.velocity[0] *= (1.0 - magnetism_effect)
            print(f"   🧲 Enhanced platform magnetism: vel_x {old_vel_x:.2f} -> {character.velocity[0]:.2f}")
    
    def update(self, delta_time):
        """
        Update all dynamic Plains stage elements
        
        This method handles:
        - Weather system updates (wind, clouds, lighting)
        - Terrain animation (swaying grass, particle effects)
        - Natural lighting changes
        - Environmental sound effects
        
        Args:
            delta_time (float): Time in seconds since last update
        """
        
        # Call parent update for base functionality
        super().update(delta_time)
        
        # Track total elapsed time for natural effects
        if not hasattr(self, 'total_elapsed_time'):
            self.total_elapsed_time = 0.0
        self.total_elapsed_time += delta_time
        
        # === UPDATE WEATHER SYSTEM ===
        if self.weather_enabled:
            self.update_weather_effects(delta_time)
        
        # === UPDATE TERRAIN ANIMATION ===
        self.update_terrain_effects(delta_time)
        
        # === UPDATE NATURAL LIGHTING ===
        self.update_lighting_effects(delta_time)
        
        # === UPDATE PLATFORM STATES ===
        for platform in self.platforms:
            platform.update(delta_time)
    
    def update_weather_effects(self, delta_time):
        """
        Update dynamic weather effects
        
        Args:
            delta_time (float): Time in seconds since last update
        """
        
        # === UPDATE WIND SYSTEM ===
        # Occasional wind gusts for visual variety
        if hasattr(self, 'wind_system') and self.wind_system['gusts']['enabled']:
            # Check for wind gust timing
            if not hasattr(self, 'next_gust_time'):
                self.next_gust_time = self.total_elapsed_time + random.uniform(3.0, 8.0)
            
            if self.total_elapsed_time >= self.next_gust_time:
                # Trigger wind gust
                self.wind_strength *= self.wind_system['gusts']['strength_multiplier']
                self.wind_gust_duration = random.uniform(0.5, 1.5)
                self.wind_gust_start = self.total_elapsed_time
                
                # Schedule next gust
                self.next_gust_time = self.total_elapsed_time + random.uniform(5.0, 12.0)
            
            # End wind gust
            if hasattr(self, 'wind_gust_start'):
                if self.total_elapsed_time - self.wind_gust_start > self.wind_gust_duration:
                    self.wind_strength = random.uniform(0.3, 0.7)  # Return to normal
                    delattr(self, 'wind_gust_start')
        
        # === UPDATE CLOUD MOVEMENT ===
        if hasattr(self, 'cloud_system'):
            # Clouds move based on wind strength and direction
            cloud_speed = self.cloud_system['movement_speed'] * self.wind_direction
            # Cloud positions would be updated here in a full implementation
    
    def update_terrain_effects(self, delta_time):
        """
        Update natural terrain animations
        
        Args:
            delta_time (float): Time in seconds since last update
        """
        
        # === GRASS SWAYING ANIMATION ===
        # Grass sways based on wind strength and direction
        if not hasattr(self, 'grass_sway_phase'):
            self.grass_sway_phase = 0.0
        
        # Update grass animation phase
        sway_speed = self.grass_animation_speed * (1.0 + self.wind_strength * 0.5)
        self.grass_sway_phase += delta_time * sway_speed * 2 * math.pi
        
        # Keep phase in reasonable range
        if self.grass_sway_phase > 2 * math.pi:
            self.grass_sway_phase -= 2 * math.pi
        
        # === PARTICLE EFFECTS ===
        # Natural particles like pollen, dust, or leaves
        if not hasattr(self, 'particle_spawn_timer'):
            self.particle_spawn_timer = 0.0
        
        self.particle_spawn_timer += delta_time
        
        # Spawn particles based on wind strength
        spawn_rate = 0.2 + (self.wind_strength * 0.3)  # More particles in stronger wind
        if self.particle_spawn_timer >= spawn_rate:
            self.particle_spawn_timer = 0.0
            # Particle spawning would be implemented here
    
    def update_lighting_effects(self, delta_time):
        """
        Update natural lighting effects
        
        Args:
            delta_time (float): Time in seconds since last update
        """
        
        # === DYNAMIC LIGHTING ===
        # Subtle changes in lighting intensity based on cloud coverage
        if hasattr(self, 'lighting_system'):
            base_intensity = self.lighting_intensity
            
            # Cloud coverage affects lighting
            cloud_dimming = self.cloud_coverage * 0.2  # Up to 20% dimming
            current_intensity = base_intensity * (1.0 - cloud_dimming)
            
            # Subtle flickering for natural feel
            flicker_amount = 0.02
            flicker = math.sin(self.total_elapsed_time * 3.0) * flicker_amount
            
            self.current_lighting_intensity = current_intensity + flicker
    
    def render_background(self, screen, camera_offset):
        """
        Render the Plains background with natural parallax effects
        
        Args:
            screen: Pygame surface to render to
            camera_offset: (x, y) tuple of camera position offset
        """
        
        # === RENDER SKY ===
        # Natural sky color that changes based on cloud coverage
        base_sky_color = (135, 206, 235)  # Sky blue
        
        # Adjust sky color based on cloud coverage
        cloud_influence = self.cloud_coverage * 0.3
        sky_color = (
            int(base_sky_color[0] * (1.0 - cloud_influence)),
            int(base_sky_color[1] * (1.0 - cloud_influence)),
            int(base_sky_color[2] * (1.0 - cloud_influence * 0.5))
        )
        
        screen.fill(sky_color)
        
        # === RENDER DISTANT MOUNTAINS ===
        # Parallax background mountains for depth
        self.render_mountain_background(screen, camera_offset)
        
        # === RENDER CLOUD LAYERS ===
        # Multiple cloud layers for natural sky
        self.render_cloud_layers(screen, camera_offset)
        
        # === RENDER ATMOSPHERIC PARTICLES ===
        # Natural particles like pollen or dust
        self.render_atmospheric_particles(screen, camera_offset)
    
    def render_mountain_background(self, screen, camera_offset):
        """
        Render distant mountain silhouettes for depth
        
        Args:
            screen: Pygame surface to render to
            camera_offset: Camera position for parallax calculation
        """
        
        # Calculate parallax offset (mountains move very slowly)
        parallax_factor = 0.05
        mountain_offset_x = camera_offset[0] * parallax_factor
        
        # Mountain silhouette color (darker than sky)
        mountain_color = (80, 100, 120)
        
        # Render simple mountain shapes
        mountain_points = [
            # Left mountain range
            (0 - mountain_offset_x, screen.get_height()),
            (200 - mountain_offset_x, screen.get_height() - 150),
            (400 - mountain_offset_x, screen.get_height() - 100),
            (600 - mountain_offset_x, screen.get_height()),
            
            # Right mountain range  
            (800 - mountain_offset_x, screen.get_height()),
            (1000 - mountain_offset_x, screen.get_height() - 120),
            (1200 - mountain_offset_x, screen.get_height() - 80),
            (1400 - mountain_offset_x, screen.get_height())
        ]
        
        # Draw mountain silhouettes
        if len(mountain_points) >= 3:
            pygame.draw.polygon(screen, mountain_color, mountain_points[:4])
            if len(mountain_points) >= 7:
                pygame.draw.polygon(screen, mountain_color, mountain_points[4:])
    
    def render_cloud_layers(self, screen, camera_offset):
        """
        Render natural cloud formations
        
        Args:
            screen: Pygame surface to render to
            camera_offset: Camera position for parallax calculation
        """
        
        # Render clouds based on coverage and wind
        cloud_count = int(5 + self.cloud_coverage * 8)
        
        for i in range(cloud_count):
            # Calculate cloud position with parallax and wind movement
            parallax_factor = 0.1 + (i * 0.05)  # Different layers move at different speeds
            wind_offset = self.total_elapsed_time * self.wind_direction * 20
            
            cloud_x = (i * 300 + wind_offset - camera_offset[0] * parallax_factor) % (screen.get_width() + 400) - 200
            cloud_y = 30 + (i * 20) % 80
            
            # Cloud properties
            cloud_size = 80 + (i * 15) % 60
            cloud_opacity = int(40 + self.cloud_coverage * 60)
            
            # Render cloud
            cloud_surface = pygame.Surface((cloud_size, cloud_size // 2), pygame.SRCALPHA)
            cloud_color = (255, 255, 255, cloud_opacity)
            pygame.draw.ellipse(cloud_surface, cloud_color, (0, 0, cloud_size, cloud_size // 2))
            
            screen.blit(cloud_surface, (cloud_x, cloud_y))
    
    def render_atmospheric_particles(self, screen, camera_offset):
        """
        Render natural atmospheric particles
        
        Args:
            screen: Pygame surface to render to
            camera_offset: Camera position for parallax calculation
        """
        
        # Render floating particles affected by wind
        particle_count = self.ambient_particle_count
        
        for i in range(particle_count):
            # Calculate particle position with wind influence
            wind_influence = self.wind_direction * self.wind_strength * 50
            particle_x = (i * 100 + self.total_elapsed_time * 15 + wind_influence) % screen.get_width()
            particle_y = (i * 80 + math.sin(self.total_elapsed_time + i) * 30) % screen.get_height()
            
            # Apply camera parallax
            particle_x -= camera_offset[0] * 0.05
            particle_y -= camera_offset[1] * 0.05
            
            # Particle properties
            particle_size = 1 + (i % 3)
            particle_color = (255, 255, 200, 30)  # Warm, natural color
            
            # Render particle
            particle_surface = pygame.Surface((particle_size * 2, particle_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle_color, (particle_size, particle_size), particle_size)
            
            screen.blit(particle_surface, (particle_x, particle_y))
    
    def render_platforms(self, screen, camera_offset):
        """
        Render Plains platforms with natural styling
        
        Args:
            screen: Pygame surface to render to
            camera_offset: (x, y) tuple of camera position offset
        """
        
        # === RENDER PLATFORM SHADOWS ===
        for platform in self.platforms:
            self.render_platform_shadow(screen, platform, camera_offset)
        
        # === RENDER PLATFORMS WITH NATURAL STYLING ===
        for platform in self.platforms:
            screen_x = platform.x - camera_offset[0]
            screen_y = platform.y - camera_offset[1]
            
            # Determine platform visual style based on terrain type
            if platform == self.main_platform:
                # Main platform: natural grass and dirt
                base_color = (101, 67, 33)  # Rich brown earth
                grass_color = (34, 139, 34)  # Forest green grass
                
                # Render earth base
                platform_rect = pygame.Rect(screen_x, screen_y, platform.width, platform.height)
                pygame.draw.rect(screen, base_color, platform_rect)
                
                # Add grass layer on top
                grass_height = 8
                grass_rect = pygame.Rect(screen_x, screen_y - grass_height, platform.width, grass_height)
                pygame.draw.rect(screen, grass_color, grass_rect)
                
                # Add grass texture with swaying effect
                self.render_grass_texture(screen, grass_rect, camera_offset)
                
            else:
                # Side platforms: rocky outcroppings
                rock_color = (120, 120, 120)  # Gray stone
                highlight_color = (150, 150, 150)  # Lighter gray
                
                platform_rect = pygame.Rect(screen_x, screen_y, platform.width, platform.height)
                pygame.draw.rect(screen, rock_color, platform_rect)
                
                # Add rock texture
                pygame.draw.line(screen, highlight_color,
                               (screen_x, screen_y),
                               (screen_x + platform.width, screen_y), 2)
    
    def render_grass_texture(self, screen, grass_rect, camera_offset):
        """
        Render animated grass texture on the main platform
        
        Args:
            screen: Pygame surface to render to
            grass_rect: Rectangle area to render grass in
            camera_offset: Camera position offset
        """
        
        # Render individual grass blades with swaying animation
        grass_blade_count = grass_rect.width // 8  # One blade every 8 pixels
        
        for i in range(grass_blade_count):
            blade_x = grass_rect.x + (i * 8)
            blade_base_y = grass_rect.bottom
            blade_height = random.randint(3, 6)
            
            # Calculate sway based on wind and grass animation phase
            grass_phase = getattr(self, 'grass_sway_phase', 0.0)
            sway_amount = math.sin(grass_phase + i * 0.5) * self.wind_strength * 2
            blade_top_x = blade_x + sway_amount
            blade_top_y = blade_base_y - blade_height
            
            # Render grass blade
            grass_color = (34, 139, 34)
            pygame.draw.line(screen, grass_color,
                           (blade_x, blade_base_y),
                           (blade_top_x, blade_top_y), 1)
    
    def render_platform_shadow(self, screen, platform, camera_offset):
        """
        Render natural shadows beneath platforms
        
        Args:
            screen: Pygame surface to render to
            platform: Platform object to render shadow for
            camera_offset: Camera position offset
        """
        
        # Calculate shadow position based on lighting angle
        shadow_offset_x = 8   # Horizontal offset based on sun angle
        shadow_offset_y = 12  # Vertical offset
        
        screen_x = platform.x - camera_offset[0] + shadow_offset_x
        screen_y = platform.y - camera_offset[1] + shadow_offset_y
        
        # Shadow opacity based on lighting intensity
        shadow_opacity = int(80 * (1.0 - getattr(self, 'current_lighting_intensity', 0.9)))
        
        # Create shadow surface
        shadow_surface = pygame.Surface((platform.width, platform.height), pygame.SRCALPHA)
        shadow_color = (0, 0, 0, shadow_opacity)
        pygame.draw.rect(shadow_surface, shadow_color, (0, 0, platform.width, platform.height))
        
        screen.blit(shadow_surface, (screen_x, screen_y))
    
    def get_stage_info(self):
        """
        Get comprehensive information about the Plains stage
        
        Returns:
            dict: Complete stage information including unique features and mechanics
        """
        
        base_info = super().get_stage_info()
        
        plains_info = {
            # === BASIC INFORMATION ===
            "description": self.description,
            "theme": self.theme,
            "music_track": self.music_track,
            "difficulty_rating": self.difficulty_rating,
            
            # === COMPETITIVE INFORMATION ===
            "competitive_legal": self.competitive_legal,
            "tournament_approved": True,
            "skill_level": "Intermediate to Advanced",
            "character_advantages": "Favors spacing and neutral game specialists",
            
            # === LAYOUT INFORMATION ===
            "platform_layout": "Wide ground-focused design",
            "platform_count": len(self.platforms),
            "main_platform_width": self.platform_distances['main_width'],
            "has_ledges": True,
            "has_hazards": False,
            "symmetrical": True,
            
            # === UNIQUE MECHANICS ===
            "gravity_multiplier": self.gravity_multiplier,
            "air_friction_modifier": self.air_friction_modifier,
            "terminal_velocity": self.terminal_velocity_cap,
            "surface_friction": self.surface_friction,
            "wind_effects": self.weather_enabled,
            
            # === VISUAL FEATURES ===
            "natural_theme": True,
            "weather_system": self.weather_enabled,
            "terrain_variation": True,
            "grass_animation": True,
            "mountain_parallax": True,
            
            # === GAMEPLAY DIFFERENCES ===
            "compared_to_battlefield": {
                "wider_main_platform": f"+{self.platform_distances['main_width'] - 800}px",
                "stronger_gravity": f"+{(self.gravity_multiplier - 1.0) * 100:.0f}%",
                "more_air_friction": f"+{(self.air_friction_modifier - 1.0) * 100:.0f}%",
                "fewer_platforms": f"{len(self.platforms)} vs 4",
                "wider_blast_zones": f"+{self.blast_zone_info['width_advantage']}px"
            },
            
            # === RECOMMENDATIONS ===
            "recommended_for": [
                "Neutral game practice",
                "Spacing and footsies",
                "Projectile character training",
                "Ground-based combat",
                "Fundamental skill development"
            ],
            
            "strategies": [
                "Master precise spacing and movement",
                "Utilize the wide platform for neutral game",
                "Practice projectile zoning techniques",
                "Learn to control center stage",
                "Develop ground-based combo routes"
            ],
            
            "character_types": {
                "excellent": ["Zoners", "Spacing specialists", "Projectile users"],
                "good": ["Grapplers", "Rushdown with good neutral"],
                "challenging": ["Pure aerial fighters", "Platform movement specialists"]
            }
        }
        
        base_info.update(plains_info)
        return base_info 