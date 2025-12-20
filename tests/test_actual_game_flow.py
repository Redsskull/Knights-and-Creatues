"""
Integration test to validate actual game flow and scene transitions.
This test validates that the game actually works as expected, not just the mocked behavior.
"""

import pytest
import pygame
import sys
import os
from unittest.mock import patch

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.main_game import KnightsAndCreaturesGame
from ui.scene_manager import SceneManager
from ui.scene import JSONScene


class TestActualGameFlow:
    """Test actual game flow without excessive mocking."""

    def test_scene_manager_real_setup(self, pygame_init):
        """Test that scene manager actually sets up scenes correctly."""
        screen = pygame.Surface((800, 600))
        manager = SceneManager(screen)
        manager.setup_default_scenes()

        # Verify all expected scenes exist
        scenes = manager.list_scenes()
        expected_scenes = ['blue_stone', 'choose_character_class', 'character_select', 'start_game', 'main_menu']

        for expected in expected_scenes:
            assert expected in scenes, f"Expected scene '{expected}' not found in {scenes}"

    def test_start_game_scene_buttons(self, pygame_init):
        """Test that start_game scene creates functional buttons."""
        screen = pygame.Surface((800, 600))
        manager = SceneManager(screen)

        # Create and initialize start_game scene
        scene = JSONScene(manager, 'start_game', 'start_game.json')
        scene.initialize()

        # Should have buttons for choices
        button_count = scene.button_group.get_button_count()
        assert button_count > 0, "Start game scene should have choice buttons"

        # Should have scene data
        assert 'story_text' in scene.scene_data
        assert 'info_text' in scene.scene_data

        # Story text should contain the game intro
        story = scene.scene_data.get('story_text', '')
        assert 'Bartholomew' in story, "Story should mention Bartholomew"

    def test_character_selection_scene_buttons(self, pygame_init):
        """Test that character selection scene creates class buttons."""
        screen = pygame.Surface((800, 600))
        manager = SceneManager(screen)

        # Create and initialize character selection scene
        scene = JSONScene(manager, 'choose_character_class', 'character_classes.json')
        scene.initialize()

        # Should have 4 class buttons
        button_count = scene.button_group.get_button_count()
        assert button_count == 4, f"Expected 4 class buttons, got {button_count}"

        # Should have scene data
        assert 'story_text' in scene.scene_data
        assert 'info_text' in scene.scene_data

        # Info should mention available classes
        info = scene.scene_data.get('info_text', '')
        assert 'Available Classes: 4' in info, f"Expected class count info, got: {info}"

    def test_button_keyboard_navigation_real(self, pygame_init):
        """Test that button keyboard navigation actually works."""
        screen = pygame.Surface((800, 600))
        manager = SceneManager(screen)

        scene = JSONScene(manager, 'choose_character_class', 'character_classes.json')
        scene.initialize()
        scene.enter()

        button_group = scene.button_group

        # Should have a selected button initially
        selected = button_group.get_selected_button()
        assert selected is not None, "Should have an initially selected button"
        assert button_group.selected_index == 0, "First button should be selected initially"

        # Test navigation
        button_group.select_next()
        assert button_group.selected_index == 1, "Should move to second button"

        button_group.select_previous()
        assert button_group.selected_index == 0, "Should move back to first button"

    def test_scene_transition_trigger(self, pygame_init):
        """Test that scene transitions are properly triggered."""
        screen = pygame.Surface((800, 600))
        manager = SceneManager(screen)

        # Mock the transition_to method to track calls
        original_transition = manager.transition_to
        transition_calls = []
        def mock_transition(scene_id, data=None):
            transition_calls.append((scene_id, data))
            return True
        manager.transition_to = mock_transition

        # Create start_game scene
        scene = JSONScene(manager, 'start_game', 'start_game.json')
        scene.initialize()
        scene.enter()

        # Get
