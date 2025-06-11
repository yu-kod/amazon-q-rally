# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-06-11

### Added
- Initial release of Amazon Q Rally
- Realistic rally car physics with manual transmission
- Procedural track generation with multiple surface types
- RPM-based engine sound system with 8 different sound levels
- Dynamic track sections (straights, curves, hairpins, chicanes, elevation)
- Multiple surface types (tarmac, gravel, dirt) with different grip levels
- Real-time telemetry display (speed, RPM, gear, distance)
- Death line penalty system for going off-track
- Endless mode with increasing difficulty
- Manual transmission with clutch control
- Drift mechanics with visual and audio feedback

### Features
- **Car Physics**: Realistic acceleration, braking, and drift mechanics
- **Track Generation**: Procedural generation of rally-style tracks
- **Audio System**: Dynamic engine sounds that change with RPM
- **Surface Variety**: Different road surfaces affecting car handling
- **UI Elements**: Speed gauge, RPM tachometer, gear indicator
- **Controls**: Full keyboard control with manual transmission

### Technical Implementation
- Modular architecture with separate physics, audio, and rendering systems
- Tile-based track rendering (16x16 pixel tiles)
- Chunk-based track generation for efficient memory usage
- Procedural audio generation using NumPy
- Vector-based physics simulation

### Controls
- WASD/Arrow keys for driving
- Q/E for gear shifting
- Space for clutch
- R for restart
- ESC to quit
