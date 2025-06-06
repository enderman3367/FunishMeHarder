# Super Smash Bros Game - Python Edition

A comprehensive 2D fighting game inspired by Super Smash Bros, built with Python and Pygame. Features smooth character movement, special attacks, multiple stages, and competitive fighting game mechanics.

## 🎮 Game Features

### Core Gameplay
- **Two-player local combat** with simultaneous inputs
- **3 unique characters** with distinct playstyles:
  - **Warrior** - Balanced all-around fighter
  - **Speedster** - Fast, agile rushdown character  
  - **Heavy** - Slow but powerful tank character
- **2 battle stages** with different layouts and mechanics:
  - **Battlefield** - Classic competitive stage
  - **Volcano** - Dynamic stage with hazards and moving platforms

### Controls
- **Player 1**: WASD for movement + Q/E/R/T/F/G for attacks
- **Player 2**: IKJL for movement + U/O/P/[/;/' for attacks
- **Special Moves**: Side, Up, Down, and Neutral specials for each character
- **Advanced Mechanics**: Combos, air dashes, wall jumps (character dependent)

### Game Modes
- **Character Select** - Choose your fighter with stat previews
- **Stage Select** - Pick your battlefield
- **Main Menu** - Clean navigation interface
- **Options** - Customizable settings and controls

## 🏗️ Project Structure

```
FunishMeHarder/
├── main.py                     # Game entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── src/                        # Main source code
│   ├── core/                   # Core game engine
│   │   ├── game_engine.py      # Main game loop and coordination
│   │   └── state_manager.py    # Game state management
│   │
│   ├── characters/             # Fighter system
│   │   ├── base_character.py   # Base character class
│   │   ├── warrior.py          # Balanced fighter
│   │   ├── speedster.py        # Fast agile fighter
│   │   └── heavy.py            # Powerful tank fighter
│   │
│   ├── stages/                 # Battle arenas
│   │   ├── base_stage.py       # Base stage class
│   │   ├── battlefield.py      # Classic platform stage
│   │   └── volcano.py          # Dynamic hazard stage
│   │
│   ├── input/                  # Input handling
│   │   └── input_manager.py    # Player controls and special moves
│   │
│   ├── physics/                # Physics engine
│   │   └── physics_manager.py  # Collision and movement
│   │
│   ├── ui/                     # User interface
│   │   ├── main_menu.py        # Main menu state
│   │   └── character_select.py # Character selection
│   │
│   └── utils/                  # Utility functions
│       └── config.py           # Game configuration
│
├── assets/                     # Game assets (to be created)
│   ├── images/                 # Sprites and textures
│   │   ├── characters/         # Character sprites
│   │   ├── stages/             # Stage backgrounds
│   │   └── ui/                 # Interface elements
│   │
│   ├── audio/                  # Sound effects and music
│   │   ├── sfx/                # Sound effects
│   │   └── music/              # Background music
│   │
│   └── data/                   # Configuration files
│       ├── characters/         # Character data
│       └── stages/             # Stage data
│
└── tests/                      # Unit tests (to be implemented)
    ├── test_characters.py
    ├── test_physics.py
    └── test_input.py
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd FunishMeHarder
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the game**
```bash
python main.py
```

### Dependencies
- `pygame==2.5.2` - Main game engine
- `numpy==1.24.3` - Math and physics calculations
- `Pillow==10.0.0` - Image processing
- `PyYAML==6.0.1` - Configuration files
- `pygame-gui==0.6.9` - Advanced UI components (optional)
- `pymunk==6.5.2` - Advanced physics (optional)

## 🎯 Development Roadmap

### Phase 1: Core Foundation ✅
- [x] Project structure setup
- [x] Basic game engine architecture
- [x] State management system
- [x] Input handling framework
- [x] Character and stage base classes

### Phase 2: Basic Gameplay 🚧
- [ ] Implement character movement and physics
- [ ] Add basic attack system
- [ ] Create hitbox/hurtbox collision detection
- [ ] Implement stage collision
- [ ] Add visual feedback and animations

### Phase 3: Character Development 📅
- [ ] Complete Warrior character implementation
- [ ] Complete Speedster character implementation  
- [ ] Complete Heavy character implementation
- [ ] Add character-specific special moves
- [ ] Implement combo system

### Phase 4: Stage Development 📅
- [ ] Complete Battlefield stage
- [ ] Complete Volcano stage with hazards
- [ ] Add stage-specific mechanics
- [ ] Implement camera system

### Phase 5: Polish & Features 📅
- [ ] Add visual effects and animations
- [ ] Implement audio system
- [ ] Create particle effects
- [ ] Add screen shake and juice
- [ ] Implement training mode

### Phase 6: Advanced Features 📅
- [ ] Add more characters and stages
- [ ] Implement replay system
- [ ] Add online multiplayer
- [ ] Create tournament mode
- [ ] Add mod support

## 🎨 Art & Assets Strategy

### Visual Style
- **2D sprite-based graphics** for retro fighting game feel
- **Smooth 60fps animations** for responsive gameplay
- **Particle effects** for impact and special moves
- **Dynamic lighting** for atmospheric stages

### Asset Creation Pipeline
1. **Placeholder Graphics** - Simple colored rectangles during development
2. **Sprite Creation** - Pixel art or hand-drawn sprites
3. **Animation Systems** - Frame-based animation with smooth interpolation
4. **Effect Systems** - Particle effects for hits, explosions, etc.

### Audio Design
- **Background Music** - Stage-specific themes with loop points
- **Sound Effects** - Satisfying impact sounds and character voices
- **Dynamic Audio** - Music that responds to gameplay intensity

## 🔧 Technical Architecture

### Game Engine Design
- **Entity-Component-System (ECS)** for flexible game objects
- **State Machine** for game flow management
- **Observer Pattern** for event handling
- **Fixed Timestep** for consistent physics

### Performance Considerations
- **Spatial Partitioning** for efficient collision detection
- **Object Pooling** for frequently created/destroyed objects
- **Sprite Batching** for optimized rendering
- **Frame Rate Management** with delta time calculations

### Fighting Game Mechanics
- **Frame-Perfect Input** for competitive play
- **Input Buffering** for combo execution
- **Hit/Hurt Box System** for precise combat
- **Knockback Calculations** based on damage and character weight

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Follow the existing code style and documentation standards
4. Add comprehensive comments and TODOs for future implementation
5. Test your changes thoroughly
6. Submit a pull request

### Code Style Guidelines
- Use **clear, descriptive variable names**
- Add **comprehensive docstrings** for all classes and methods
- Include **TODO comments** for future implementation details
- Follow **Python PEP 8** style guidelines
- Separate **game logic** from **rendering** code

### Areas Needing Contribution
- **Asset Creation** - Sprites, animations, sound effects
- **Character Implementation** - Special moves and abilities
- **Stage Design** - New battlefields with unique mechanics
- **UI/UX Design** - Menus and interface improvements
- **Testing** - Unit tests and integration tests
- **Documentation** - Tutorials and API documentation

## 📚 Learning Resources

### Fighting Game Development
- [Fighting Game Primer](https://www.gamedeveloper.com/design/fighting-game-primer) - Game design concepts
- [Frame Data Explanation](https://glossary.infil.net/) - Understanding fighting game mechanics
- [Hitbox/Hurtbox Systems](https://www.youtube.com/watch?v=kQQz_sAn1B4) - Technical implementation

### Python Game Development
- [Pygame Documentation](https://www.pygame.org/docs/) - Official Pygame reference
- [Real Python Game Development](https://realpython.com/pygame-a-primer/) - Pygame tutorial
- [Game Programming Patterns](https://gameprogrammingpatterns.com/) - Software architecture

### Assets and Tools
- [Aseprite](https://www.aseprite.org/) - Pixel art and animation
- [BFXR](https://www.bfxr.net/) - Sound effect generation
- [OpenGameArt](https://opengameart.org/) - Free game assets

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎮 Game Design Philosophy

This project aims to create a fighting game that captures the excitement and depth of Super Smash Bros while being:

- **Accessible** - Easy to pick up with simple controls
- **Deep** - Complex mechanics for competitive play
- **Modular** - Easy to add new characters and stages
- **Educational** - Well-documented code for learning game development
- **Fun** - Satisfying gameplay with smooth animations and effects

The codebase is designed as both a playable game and a learning resource, with extensive documentation and clear separation of concerns to make it easy for others to understand and contribute to fighting game development.

---

**Ready to fight?** Install the dependencies and run `python main.py` to start your Super Smash Bros adventure! 🥊 