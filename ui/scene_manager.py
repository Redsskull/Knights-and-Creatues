"""
Scene Manager for Knights and Creatures game.
Handles scene transitions, management, and game state.
"""

import pygame
from .scene import JSONScene
from .json_loader import JSONContentLoader


class SceneManager:
    """Manages game scenes and handles transitions between them."""

    def __init__(self, screen):
        # screen: pygame.Surface
        self.screen = screen
        self.json_loader = JSONContentLoader("data")

        # Scene management
        self.scenes = {}
        self.current_scene = None
        self.previous_scene = None

        # Transition state
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_speed = 5
        self.transition_target = None
        self.transition_data = None

        # Game state
        self.running = True
        self.game_data = {}

    def register_scene(self, scene_id, scene):
        """
        Register a scene with the manager.

        Args:
            scene_id: unique identifier for the scene (str)
            scene: Scene instance to register
        """
        self.scenes[scene_id] = scene

    def create_json_scene(self, scene_id, json_file, title=None):
        """
        Create and register a scene that loads from JSON.

        Args:
            scene_id: unique identifier for the scene (str)
            json_file: JSON file to load content from (str)
            title: optional title for the scene (str)
        """
        scene = JSONScene(self, scene_id, json_file, title)
        self.register_scene(scene_id, scene)
        return scene

    def get_scene(self, scene_id):
        """
        Get a scene by its ID.

        Args:
            scene_id: ID of scene to retrieve (str)

        Returns:
            Scene instance or None if not found
        """
        return self.scenes.get(scene_id)

    def transition_to(self, scene_id, data=None, use_transition=True):
        """
        Transition to a new scene.

        Args:
            scene_id: ID of scene to transition to (str)
            data: optional data to pass to the new scene (dict)
            use_transition: whether to use fade transition (bool)
        """
        if scene_id not in self.scenes:
            print(f"Warning: Scene '{scene_id}' not found!")
            return False

        if use_transition:
            self.start_transition(scene_id, data)
        else:
            self.change_scene_immediately(scene_id, data)

        return True

    def start_transition(self, target_scene_id, data=None):
        """
        Start a fade transition to a new scene.

        Args:
            target_scene_id: ID of scene to transition to (str)
            data: optional data to pass to new scene (dict)
        """
        self.transitioning = True
        self.transition_alpha = 0
        self.transition_target = target_scene_id
        self.transition_data = data

    def change_scene_immediately(self, scene_id, data=None):
        """
        Change scene immediately without transition.

        Args:
            scene_id: ID of scene to change to (str)
            data: optional data to pass to new scene (dict)
        """
        # Exit current scene
        if self.current_scene:
            self.current_scene.exit()
            self.previous_scene = self.current_scene

        # Enter new scene
        new_scene = self.scenes[scene_id]
        if data:
            new_scene.set_scene_data(data)

        new_scene.enter()
        self.current_scene = new_scene

        print(f"Changed to scene: {scene_id}")

    def update_transition(self, dt):
        """
        Update transition animation.

        Args:
            dt: delta time since last update (float)
        """
        if not self.transitioning:
            return

        self.transition_alpha += self.transition_speed * dt * 60  # 60 FPS base

        if self.transition_alpha >= 255:
            # Transition halfway point - change scene
            if self.transition_target:
                self.change_scene_immediately(self.transition_target, self.transition_data)
                self.transition_target = None
                self.transition_data = None

        elif self.transition_alpha >= 510:  # Full fade out and in
            # Transition complete
            self.transitioning = False
            self.transition_alpha = 0

    def handle_event(self, event):
        """
        Handle pygame events.

        Args:
            event: pygame event to handle

        Returns:
            True if event was handled (bool)
        """
        # Global events
        if event.type == pygame.QUIT:
            self.quit_game()
            return True

        # Pass to current scene
        if self.current_scene and not self.transitioning:
            return self.current_scene.handle_event(event)

        return False

    def update(self, dt):
        """
        Update the scene manager.

        Args:
            dt: delta time since last update (float)
        """
        # Update transition
        if self.transitioning:
            self.update_transition(dt)

        # Update current scene
        if self.current_scene and not self.transitioning:
            self.current_scene.update(dt)

    def render(self):
        """Render the current scene and any transition effects."""
        # Render current scene
        if self.current_scene:
            self.current_scene.render()

        # Render transition overlay
        if self.transitioning:
            self.render_transition_overlay()

    def render_transition_overlay(self):
        """Render fade transition overlay."""
        if self.transition_alpha <= 0:
            return

        # Create fade overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))  # Black fade

        # Calculate alpha (fade out then in)
        if self.transition_alpha <= 255:
            alpha = min(255, self.transition_alpha)
        else:
            alpha = max(0, 510 - self.transition_alpha)

        overlay.set_alpha(alpha)
        self.screen.blit(overlay, (0, 0))

    def setup_default_scenes(self):
        """Set up the default game scenes from JSON files."""
        # Create scenes based on available JSON files
        scene_configs = [
            ("blue_stone", "blue_stone_scenes.json", "The Blue Stone Adventure"),
            ("choose_character_class", "character_classes.json", "Choose Your Character"),
            ("character_select", "character_classes.json", "Choose Your Character"),  # Alias for compatibility
            ("start_game", "start_game.json", "Begin Your Quest"),
            ("main_menu", "start_game.json", "Main Menu")  # Reuse start_game for demo
        ]

        for scene_id, json_file, title in scene_configs:
            self.create_json_scene(scene_id, json_file, title)

        print(f"Set up {len(scene_configs)} default scenes")

    def start_game(self, initial_scene="start_game"):
        """
        Start the game with the specified initial scene.

        Args:
            initial_scene: ID of scene to start with (str)
        """
        if initial_scene not in self.scenes:
            print(f"Error: Initial scene '{initial_scene}' not found!")
            return False

        self.change_scene_immediately(initial_scene)
        return True

    def quit_game(self):
        """Quit the game."""
        print("Quitting game...")
        self.running = False

    def is_running(self):
        """
        Check if the game is still running.

        Returns:
            True if game should continue running (bool)
        """
        return self.running

    def get_game_data(self, key, default=None):
        """
        Get game data value.

        Args:
            key: data key to retrieve (str)
            default: default value if key not found

        Returns:
            Value from game data or default
        """
        return self.game_data.get(key, default)

    def set_game_data(self, key, value):
        """
        Set game data value.

        Args:
            key: data key to set (str)
            value: value to set
        """
        self.game_data[key] = value

    def get_scene_count(self):
        """
        Get number of registered scenes.

        Returns:
            Number of scenes (int)
        """
        return len(self.scenes)

    def list_scenes(self):
        """
        Get list of all scene IDs.

        Returns:
            List of scene IDs
        """
        return list(self.scenes.keys())
