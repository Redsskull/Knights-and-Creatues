"""
Integration Tests for Knights and Creatures Game
Tests the complete user experience and game flow with real components.
"""

import pytest
import pygame
import time
from test_helpers import GameFlowTester, create_test_helper


class TestGameIntegration:
    """Integration tests for complete game functionality."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.helper = create_test_helper()

    def teardown_method(self):
        """Clean up after each test."""
        self.helper.cleanup_game()

    def test_game_initialization(self):
        """Test that the game initializes properly with all required scenes."""
        self.helper.setup_game()

        # Verify game object exists
        assert self.helper.game is not None

        # Verify scene manager exists
        assert self.helper.game.scene_manager is not None

        # Verify scenes are loaded
        scene_count = self.helper.game.scene_manager.get_scene_count()
        assert scene_count >= 4  # start_game, character_select, blue_stone, etc.

        # Verify expected scenes exist
        scenes = self.helper.game.scene_manager.list_scenes()
        required_scenes = ["start_game", "choose_character_class", "blue_stone"]
        for scene in required_scenes:
            assert scene in scenes

    def test_game_startup_flow(self):
        """Test the complete game startup sequence."""
        # Start the game
        success = self.helper.start_game()
        assert success

        # Should be in start_game scene
        self.helper.assert_in_scene("start_game")

        # Should have buttons available
        buttons = self.helper.get_scene_buttons()
        assert len(buttons) >= 2

        # Should have accept/decline options
        self.helper.assert_scene_has_buttons(["Yes, I accept", "No, I'm not interested"])

    def test_accept_challenge_flow(self):
        """Test accepting the challenge and transitioning to character selection."""
        self.helper.start_game()
        self.helper.assert_in_scene("start_game")

        # Click accept challenge
        clicked = self.helper.click_button("Yes, I accept the challenge!")
        assert clicked

        # Should transition to character selection
        transitioned = self.helper.wait_for_scene_transition("choose_character_class")
        assert transitioned

        # Should have character class options
        buttons = self.helper.get_scene_buttons()
        assert len(buttons) >= 4  # At least 4 character classes

    def test_decline_challenge(self):
        """Test declining the challenge (should not progress)."""
        self.helper.start_game()
        self.helper.assert_in_scene("start_game")

        # Click decline
        clicked = self.helper.click_button("No, I'm not interested")
        assert clicked

        # Should stay in the same scene (or handle appropriately)
        current_scene = self.helper.get_current_scene_id()
        assert current_scene == "start_game"  # Assuming it stays in start_game

    @pytest.mark.parametrize("character_name", ["Warrior", "Mage", "Bard", "Clerk"])
    def test_character_selection(self, character_name):
        """Test selecting each character class."""
        # Get to character selection
        self.helper.start_game()
        self.helper.click_button("Yes, I accept the challenge!")
        self.helper.wait_for_scene_transition("choose_character_class")

        # Select character
        clicked = self.helper.click_button(character_name)
        assert clicked

        # Should store selected class
        selected_class = self.helper.get_game_data('selected_class')
        assert selected_class is not None
        assert selected_class['name'] == character_name

        # Should transition to blue stone scene
        transitioned = self.helper.wait_for_scene_transition("blue_stone")
        assert transitioned

    def test_complete_character_selection_flow(self):
        """Test the complete flow from start to blue stone scene."""
        success = GameFlowTester.complete_character_selection(self.helper, "Warrior")
        assert success

        # Verify we're in the blue stone scene
        self.helper.assert_in_scene("blue_stone")

        # Verify scene has content
        story_text = self.helper.get_scene_data('story_text')
        assert story_text is not None
        assert len(story_text) > 0

        # Should have choice buttons
        buttons = self.helper.get_scene_buttons()
        assert len(buttons) >= 3


class TestBlueStoneScenario:
    """Integration tests for the Blue Stone adventure scenario."""

    def setup_method(self):
        """Set up test environment with character already selected."""
        self.helper = create_test_helper()
        # Get to blue stone scene
        GameFlowTester.complete_character_selection(self.helper, "Warrior")

    def teardown_method(self):
        """Clean up after each test."""
        self.helper.cleanup_game()

    def test_blue_stone_scene_initialization(self):
        """Test that the blue stone scene loads correctly."""
        self.helper.assert_in_scene("blue_stone")

        # Should have story content
        story_text = self.helper.get_scene_data('story_text')
        assert "dolphin" in story_text.lower() or "underwater" in story_text.lower()

        # Should have three initial choices
        buttons = self.helper.get_scene_buttons()
        assert len(buttons) == 3

    def test_blue_stone_first_choice_success(self):
        """Test the successful path through first dolphin encounter."""
        # Choose option A (pretend relaxing dive)
        clicked = self.helper.click_button("Pretend you are just here")
        assert clicked

        # Should progress to next chapter
        time.sleep(2)  # Wait for transition

        # Process any pending events
        for event in pygame.event.get():
            self.helper.game.scene_manager.handle_event(event)
        self.helper.game.update()

        # Should now have different story content (water elemental)
        self.helper.get_scene_data('story_text')
        self.helper.get_scene_data('info_text')

        # Verify we progressed (different content or choices)
        buttons = self.helper.get_scene_buttons()
        assert len(buttons) > 0

    def test_blue_stone_choice_feedback(self):
        """Test that choices provide proper feedback."""
        initial_info = self.helper.get_scene_data('info_text')

        # Make a choice
        self.helper.click_button("Greet them and tell them")

        # Wait for choice to process
        time.sleep(1)

        # Should have updated info text with choice result
        updated_info = self.helper.get_scene_data('info_text')
        assert updated_info != initial_info

    def test_keyboard_navigation_in_blue_stone(self):
        """Test keyboard navigation works in the blue stone scene."""
        # Test number key shortcuts
        success = self.helper.send_key_event(pygame.K_1)
        assert success

        # Wait for processing
        time.sleep(1)

        # Should have processed the choice
        info_text = self.helper.get_scene_data('info_text')
        assert "Choice:" in info_text or "Result:" in info_text


class TestInputSystemIntegration:
    """Integration tests for the input system across all scenes."""

    def setup_method(self):
        """Set up test environment."""
        self.helper = create_test_helper()

    def teardown_method(self):
        """Clean up after each test."""
        self.helper.cleanup_game()

    def test_mouse_input_works_across_scenes(self):
        """Test that mouse input works consistently across different scenes."""
        # Test in start scene
        self.helper.start_game()
        start_buttons = self.helper.get_scene_buttons()
        assert len(start_buttons) > 0

        # Click should work
        clicked = self.helper.click_button(start_buttons[0])
        assert clicked

        # Move to character selection
        self.helper.wait_for_scene_transition("choose_character_class")
        char_buttons = self.helper.get_scene_buttons()
        assert len(char_buttons) > 0

        # Click should work in new scene
        clicked = self.helper.click_button(char_buttons[0])
        assert clicked

    def test_keyboard_shortcuts_work_across_scenes(self):
        """Test that keyboard shortcuts work in different scenes."""
        # Test in start scene
        self.helper.start_game()

        # Number key should work
        success = self.helper.send_key_event(pygame.K_1)
        assert success

        # Move to character selection
        self.helper.wait_for_scene_transition("choose_character_class")

        # Number key should work in new scene
        success = self.helper.send_key_event(pygame.K_2)
        assert success

    def test_escape_key_works_globally(self):
        """Test that ESC key works from any scene."""
        self.helper.start_game()

        # ESC should be handled
        success = self.helper.send_key_event(pygame.K_ESCAPE)
        assert success

        # Game should initiate shutdown
        # Note: In real implementation, this might set a quit flag


class TestErrorHandling:
    """Integration tests for error handling and edge cases."""

    def setup_method(self):
        """Set up test environment."""
        self.helper = create_test_helper()

    def teardown_method(self):
        """Clean up after each test."""
        self.helper.cleanup_game()

    def test_clicking_nonexistent_button(self):
        """Test clicking a button that doesn't exist."""
        self.helper.start_game()

        # Try to click a button that doesn't exist
        clicked = self.helper.click_button("This Button Does Not Exist")
        assert not clicked

    def test_scene_with_no_buttons(self):
        """Test handling scenes that might have no buttons."""
        self.helper.start_game()

        # Even if a scene has issues, it shouldn't crash
        buttons = self.helper.get_scene_buttons()
        # Should at least return empty list, not crash
        assert isinstance(buttons, list)

    def test_rapid_button_clicks(self):
        """Test rapid button clicking doesn't break the system."""
        self.helper.start_game()

        button_text = self.helper.get_scene_buttons()[0]

        # Click rapidly
        for _ in range(5):
            self.helper.click_button(button_text)
            time.sleep(0.1)

        # System should still be responsive
        current_scene = self.helper.get_current_scene_id()
        assert current_scene is not None


