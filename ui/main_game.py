"""
Main game for Knights and Creatures using scene management system.
Integrates SceneManager with JSON content loading and smooth transitions.
"""

import pygame
import sys
import os

# Add the parent directory to the path so we can import from ui modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.scene_manager import SceneManager
# from ui.demo_scene import DemoScene  # TODO: Create demo scene


class KnightsAndCreaturesGame:
    """Main game class using the scene management system."""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 700
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Knights and Creatures - Adventure Game")

        # Set up clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()

        # Initialize scene manager
        self.scene_manager = SceneManager(self.screen)

        # Set up scenes
        self.setup_scenes()

    def setup_scenes(self):
        """Set up all game scenes."""
        # Set up default JSON-based scenes
        self.scene_manager.setup_default_scenes()

        # TODO: Add demo scene when created
        # demo_scene = DemoScene(self.scene_manager)
        # self.scene_manager.register_scene("demo", demo_scene)

        print("Game scenes set up:")
        for scene_id in self.scene_manager.list_scenes():
            print(f"  - {scene_id}")

    def calculate_delta_time(self):
        """Calculate delta time for smooth animations."""
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_time) / 1000.0  # Convert to seconds
        self.last_time = current_time
        return dt

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            # Let scene manager handle events first
            if self.scene_manager.handle_event(event):
                continue

            # Handle any remaining global events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    # F1 to go to start_game scene
                    self.scene_manager.transition_to("start_game")
                elif event.key == pygame.K_F2:
                    # F2 to cycle through scenes
                    self.cycle_scenes()

    def cycle_scenes(self):
        """Cycle through available scenes for testing."""
        scenes = self.scene_manager.list_scenes()
        if not scenes:
            return

        current_scene_id = None
        if self.scene_manager.current_scene:
            current_scene_id = self.scene_manager.current_scene.scene_id

        try:
            current_index = scenes.index(current_scene_id)
            next_index = (current_index + 1) % len(scenes)
        except (ValueError, TypeError):
            next_index = 0

        next_scene = scenes[next_index]
        print(f"Cycling to scene: {next_scene}")
        self.scene_manager.transition_to(next_scene)

    def update(self):
        """Update game logic."""
        dt = self.calculate_delta_time()
        self.scene_manager.update(dt)

    def render(self):
        """Render the game."""
        self.scene_manager.render()

        # Draw debug info in top-right corner
        self.draw_debug_info()

        # Update display
        pygame.display.flip()

    def draw_debug_info(self):
        """Draw debug information."""
        font = pygame.font.Font(None, 24)

        # Current scene info
        current_scene_text = "No Scene"
        if self.scene_manager.current_scene:
            current_scene_text = f"Scene: {self.scene_manager.current_scene.scene_id}"

        debug_lines = [
            current_scene_text,
            f"Scenes: {self.scene_manager.get_scene_count()}",
            "F1=Demo, F2=Cycle"
        ]

        y_offset = 10
        for line in debug_lines:
            text_surface = font.render(line, True, (100, 100, 100))
            text_rect = text_surface.get_rect()
            text_rect.topright = (self.SCREEN_WIDTH - 10, y_offset)
            self.screen.blit(text_surface, text_rect)
            y_offset += 25

    def run(self):
        """Main game loop."""
        print("Starting Knights and Creatures with Scene Management")
        print(f"Screen size: {self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}")
        print("-" * 50)

        # Start with start_game scene (demo scene not yet implemented)
        if not self.scene_manager.start_game("start_game"):
            print("Failed to start game - trying alternative scenes")
            # Try other available scenes
            scenes = self.scene_manager.list_scenes()
            if scenes:
                if not self.scene_manager.start_game(scenes[0]):
                    print("Critical error: No valid scenes found!")
                    return
            else:
                print("Critical error: No scenes available!")
                return

        print("Game started successfully!")
        print("Controls:")
        print("  F1 - Go to Start Game Scene")
        print("  F2 - Cycle through scenes")
        print("  ESC - Quit game")
        print("  Scene-specific controls shown in each scene")
        print("-" * 50)

        # Main game loop
        while self.scene_manager.is_running():
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        print("Game ended gracefully")


def main():
    """Entry point for the game."""
    try:
        game = KnightsAndCreaturesGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
