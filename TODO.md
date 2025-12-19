# Knights and Creatures - UI Conversion Plan

## Project Overview
Convert the existing terminal-based text adventure to a beautiful Pygame UI with JSON-based content management.

## Week 1: Foundation & Setup

### Day 1: Environment Setup
- [ x] Install Pygame: `pip install pygame`
- [ x] Create new directory structure: `src/`, `assets/`, `data/`, `ui/`
- [ x] Set up basic Pygame window with title and basic event loop

### Day 2: JSON Data Structure Design
- [ x] Create sample JSON structure for one scene (blue_stone)
- [ x] Extract text from `blue_stone` function to JSON file
- [ x] Design JSON schema for game state tracking
- [ x] Create JSON for character classes and their abilities

### Day 3: Basic UI Framework
- [x] Create a base UI class that can render text to screen
- [x] Implement basic text wrapping for story panels
- [x] Create a simple button class
- [x] Load and display a sample text from JSON

### Day 4: Scene Management System
- [ ] Create a Scene base class
- [ ] Implement a Scene Manager to handle transitions
- [ ] Create a simple scene that loads from JSON
- [ ] Add basic transitions between scenes

### Day 5: Player Input System
- [ ] Replace `input()` functionality with mouse-based button clicks
- [ ] Implement hover effects on buttons
- [ ] Add basic keyboard navigation (arrow keys, enter)
- [ ] Test basic scene transition with JSON-loaded content

### Day 6: Content Migration
- [ ] Convert `start_game()` function to JSON and UI scene
- [ ] Create character selection UI scene
- [ ] Add class-specific ability descriptions from JSON
- [ ] Test character selection flow

## Week 2: Core Gameplay Conversion

### Day 7: Blue Stone Scenario
- [ ] Convert `blue_stone` functions to JSON format
- [ ] Create game state tracking for gemstones
- [ ] Implement the underwater cave scene with UI
- [ ] Add water elemental companion tracking

### Day 8: Yellow Stone Scenario
- [ ] Convert `yellow_stone` functions to JSON
- [ ] Implement class-based choice differences in UI
- [ ] Add desert background placeholder
- [ ] Test different paths based on player class

### Day 9: Red Stone Scenario
- [ ] Convert `red_stone` functions to JSON
- [ ] Implement volcano cave scene
- [ ] Add trap detection mechanics in UI
- [ ] Test all three tunnel paths

### Day 10: Final Dungeon & UI Polish
- [ ] Convert `void_prison` functions to JSON
- [ ] Implement portal creation scene
- [ ] Add Bart rescue mechanics
- [ ] Create victory/conclusion scenes

### Day 11: Game State & Progress Tracking
- [ ] Implement player data persistence between scenes
- [ ] Add gemstone tracking and display
- [ ] Create inventory system for UI display
- [ ] Add save/load functionality

### Day 12: UI Enhancement
- [ ] Add background images for each scene
- [ ] Implement character portrait displays
- [ ] Add visual effects (transitions, animations)
- [ ] Create a consistent visual theme

## Week 3: Polish & Testing

### Day 13: Sound & Audio
- [ ] Add placeholder audio system
- [ ] Integrate sound effects for button clicks
- [ ] Add background music capability
- [ ] Find and add free audio assets

### Day 14: Asset Integration
- [ ] Find and add placeholder art for scenes
- [ ] Create character sprites/portraits
- [ ] Add gemstone images
- [ ] Integrate all visual assets into scenes

### Day 15: Game Balance & Testing
- [ ] Test all game paths and endings
- [ ] Balance difficulty and choice outcomes
- [ ] Fix any logic issues from UI conversion
- [ ] Test different character classes thoroughly

### Day 16: Accessibility & UX
- [ ] Add text size adjustment
- [ ] Implement color contrast for readability
- [ ] Add game instruction tooltips
- [ ] Create a main menu

### Day 17: Additional Features
- [ ] Add restart game functionality
- [ ] Create an options menu
- [ ] Add scene navigation for replayability
- [ ] Implement achievement system (optional)

### Day 18: Documentation & Final Testing
- [ ] Write README with game instructions
- [ ] Test for all possible edge cases
- [ ] Create proper credits for assets used
- [ ] Final playthrough to ensure everything works

## Week 4: Deployment

### Day 19: Packaging
- [ ] Create setup.py or build script
- [ ] Package all assets with the game
- [ ] Create executable for Windows/Linux/Mac (using PyInstaller)

### Day 20: Deployment
- [ ] Test on different systems
- [ ] Create distribution files
- [ ] Add to GitHub or other platform
- [ ] Document deployment process

## Stretch Goals (Optional)
- [ ] Add more complex dialogue trees
- [ ] Implement character relationships
- [ ] Create random events
- [ ] Add multiple difficulty levels
- [ ] Allow other languages/localization
- [ ] Create a map system
- [ ] Add mini-games between story segments
