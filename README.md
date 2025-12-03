# Platformer Game

A Mario-like platformer game built with Python and Pygame featuring 5 intricate maze levels with side-scrolling camera, progressive difficulty, and boss battles at the end of each level.

## Features

- **5 Intricate Maze Levels**: Complex side-scrolling level designs with multiple paths and challenges
- **Side-Scrolling Camera**: Mario/Sonic-style camera that follows the player through 3000-pixel-wide levels
- **Boss Battles at End of Levels**: Defeat bosses after navigating the maze, not at the start
- **Character Sprite**: Animated character with head, body, arms, and legs
- **Fixed Floor Collision**: Player properly stands on platforms
- **3 Difficulty Modes**: Easy, Medium, and Hard with unique mechanics and boss scaling
- **Dynamic Difficulty Scaling**:
  - Gravity affects jump control
  - Player speed varies by difficulty
  - Jump power changes
  - Enemy speed increases
  - Boss health and attack patterns scale
- **Player Movement**: Move left/right with arrow keys or A/D
- **Jumping**: Press SPACE to jump with physics-based mechanics
- **Enemies**: Regular enemies patrol throughout maze levels
- **Platform Variety**: Multiple paths, tight jumps, vertical sections, and precision platforming
- **Progressive Difficulty**: Each level introduces new challenges and mechanics
- **Replay Functionality**: Start a new game at any difficulty after completion

## Requirements

- Python 3.8+
- Pygame 2.5.0

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

- **Left Arrow / A**: Move left
- **Right Arrow / D**: Move right
- **SPACE**: Jump
- **R**: Reset to level start (during gameplay)

## Gameplay Mechanics

### Side-Scrolling Camera
- Camera smoothly follows the player
- Player stays roughly in the left third of screen
- Can explore 3000-pixel-wide levels
- Seamless scrolling like Mario or Sonic

### Maze Design
- Each level features intricate platform layouts
- Multiple routes and paths through levels
- Hidden shortcuts and alternative passages
- Vertical sections with tower-like climbs
- Horizontal precision platforming sections

### Boss Battles
- One boss appears at the END of each level
- Must navigate the entire maze first
- Jump on the boss multiple times to defeat
- Boss health displayed at top right
- Bosses patrol and jump in their arena
- Boss appears larger and stronger on higher levels
- Must defeat boss to access goal

## Difficulty Modes

### Easy
- Slower gravity (easier control)
- Faster player movement (6 speed)
- Higher jump power (16)
- Slower enemies (1.5 speed)
- Enemies can't damage you
- Bosses have reduced health
- Fewer enemies throughout level

### Medium (Default)
- Standard gravity (0.5)
- Normal player speed (5)
- Normal jump power (15)
- Normal enemy speed (2)
- Enemies can damage you
- Standard boss health
- Moderate enemy density

### Hard
- Faster gravity (0.6) - harder to control
- Slower player movement (4 speed)
- Lower jump power (14)
- Faster enemies (3 speed)
- Enemies can damage you
- Increased boss health (+2)
- Maximum enemy density
- Bosses move and jump faster

## Level Progression

### Level 1 - Maze with Tunnels
- Entrance → Vertical challenges → Horizontal maze → Tower climb
- Boss: Small (45x53)
- Boss Health: 4 (Easy), 5 (Medium), 7 (Hard)
- Paths: Main route leads to scattered enemy encounters

### Level 2 - Intricate Pathways
- Dual-path entry → Upper/Lower routes → Spiral section → Platforming gauntlet
- Boss: Growing threat (50x56)
- Boss Health: 5 (Easy), 6 (Medium), 8 (Hard)
- Features: Multiple convergence points, complex navigation

### Level 3 - Precision Maze
- Narrow corridor → Vertical tower → Floating platform challenge
- Boss: Tougher challenge (55x59)
- Boss Health: 6 (Easy), 7 (Medium), 9 (Hard)
- Features: Tight jumps, serious platforming precision needed

### Level 4 - Advanced Maze
- Multiple routes from start → Twisting corridor → Vertical climb → Final gauntlet
- Boss: Advanced threat (60x62)
- Boss Health: 7 (Easy), 8 (Medium), 10 (Hard)
- Features: Strategic routing, complex enemy placement

### Level 5 - Final Expert Challenge
- Narrow entrance → Complex winding path → Precision platforming → Tower climb → Boss arena
- FINAL BOSS: Maximum threat (65x65)
- Boss Health: 8 (Easy), 9 (Medium), 11 (Hard)
- Features: Hardest maze, most enemies, final test before completion

## Gameplay Tips

- **Navigation**: Take your time navigating the maze - find the optimal route
- **Enemy Avoidance**: Learn enemy patrol patterns to avoid damage
- **Boss Strategy**: Defeat enemies before the boss if possible to reduce pressure
- **Easy Mode**: Great for learning level layouts, bosses are weakened
- **Medium**: Balanced challenge with all mechanics active
- **Hard**: Extreme difficulty with fast enemies and tough bosses
- **Timing**: Master jump timing to maintain momentum through levels

## Project Structure

```
Platformer/
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
├── assets/              # Game assets
├── .github/
│   └── copilot-instructions.md
└── src/
    ├── game.py          # Main game loop, camera system
    ├── player.py        # Player class with sprite
    ├── platform.py      # Platform class
    ├── enemy.py         # Enemy class with patrol AI
    ├── boss.py          # Boss class with health system
    ├── level.py         # 5 intricate maze levels
    └── constants.py     # Game configuration
```

## Future Enhancements

- [ ] Animated player sprite (walking, jumping, falling states)
- [ ] Boss attack patterns (projectiles, ground slam, AoE)
- [ ] Power-ups (speed boost, jump boost, shield, invincibility)
- [ ] Collectible coins and scoring system
- [ ] Sound effects and background music
- [ ] Particle effects on jumps and hits
- [ ] Lives/Health system
- [ ] Multiple difficulty modifiers
- [ ] Level editor for custom mazes
- [ ] Speedrun timer and leaderboard
- [ ] Mobile touch controls

## Game States

1. **Difficulty Selection**: Choose Easy, Medium, or Hard
2. **Level Exploration**: Navigate through intricate maze
3. **Enemy Encounters**: Avoid or defeat scattered enemies
4. **Boss Battle**: Face boss at end of maze
5. **Boss Defeated**: Collect goal after victory
6. **Level Complete**: Advance to next level
7. **Game Complete**: Beat all 5 levels and final boss to win

## Technical Details

- **World Width**: 3000 pixels per level (10x screen width)
- **Camera System**: Smooth following with player positioned at 1/3 from left
- **Collision Detection**: Proper platform, enemy, and boss collision
- **Difficulty Scaling**: Dynamic adjustment of all game mechanics

## License

This project is open source and available for personal use.
