# Knights and Creatures 🎮⚔️

A point-and-click adventure game built with Python and Pygame. Help Red rescue his magical cat Bartholomew from the evil Skull by collecting three mystical gemstones and opening a portal to the Void Prison.

## 🎯 Project Overview

This project started as a simple console-based text adventure in a single Python file and has been transformed into a full GUI adventure game with proper scene management, JSON-driven content, and comprehensive integration testing.

## ✨ Features

- **Interactive GUI**: Point-and-click interface with mouse and keyboard navigation
- **Character Classes**: Choose from Warrior, Mage, Bard, or Clerk - each with unique abilities
- **Scene Management**: Smooth transitions between game scenes with fade effects
- **JSON-Driven Content**: Story content, choices, and character data managed through JSON files
- **Enhanced Input System**: 
  - Mouse hover effects and click animations
  - Keyboard shortcuts (arrow keys, Tab navigation, number keys for quick selection)
  - Visual feedback for all interactions
- **Game State Management**: Persistent character selection and choice tracking
- **Multi-Chapter Scenarios**: Complex branching storylines with consequences

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Redsskull/Knights-and-Creatues.git
cd Knights-and-Creatues
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python ui/main_game.py
```

### Controls

- **Mouse**: Click buttons to make choices
- **Keyboard**: 
  - Arrow keys or Tab to navigate between options
  - Enter/Space to select highlighted option
  - Number keys (1-9) for quick choice selection
  - F1: Return to start screen
  - F2: Cycle through scenes (debug)
  - ESC: Quit game

## 🧪 Testing Philosophy

This project emphasizes **integration testing over unit testing**. After experiencing the pitfall of 46 passing mock tests while the game was completely broken, we rebuilt the testing approach to focus on real user experience validation.

### Running Tests

```bash
# Run all integration tests
pytest

# Run specific test categories
pytest tests/test_game_integration.py
pytest tests/test_scene_functionality.py

# Run with verbose output
pytest -v
```

### Test Coverage

- **45+ Integration Tests** that validate complete user journeys
- **Real Component Testing** with minimal mocking
- **Scene Transition Validation** using actual pygame events
- **JSON Data Integrity** testing with real game files
- **Input System Testing** with simulated mouse/keyboard events

## 📁 Project Structure

```
Knights-and-Creatues/
├── data/                   # JSON game content files
│   ├── start_game.json
│   ├── character_classes.json
│   └── blue_stone_scenes.json
├── ui/                     # GUI components and game engine
│   ├── main_game.py       # Main game entry point
│   ├── scene_manager.py   # Scene transitions and state
│   ├── scene.py           # Base scene classes
│   ├── button.py          # Interactive button components
│   └── ui_base.py         # UI foundations
├── tests/                  # Integration test suite
├── assets/                 # Game assets (images, sounds)
├── run.py                 # Original console game
└── requirements.txt
```

## 🎮 Current Game Content

### Implemented Scenarios
- ✅ **Game Start**: Accept the quest to rescue Bartholomew
- ✅ **Character Selection**: Choose your class and see abilities
- ✅ **Blue Stone Adventure**: Multi-chapter underwater cave scenario
  - Dolphin encounters with multiple choice outcomes
  - Water elemental negotiations
  - Companion recruitment options

### In Development
- 🔄 **Yellow Stone Adventure**: Desert temple challenges
- 🔄 **Red Stone Adventure**: Volcanic cave exploration
- 🔄 **Final Dungeon**: Void Prison and Bartholomew rescue

## 🛠️ Technical Highlights

- **Scene Management System**: Smooth transitions between game states
- **Event-Driven Architecture**: Clean separation of UI, game logic, and content
- **JSON Content Pipeline**: Non-programmer-friendly story editing
- **Enhanced Button System**: Hover effects, keyboard navigation, visual feedback
- **Integration Testing**: Real user experience validation

## 🤝 Contributing

This is a learning project, but contributions are welcome! Areas where help would be appreciated:

- **Art Assets**: Character sprites, backgrounds, UI elements
- **Sound Design**: Background music and effect sounds
- **Content**: Additional story scenarios and character dialogue
- **Testing**: More edge cases and user journey validation

## 📚 Learning Outcomes

This project demonstrates several important software development concepts:

1. **Testing Strategy Evolution**: From unit mocks to integration reality
2. **Architecture Refactoring**: Console to GUI transformation
3. **Content-Code Separation**: JSON-driven game content
4. **User Experience Focus**: Input systems that feel responsive
5. **State Management**: Persistent game progression

## 🎯 Future Roadmap

- [ ] Complete yellow and red stone adventures
- [ ] Polish UI design with proper artwork
- [ ] Add sound effects and background music  
- [ ] Implement save/load game functionality
- [ ] Create a proper main menu system
- [ ] Package for distribution

## 📜 License

This project is open source and available under the MIT License.

---

*"Sometimes the best projects are the ones that teach you as much about testing as they do about the domain itself."*

**Built with Python 🐍 | Pygame 🎮 | Tested with Pytest ✅**