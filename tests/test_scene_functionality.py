"""
Scene-Specific Integration Tests for Knights and Creatures Game
Tests individual scene functionality with real components and JSON data.
"""

import pytest
import pygame
import time
from test_helpers import create_test_helper


class TestStartGameScene:
    """Integration tests for the start game scene."""

    def setup_method(self):
        """Set up test environment."""
        self.helper = create_test_helper()
        self.helper.start_game("start_game")

    def teardown_method(self):
        """Clean up after each test."""
        self.helper.cleanup_game()

    def test_start_scene_loads_correctly(self):
        """Test that start scene loads with correct content."""
        self.helper.assert_in_scene("start_game")

        # Should have story content about Bartholomew
        story_text = self.helper.get_scene_data('story_text')
        assert "Bartholomew" in story_text
        assert "gemstones" in story_text
        assert "Skull" in story_text

    def test_start_scene_has_correct_choices(self):
        """Test that start scene has yes/no choices."""
        buttons = self.helper.get_scene_buttons()

        # Should have exactly 2 buttons
        assert len(buttons) == 2

        # Should have accept and decline options
        self.helper.assert_scene_has_buttons([
            "Yes, I accept the challenge!",
            "No, I'm not interested"
        ])

    def test_accepting_challenge_transitions_correctly(self):
        """Test that accepting challenge leads to character selection."""
        # Click yes
        clicked = self.helper.click_button("Yes, I accept the challenge!")
        assert clicked

        # Should transition to character selection
        transitioned = self.helper.wait_for_scene_transition("choose_character_class", timeout=3.0)
        assert transitioned

        # Verify we're in the right scene
        self.helper.assert_in_scene("choose_character_class")

    def test_declining_challenge_stays_in_scene(self):
        """Test that declining challenge keeps you in start scene."""
        initial_scene = self.helper.get_current_scene_id()

        # Click no
        clicked = self.helper.click_button("No, I'm not interested")
        assert clicked

        # Should stay in same scene
        time.sleep(1)
        current_scene = self.helper.get_current_scene_id()
        assert current_scene == initial_scene

    def test_keyboard_shortcuts_work(self):
        """Test number key shortcuts work in start scene."""
        # Press 1 for first choice (Yes)
        success = self.helper.send_key_event(pygame.K_1)
        assert success

        # Should trigger transition
        transitioned = self.helper.wait_for_scene_transition("choose_character_class", timeout=3.0)
        assert transitioned


class TestCharacterSelectionScene:
    """Integration tests for the character selection scene."""

    def setup_method(self):
        """Set up test environment at character selection."""
        self.helper = create_test_helper()
        self.helper.start_game("start_game")
        self.helper.click_button("Yes, I accept the challenge!")
        self.helper.wait_for_scene_transition("choose_character_class")

    def teardown_method(self):
        """Clean up after each test."""
        self.helper.cleanup_game()

    def test_character_scene_loads_correctly(self):
        """Test that character selection scene loads properly."""
        self.helper.assert_in_scene("choose_character_class")

        # Should have character information
        story_text = self.helper.get_scene_data('story_text')
        assert len(story_text) > 0

        # Should mention character class
        assert "Class:" in story_text or "Warrior" in story_text

    def test_has_all_character_classes(self):
        """Test that all expected character classes are available."""
        buttons = self.helper.get_scene_buttons()

        # Should have 4 character classes
        assert len(buttons) == 4

        # Should have all expected classes
        expected_classes = ["Warrior", "Mage", "Bard", "Clerk"]
        for class_name in expected_classes:
            self.helper.assert_scene_has_buttons([class_name])

    @pytest.mark.parametrize("class_name,expected_attribute", [
        ("Warrior", "strength"),
        ("Mage", "magic"),
        ("Bard", "charisma"),
        ("Clerk", "charisma")
    ])
    def test_character_selection_shows_attributes(self, class_name, expected_attribute):
        """Test that selecting a character shows their attributes."""
        # Select character
        clicked = self.helper.click_button(class_name)
        assert clicked

        # Should update info text with character details
        time.sleep(1)
        info_text = self.helper.get_scene_data('info_text')

        # Should show the character's key attribute
        assert expected_attribute.title() in info_text or expected_attribute in info_text

    def test_character_selection_stores_data(self):
        """Test that character selection stores the chosen class."""
        # Select Mage
        clicked = self.helper.click_button("Mage")
        assert clicked

        # Should store selected class
        selected_class = self.helper.get_game_data('selected_class')
        assert selected_class is not None
        assert selected_class['name'] == "Mage"

    def test_character_selection_transitions_to_adventure(self):
        """Test that selecting a character transitions to the adventure."""
        # Select any character
        clicked = self.helper.click_button("Warrior")
        assert clicked

        # Should transition to blue stone scene
        transitioned = self.helper.wait_for_scene_transition("blue_stone", timeout=5.0)
        assert transitioned

        self.helper.assert_in_scene("blue_stone")


