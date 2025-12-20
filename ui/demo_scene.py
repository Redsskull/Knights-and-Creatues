"""
Demo scene for testing the enhanced input system functionality.
Demonstrates button interactions, keyboard navigation, hover effects, and scene transitions.
"""

from .scene import Scene



class DemoScene(Scene):
    """Demo scene showcasing the enhanced input system capabilities."""

    def __init__(self, scene_manager):
        super().__init__(scene_manager, "demo", "Input System Demo")
        self.demo_state = "main"
        self.button_click_count = 0
        self.last_key
