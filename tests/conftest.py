"""
Pytest configuration for Knights and Creatures UI tests.
Sets up common fixtures and pygame initialization.
"""

import pytest
import pygame
import sys
import os
from unittest.mock import Mock

# Add the parent directory to the path so we can import from ui modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def pygame_init():
    """Initialize pygame once for the entire test session."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def screen(pygame_init):
    """Create a test screen surface."""
    return pygame.display.set_mode((800, 600))


@pytest.fixture
def mock_scene_manager(screen):
    """Create a mock scene manager for testing."""
    mock_manager = Mock()
    mock_manager.screen = screen
    mock_manager.json_loader = Mock()
    mock_manager.set_game_data = Mock()
    mock_manager.transition_to = Mock()
    mock_manager.quit_game = Mock()
    return mock_manager


@pytest.fixture
def sample_json_content():
    """Sample JSON content for testing scenes."""
    return {
        "title": "Test Scene",
        "story_text": "This is a test story.",
        "description": "Test description",
        "choices": [
            {
                "id": "choice1",
                "text": "First choice",
                "outcome": {
                    "message": "You chose first",
                    "next_scene": "next_scene"
                }
            },
            {
                "id": "choice2",
                "text": "Second choice",
                "outcome": {
                    "message": "You chose second",
                    "success": True
                }
            }
        ]
    }


@pytest.fixture
def sample_character_classes():
    """Sample character classes for testing."""
    return {
        "classes": [
            {
                "name": "Warrior",
                "description": "A brave fighter",
                "abilities": [{"name": "Heroic Strike", "description": "Deal extra damage"}],
                "attributes": {"strength": 10, "magic": 2, "charisma": 5}
            },
            {
                "name": "Mage",
                "description": "A wise spellcaster",
                "abilities": [{"name": "Fireball", "description": "Cast magic missile"}],
                "attributes": {"strength": 3, "magic": 10, "charisma": 4}
            }
        ]
    }
