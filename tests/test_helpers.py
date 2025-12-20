"""
Integration Test Helpers for Knights and Creatures Game
Provides utilities for real game testing with minimal mocking.
"""

import pygame
import time
import sys
import os
from typing import Optional, Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.main_game import KnightsAndCreaturesGame
from ui.scene_manager import SceneManager
from ui.scene import Scene, JSONScene


class GameTestHelper:
    """Helper class for integration testing the actual game."""

    def __init__(self):
        """Initialize the test helper with a real game instance."""
        # Initialize pygame in headless mode for testing
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        # Create game instance
        self.game = None
        self.is_running = False

    def setup_game(self) -> KnightsAndCreaturesGame:
        """Create and set up a game instance for testing."""
        self.game = KnightsAndCreaturesGame()
        return self.game

    def cleanup_game(self):
        """Clean up the game instance after testing."""
        if self.game:
            self.game.scene_manager.quit_game()
            self.game = None
        pygame.quit()

    def start_game(self, initial_scene: str = "start_game") -> bool:
        """Start the game with specified initial scene."""
        if not self.game:
            self.setup_game()

        success = self.game.scene_manager.start_game(initial_scene)
        if success:
            self.is_running = True
        return success

    def get_current_scene_id(self) -> Optional[str]:
        """Get the ID of the currently active scene."""
        if not self.game or not self.game.scene_manager.current_scene:
            return None
        return self.game.scene_manager.current_scene.scene_id

    def get_current_scene(self) -> Optional[Scene]:
        """Get the currently active scene object."""
        if not self.game:
            return None
        return self.game.scene_manager.current_scene

    def get_scene_buttons(self) -> List[str]:
        """Get list of button texts in the current scene."""
        scene = self.get_current_scene()
        if not scene or not hasattr(scene, 'button_group'):
            return []

        button_texts = []
        for button in scene.button_group.buttons:
            button_texts.append(button.text)
        return button_texts

    def click_button(self, button_text: str) -> bool:
        """Simulate clicking a button with the given text."""
        scene = self.get_current_scene()
        if not scene or not hasattr(scene, 'button_group'):
            return False

        # Find button with matching text
        target_button = None
        for button in scene.button_group.buttons:
            if button_text in button.text or button.text == button_text:
                target_button = button
                break

        if not target_button:
            return False

        # Simulate mouse click on the button
        button_center = target_button.rect.center

        # Create and send mouse events
        mouse_down = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            button=1,
            pos=button_center
        )
        mouse_up = pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            button=1,
            pos=button_center
        )

        # Process the events
        handled_down = self.game.scene_manager.handle_event(mouse_down)
        handled_up = self.game.scene_manager.handle_event(mouse_up)

        return handled_up or handled_down

    def send_key_event(self, key: int, mod: int = 0) -> bool:
        """Send a keyboard event to the game."""
        if not self.game:
            return False

        key_event = pygame.event.Event(
            pygame.KEYDOWN,
            key=key,
            mod=mod
        )

        return self.game.scene_manager.handle_event(key_event)

    def wait_for_scene_transition(self, expected_scene: str, timeout: float = 3.0) -> bool:
        """Wait for the scene to transition to the expected scene."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Process any pending pygame events (like timers)
            for event in pygame.event.get():
                self.game.scene_manager.handle_event(event)

            # Update game state
            self.game.update()

            # Check if we've reached the expected scene
            if self.get_current_scene_id() == expected_scene:
                return True

            # Small delay to avoid busy waiting
            time.sleep(0.1)

        return False

    def get_game_data(self, key: str) -> Any:
        """Get data from the game's persistent state."""
        if not self.game:
            return None
        return self.game.scene_manager.get_game_data(key)

    def set_game_data(self, key: str, value: Any):
        """Set data in the game's persistent state."""
        if self.game:
            self.game.scene_manager.set_game_data(key, value)

    def get_scene_data(self, key: str = None) -> Dict[str, Any]:
        """Get scene-specific data (story_text, info_text, etc.)."""
        scene = self.get_current_scene()
        if not scene or not hasattr(scene, 'scene_data'):
            return {}

        if key:
            return scene.scene_data.get(key)
        return scene.scene_data.copy()

    def assert_scene_has_buttons(self, expected_buttons: List[str]) -> bool:
        """Assert that the current scene has buttons with the expected texts."""
        actual_buttons = self.get_scene_buttons()

        for expected in expected_buttons:
            found = False
            for actual in actual_buttons:
                if expected in actual:
                    found = True
                    break
            if not found:
                raise AssertionError(
                    f"Expected button '{expected}' not found. "
                    f"Available buttons: {actual_buttons}"
                )
        return True

    def assert_in_scene(self, expected_scene_id: str):
        """Assert that we're currently in the expected scene."""
        current = self.get_current_scene_id()
        if current != expected_scene_id:
            raise AssertionError(
                f"Expected to be in scene '{expected_scene_id}', "
                f"but currently in '{current}'"
            )

    def assert_story_contains(self, expected_text: str):
        """Assert that the current scene's story text contains the expected text."""
        story_text = self.get_scene_data('story_text')
        if not story_text or expected_text not in story_text:
            raise AssertionError(
                f"Expected story to contain '{expected_text}', "
                f"but got: '{story_text}'"
            )


