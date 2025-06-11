# Amazon Q Rally

A realistic rally racing game built with Python and Pygame, featuring procedural track generation, realistic car physics, and immersive sound effects.

## Features

### 🏁 Realistic Rally Experience
- **Authentic Car Physics**: Realistic acceleration, braking, and drift mechanics
- **Multiple Surface Types**: Tarmac, gravel, and dirt with different grip levels
- **Manual Transmission**: 6-speed manual gearbox with clutch control
- **RPM-Based Engine Sound**: Engine sound pitch changes according to RPM

### 🛣️ Dynamic Track System
- **Procedural Generation**: Endless rally stages with varied layouts
- **Rally-Style Sections**: Straights, curves, hairpins, chicanes, and elevation changes
- **Surface Variety**: Strategic placement of different road surfaces
- **Challenging Width**: Narrow tracks for authentic rally experience

### 🎮 Game Features
- **Endless Mode**: Continuous rally stages with increasing difficulty
- **Real-time Telemetry**: Speed, RPM, gear, and distance tracking
- **Death Line System**: Penalty system for going off-track
- **Restart Functionality**: Quick restart with R key

### 🔊 Audio System
- **Dynamic Engine Sound**: 8-level RPM-based engine audio
- **Surface-Specific Audio**: Different sounds for tire slip on various surfaces
- **Gear Change Audio**: Realistic transmission sounds
- **Balanced Audio Levels**: Optimized volume levels for comfortable gameplay

## Controls

### Driving
- **W / ↑**: Accelerate
- **S / ↓**: Brake/Reverse
- **A / ←**: Steer Left
- **D / →**: Steer Right

### Transmission
- **Q**: Shift Up
- **E**: Shift Down
- **Space**: Clutch (hold while shifting for smooth gear changes)

### Game Controls
- **R**: Restart Game
- **ESC**: Quit to Menu

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Required Dependencies
```bash
pip install pygame numpy
```

### Running the Game
1. Clone this repository:
```bash
git clone https://github.com/yourusername/amazon-q-rally.git
cd amazon-q-rally
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## Technical Details

### Architecture
- **Modular Design**: Separate modules for car physics, track generation, UI, and audio
- **Object-Oriented**: Clean class structure for maintainability
- **Configurable**: Centralized configuration system

### Car Physics
- **Realistic Acceleration**: Torque curves and gear ratios
- **Surface Interaction**: Different friction coefficients for various surfaces
- **Drift Mechanics**: Authentic sliding physics with visual and audio feedback
- **Speed Limiting**: Realistic top speeds per gear

### Track Generation
- **Chunk-Based System**: Efficient memory usage with dynamic loading
- **Procedural Algorithms**: Mathematical functions for natural-looking curves
- **Surface Distribution**: Strategic placement based on track section types
- **Tile-Based Rendering**: 16x16 pixel tiles for retro aesthetic

## File Structure

```
amazon-q-rally/
├── main.py                     # Main game entry point
├── config.py                   # Game configuration
├── endless_game.py             # Main game loop and logic
├── realistic_rally_car.py      # Car physics and controls
├── realistic_car.py            # Sound system and car components
├── endless_track_advanced.py   # Track generation and rendering
├── advanced_track_generator.py # Procedural track algorithms
├── ui.py                       # User interface elements
├── tachometer.py              # RPM gauge and telemetry
├── death_line.py              # Off-track penalty system
└── README.md                  # This file
```

## Development

### Built With
- **Python 3.9+**: Core programming language
- **Pygame 2.5+**: Game development framework
- **NumPy**: Audio generation and mathematical operations

### Key Algorithms
- **Procedural Track Generation**: Sine waves and random variations for natural curves
- **Physics Simulation**: Vector-based movement with friction and surface interaction
- **Audio Synthesis**: Procedural generation of engine and tire sounds
- **Collision Detection**: Tile-based track boundary detection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with assistance from Amazon Q Developer
- Inspired by classic rally racing games
- Physics algorithms based on real automotive engineering principles

## Screenshots

*Add screenshots of your game here*

## Future Enhancements

- [ ] Multiplayer support
- [ ] More track environments (forest, desert, snow)
- [ ] Car customization and tuning
- [ ] Leaderboards and time trials
- [ ] Weather effects
- [ ] Co-driver pace notes