class TestBlueStoneScene:
    """Integration tests for the Blue Stone adventure scene."""

    def setup_method(self):
        """Set up test environment at blue stone scene."""
        self.helper = create_test_helper()
        # Get to blue stone scene quickly
        self.helper.start_game("start_game")
        self.helper.click_button("Yes, I accept the challenge!")
        self.helper.wait_for_scene_transition("choose_character_class")
        self.helper.click_button("Warrior")
        self.helper.wait_for_scene_transition("blue_stone")

    def teardown_method(self):
        """Clean up after each test."""
        self.helper.cleanup_game()

    def test_blue_stone_scene_loads_correctly(self):
        """Test that blue stone scene loads with correct content."""
        self.helper.assert_in_scene("blue_stone")

        # Should have underwater/dolphin story content
        story_text = self.helper.get_scene_data('story_text')
        assert "underwater" in story_text.lower() or "dolphins" in story_text.lower()

    def test_blue_stone_has_three_initial_choices(self):
        """Test that blue stone scene has the expected choices."""
        buttons = self.helper.get_scene_buttons()

        # Should have 3 initial choices
        assert len(buttons) == 3

        # Should have dolphin encounter choices
        button_texts = ' '.join(buttons)
        assert "dive" in button_texts.lower() or "greet" in button_texts.lower()

    def test_blue_stone_choice_provides_feedback(self):
        """Test that making choices provides proper feedback."""
        initial_info = self.helper.get_scene_data('info_text')

        # Make first choice
        buttons = self.helper.get_scene_buttons()
        clicked = self.helper.click_button(buttons[0])
        assert clicked

        # Should update info text with result
        time.sleep(1.5)  # Wait for choice processing

        # Process any pending events
        for event in pygame.event.get():
            self.helper.game.scene_manager.handle_event(event)
        self.helper.game.update()

        updated_info = self.helper.get_scene_data('info_text')
        assert updated_info != initial_info

    def test_successful_choice_progresses_story(self):
        """Test that successful choices progress the story."""
        # Make the successful first choice (option A - pretend relaxing dive)
        clicked = self.helper.click_button("Pretend you are just here")
        assert clicked

        # Wait for story progression
        time.sleep(2)

        # Process pending events
        for event in pygame.event.get():
            self.helper.game.scene_manager.handle_event(event)
        self.helper.game.update()

        # Story should have progressed (different content or new choices)
        buttons = self.helper.get_scene_buttons()
        info_text = self.helper.get_scene_data('info_text')

        # Should have some indication of progression
        assert len(buttons) > 0 or "Result:" in info_text

    def test_blue_stone_choice_recording(self):
        """Test that choices are recorded in game data."""
        # Make a choice
        self.helper.click_button("Greet them and tell them")

        # Wait for processing
        time.sleep(1)

        # Choice should be recorded
        last_choice = self.helper.get_game_data('last_choice_blue_stone')
        assert last_choice is not None

    def test_multiple_choice_sequence(self):
        """Test making multiple choices in sequence."""
        # Make first choice (successful path)
        clicked1 = self.helper.click_button("Pretend you are just here")
        assert clicked1

        # Wait for progression
        time.sleep(2)

        # Process events
        for event in pygame.event.get():
            self.helper.game.scene_manager.handle_event(event)
        self.helper.game.update()

        # Should have new buttons available
        buttons = self.helper.get_scene_buttons()
        if len(buttons) > 0:
            # Make second choice if available
            clicked2 = self.helper.click_button(buttons[0])
            assert clicked2


class TestSceneDataIntegrity:
    """Integration tests for scene data loading and integrity."""

    def setup_method(self):
        """Set up test environment."""
        self.helper = create_test_helper()

    def teardown_method(self):
        """Clean up after each test."""
        self.helper.cleanup_game()

    def test_all_scenes_load_without_errors(self):
        """Test that all registered scenes can be loaded without errors."""
        self.helper.setup_game()

        scenes = self.helper.game.scene_manager.list_scenes()

        for scene_id in scenes:
            # Try to transition to each scene
            success = self.helper.game.scene_manager.start_game(scene_id)
            assert success, f"Failed to load scene: {scene_id}"

            # Verify scene loaded
            current = self.helper.get_current_scene_id()
            assert current == scene_id

            # Verify scene has basic data
            scene_data = self.helper.get_scene_data()
            assert isinstance(scene_data, dict)

    def test_scene_json_data_integrity(self):
        """Test that scenes load their JSON data correctly."""
        # Test start_game scene
        self.helper.start_game("start_game")
        story = self.helper.get_scene_data('story_text')
        assert "Bartholomew" in story

        # Test character selection scene
        self.helper.game.scene_manager.start_game("choose_character_class")
        story = self.helper.get_scene_data('story_text')
        assert len(story) > 0

    def test_scene_button_consistency(self):
        """Test that scene buttons are consistent with JSON data."""
        # Test start scene
        self.helper.start_game("start_game")
        buttons = self.helper.get_scene_buttons()
        assert len(buttons) == 2  # Should match JSON choices

        # Test character scene
        self.helper.game.scene_manager.start_game("choose_character_class")
        buttons = self.helper.get_scene_buttons()
        assert len(buttons) == 4  # Should match 4 character classes

    def test_scene_transitions_preserve_data(self):
        """Test that scene transitions don't lose important data."""
        # Start and select character
        self.helper.start_game("start_game")
        self.helper.click_button("Yes, I accept the challenge!")
        self.helper.wait_for_scene_transition("choose_character_class")
        self.helper.click_button("Mage")

        # Store some test data
        self.helper.set_game_data("test_key", "test_value")

        # Transition to next scene
        self.helper.wait_for_scene_transition("blue_stone")

        # Data should still be there
        test_value = self.helper.get_game_data("test_key")
        assert test_value == "test_value"

        # Character selection should also be preserved
        selected_class = self.helper.get_game_data('selected_class')
        assert selected_class['name'] == "Mage"


if __name__ == "__main__":
    # Run a quick test when executed directly
    helper = create_test_helper()
    try:
        helper.start_game("start_game")
        print("✅ Start scene loads correctly")

        buttons = helper.get_scene_buttons()
        print(f"✅ Found {len(buttons)} buttons: {buttons}")

        helper.click_button("Yes, I accept the challenge!")
        if helper.wait_for_scene_transition("choose_character_class"):
            print("✅ Scene transition works")

        print("✅ Scene functionality tests ready to run!")

    finally:
        helper.cleanup_game()
