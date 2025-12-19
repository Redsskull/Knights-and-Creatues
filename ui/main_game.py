"""
Main game UI for Knights and Creatures
Integrates UI components and displays JSON content for testing
"""

import pygame
import sys
import os

# Add the parent directory to the path so we can import from ui modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.ui_base import UIBase, TextPanel
from ui.button import Button, ButtonGroup
from ui.json_loader import JSONContentLoader


class MainGameUI:
    """Main game UI class that manages the overall game interface."""

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

        # Initialize UI base
        self.ui_base = UIBase(self.screen)

        # Initialize content loader
        self.json_loader = JSONContentLoader("data")

        # Create UI panels
        self.story_panel = TextPanel(self.screen, 50, 50, 600, 400)
        self.info_panel = TextPanel(self.screen, 700, 50, 250, 400)

        # Create buttons
        self.button_group = ButtonGroup()
        self.setup_buttons()

        # Game state
        self.current_scene = "blue_stone"
        self.sample_data = {}

        # Load initial content
        self.load_sample_content()

    def setup_buttons(self):
        """Set up the game buttons."""
        button_width = 180
        button_height = 40
        button_x = 70
        start_y = 470

        # Create sample buttons to test functionality
        buttons_data = [
            ("Load Blue Stone", lambda: self.load_scene_content("blue_stone")),
            ("Load Character Classes", lambda: self.load_scene_content("character_classes")),
            ("Load Start Game", lambda: self.load_scene_content("start_game")),
            ("Next Sample", self.next_sample),
            ("Quit Game", self.quit_game)
        ]

        for i, (text, callback) in enumerate(buttons_data):
            button_y = start_y + (i * 45)
            button = Button(
                self.screen,
                button_x,
                button_y,
                button_width,
                button_height,
                text,
                callback
            )
            self.button_group.add_button(button)

    def load_sample_content(self):
        """Load initial sample content from JSON."""
        self.load_scene_content("blue_stone")

    def load_scene_content(self, content_type: str):
        """
        Load and display content from JSON files.

        Args:
            content_type: Type of content to load (blue_stone, character_classes, start_game)
        """
        print(f"Loading content type: {content_type}")
        self.current_scene = content_type
        self.sample_data = self.json_loader.extract_sample_text(content_type)

        # Also try to load character class info for the info panel
        if content_type == "character_classes":
            classes_data = self.json_loader.get_character_classes()
            if classes_data and len(classes_data) > 0:
                first_class = classes_data[0]
                self.sample_data['info_text'] = f"Class: {first_class.get('name', 'Unknown')}\n\n"
                self.sample_data['info_text'] += f"Abilities: {len(first_class.get('abilities', []))}\n"
                self.sample_data['info_text'] += f"Strength: {first_class.get('attributes', {}).get('strength', 'N/A')}\n"
                self.sample_data['info_text'] += f"Magic: {first_class.get('attributes', {}).get('magic', 'N/A')}\n"
                self.sample_data['info_text'] += f"Charisma: {first_class.get('attributes', {}).get('charisma', 'N/A')}"
            else:
                self.sample_data['info_text'] = "Character data not available"
        elif content_type == "blue_stone":
            blue_stone_data = self.json_loader.get_scene_data("blue_stone")
            if blue_stone_data:
                self.sample_data['info_text'] = f"Scene: {blue_stone_data.get('scene_id', 'Unknown')}\n\n"
                chapters = blue_stone_data.get('chapters', [])
                self.sample_data['info_text'] += f"Chapters: {len(chapters)}\n"
                if chapters:
                    self.sample_data['info_text'] += f"Choices in first chapter: {len(chapters[0].get('choices', []))}"
            else:
                self.sample_data['info_text'] = "Scene data not available"
        else:
            self.sample_data['info_text'] = f"Loaded: {content_type}\n\nThis is sample info panel text to test the UI layout and text wrapping functionality."

    def next_sample(self):
        """Cycle through different sample content."""
        content_types = ["blue_stone", "character_classes", "start_game"]
        try:
            current_index = content_types.index(self.current_scene)
            next_index = (current_index + 1) % len(content_types)
            self.load_scene_content(content_types[next_index])
        except ValueError:
            # If current_scene is not in the list, default to first
            self.load_scene_content(content_types[0])

    def quit_game(self):
        """Quit the game."""
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.next_sample()

            # Handle button events
            clicked_button = self.button_group.handle_event(event)
            if clicked_button:
                print(f"Button clicked: {clicked_button.text}")

        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        self.button_group.update_hover_states(mouse_pos)

        return True

    def render(self):
        """Render the game UI."""
        # Clear screen with background color
        self.screen.fill(self.ui_base.colors['background'])

        # Draw title
        title_text = self.sample_data.get('title', 'Knights and Creatures')
        self.ui_base.render_title(title_text, 50, 10)

        # Draw story panel with main content
        story_text = self.sample_data.get('story_text', 'Loading game content...')
        scene_desc = self.sample_data.get('scene_description', '')

        # Combine story text and scene description
        full_story = story_text
        if scene_desc and scene_desc != story_text:
            full_story += f"\n\n{scene_desc}"

        self.story_panel.display_text(full_story, "Story")

        # Draw info panel
        info_text = self.sample_data.get('info_text', 'Game information will appear here.')
        self.info_panel.display_text(info_text, "Information")

        # Draw buttons
        self.button_group.draw_all()

        # Draw instructions at the top right area
        instruction_text = "Press SPACE to cycle content, ESC to quit, or click buttons to interact"
        self.ui_base.render_text(
            instruction_text,
            700,
            470,
            color=(150, 150, 150),
            max_width=250
        )

        # Update display
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        print("Starting Knights and Creatures UI Demo")
        print("Loading JSON content...")

        # Load all available content for testing
        all_content = self.json_loader.load_all_content()
        print(f"Loaded {len(all_content)} JSON files:")
        for filename in all_content.keys():
            print(f"  - {filename}")

        running = True
        while running:
            running = self.handle_events()
            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    try:
        game = MainGameUI()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