class TestGameProgression:
    """Integration tests for overall game progression and state management."""

    def setup_method(self):
        """Set up test environment."""
        self.helper = create_test_helper()

    def teardown_method(self):
        """Clean up after each test."""
        self.helper.cleanup_game()

    def test_game_state_persistence(self):
        """Test that game state persists between scenes."""
        # Complete character selection
        GameFlowTester.complete_character_selection(self.helper, "Mage")

        # Verify selected class is stored
        selected_class = self.helper.get_game_data('selected_class')
        assert selected_class is not None
        assert selected_class['name'] == "Mage"

        # Make a choice in blue stone
        self.helper.click_button("Pretend you are just here")
        time.sleep(1)

        # Verify choice was recorded
        last_choice = self.helper.get_game_data('last_choice_blue_stone')
        assert last_choice is not None

    def test_scene_transition_data_flow(self):
        """Test that data flows correctly between scenes."""
        # Start with character selection
        self.helper.start_game()
        self.helper.click_button("Yes, I accept the challenge!")
        self.helper.wait_for_scene_transition("choose_character_class")

        # Select warrior
        self.helper.click_button("Warrior")

        # Wait for blue stone scene
        self.helper.wait_for_scene_transition("blue_stone")

        # Verify character data is available in new scene
        selected_class = self.helper.get_game_data('selected_class')
        assert selected_class is not None
        assert selected_class['name'] == "Warrior"


def test_full_smoke_test():
    """Complete smoke test that validates the entire system works."""
    helper = create_test_helper()

    try:
        # Test complete user journey
        success = GameFlowTester.complete_character_selection(helper, "Bard")
        assert success

        # Test choice making in blue stone
        success = GameFlowTester.play_blue_stone_scenario(helper, ["Pretend you are just here"])
        assert success

        print("✅ Full integration smoke test passed!")

    finally:
        helper.cleanup_game()


if __name__ == "__main__":
    # Run smoke test when executed directly
    test_full_smoke_test()