class GameFlowTester:
    """High-level game flow testing utilities."""

    @staticmethod
    def complete_character_selection(helper: GameTestHelper, character_name: str) -> bool:
        """Complete the character selection flow."""
        # Start game
        if not helper.start_game():
            return False

        # Should be in start_game scene
        helper.assert_in_scene("start_game")

        # Accept the challenge
        if not helper.click_button("Yes, I accept the challenge!"):
            return False

        # Wait for transition to character selection
        if not helper.wait_for_scene_transition("choose_character_class"):
            return False

        # Select the specified character
        if not helper.click_button(character_name):
            return False

        # Wait for transition to next scene
        return helper.wait_for_scene_transition("blue_stone", timeout=5.0)

    @staticmethod
    def play_blue_stone_scenario(helper: GameTestHelper, choices: List[str]) -> bool:
        """Play through the blue stone scenario with given choices."""
        helper.assert_in_scene("blue_stone")

        for choice in choices:
            # Make sure we have buttons available
            buttons = helper.get_scene_buttons()
            if not buttons:
                return False

            # Click the choice
            clicked = False
            for button_text in buttons:
                if choice in button_text:
                    if helper.click_button(button_text):
                        clicked = True
                        break

            if not clicked:
                return False

            # Wait a moment for the choice to process
            time.sleep(0.5)

            # Process any timer events
            for event in pygame.event.get():
                helper.game.scene_manager.handle_event(event)
            helper.game.update()

        return True


def create_test_helper() -> GameTestHelper:
    """Factory function to create a test helper instance."""
    return GameTestHelper()


def run_smoke_test() -> bool:
    """Run a basic smoke test to ensure the game loads and basic functionality works."""
    helper = create_test_helper()

    try:
        # Test game initialization
        helper.setup_game()
        assert helper.game is not None, "Game failed to initialize"

        # Test scene manager
        scene_count = helper.game.scene_manager.get_scene_count()
        assert scene_count > 0, "No scenes loaded"

        # Test starting the game
        success = helper.start_game()
        assert success, "Failed to start game"

        # Test current scene
        current_scene = helper.get_current_scene_id()
        assert current_scene == "start_game", f"Expected start_game, got {current_scene}"

        # Test buttons exist
        buttons = helper.get_scene_buttons()
        assert len(buttons) > 0, "No buttons found in start scene"

        print("✅ Smoke test passed!")
        return True

    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        return False

    finally:
        helper.cleanup_game()


if __name__ == "__main__":
    # Run smoke test when executed directly
    run_smoke_test()
