"""
Demo scene for testing the scene management system.
Provides interactive examples of scene transitions and JSON loading.
"""

import pygame
from .scene import Scene
from .button import Button


class DemoScene(Scene):
    """A demo scene that showcases scene management features."""

    def __init__(self, scene_manager):
        super().__init__(scene_manager, "demo", "Scene Management Demo")

    def setup_ui(self):
        """Set up the demo scene UI."""
        super().setup_ui()
        self.create_demo_buttons()

    def create_demo_buttons(self):
        """Create buttons for demonstrating scene transitions."""
        button_configs = [
            ("Go to Start Game", "start_game", 50, 460),
            ("Go to Character Select", "character_select", 270, 460),
            ("Go to Blue Stone", "blue_stone", 490, 460),
            ("Transition Test", "transition_test", 50, 510),
            ("Back to Demo", "demo", 270, 510),
            ("Quit Game", "quit", 490, 510)
        ]

        for text, action, x, y in button_configs:
            button = Button(
                self.screen,
                x, y, 200, 35,
                text,
                lambda a=action: self.handle_demo_button(a)
            )
            self.button_group.add_button(button)

    def handle_demo_button(self, action):
        """Handle demo button clicks."""
        if action == "quit":
            self.scene_manager.quit_game()
        elif action == "transition_test":
            self.test_transition_cycle()
        elif action in self.scene_manager.scenes:
            self.transition_to(action)
        else:
            print(f"Unknown action: {action}")

    def test_transition_cycle(self):
        """Test cycling through scenes with transitions."""
        scenes = ["start_game", "character_select", "blue_stone", "demo"]
        current_index = 0
        if hasattr(self, 'cycle_index'):
            current_index = (self.cycle_index + 1) % len(scenes)

        self.cycle_index = current_index
        next_scene = scenes[current_index]

        print(f"Cycling to scene: {next_scene}")
        self.transition_to(next_scene)

    def load_content(self):
        """Load demo content."""
        self.scene_data = {
            'story_text': """Welcome to the Scene Management Demo!

This demo showcases the scene system we've built for Knights and Creatures. You can:

• Navigate between different scenes using the buttons below
• Test JSON content loading from your game files
• Experience smooth scene transitions
• See how the scene management system handles different content types

The scenes available are:
- Start Game: Shows the intro story from start_game.json
- Character Select: Displays character classes from character_classes.json
- Blue Stone: Shows the first chapter of the blue stone adventure

Try clicking the buttons to explore the different scenes!""",

            'info_text': """Scene System Features:

✓ Base Scene class
✓ JSONScene for loading content
✓ SceneManager for transitions
✓ Button-based navigation
✓ Fade transitions
✓ Game state management

Current Scene: Demo
Total Scenes: """ + str(self.scene_manager.get_scene_count()) + """

Available Scenes:
""" + "\n".join(f"• {scene_id}" for scene_id in self.scene_manager.list_scenes())
        }

    def on_key_press(self, key):
        """Handle key presses in demo scene."""
        if key == pygame.K_1:
            self.transition_to("start_game")
            return True
        elif key == pygame.K_2:
            self.transition_to("character_select")
            return True
        elif key == pygame.K_3:
            self.transition_to("blue_stone")
            return True
        elif key == pygame.K_SPACE:
            self.test_transition_cycle()
            return True

        return super().on_key_press(key)

    def render(self):
        """Render the demo scene with additional instructions."""
        super().render()

        # Add keyboard shortcuts info
        shortcuts_text = "Shortcuts: 1=Start Game, 2=Character Select, 3=Blue Stone, SPACE=Cycle, ESC=Quit"
        self.ui_base.render_text(
            shortcuts_text,
            50,
            self.screen.get_height() - 25,
            color=(120, 120, 120),
            max_width=self.screen.get_width() - 100
        )
