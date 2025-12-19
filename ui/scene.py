"""
Scene management system for Knights and Creatures game.
Provides base Scene class and scene transition functionality.
"""

import pygame
from .ui_base import UIBase, TextPanel
from .button import Button, ButtonGroup


class Scene:
    """Base class for all game scenes."""

    def __init__(self, scene_manager, scene_id, title="Untitled Scene"):
        # scene_manager: SceneManager instance
        # scene_id: unique identifier for this scene (str)
        # title: display title for the scene (str)
        self.scene_manager = scene_manager
        self.scene_id = scene_id
        self.title = title
        self.screen = scene_manager.screen
        self.ui_base = UIBase(self.screen)

        # Scene state
        self.is_active = False
        self.is_initialized = False

        # UI components
        self.button_group = ButtonGroup()
        self.story_panel = None
        self.info_panel = None

        # Scene data
        self.scene_data = {}
        self.choices = []

    def initialize(self):
        """Initialize the scene. Override this in subclasses."""
        if self.is_initialized:
            return

        self.setup_ui()
        self.load_content()
        self.is_initialized = True

    def setup_ui(self):
        """Set up UI components for this scene."""
        # Create default panels
        self.story_panel = TextPanel(self.screen, 50, 80, 600, 350)
        self.info_panel = TextPanel(self.screen, 700, 80, 250, 350)

    def load_content(self):
        """Load scene content. Override this in subclasses."""
        pass

    def enter(self):
        """Called when entering this scene."""
        self.is_active = True
        if not self.is_initialized:
            self.initialize()

    def exit(self):
        """Called when leaving this scene."""
        self.is_active = False

    def handle_event(self, event):
        """
        Handle pygame events for this scene.

        Args:
            event: pygame event to handle

        Returns:
            True if event was handled, False otherwise (bool)
        """
        if not self.is_active:
            return False

        # Handle button events
        clicked_button = self.button_group.handle_event(event)
        if clicked_button:
            return self.on_button_click(clicked_button)

        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            return self.on_key_press(event.key)

        return False

    def on_button_click(self, button):
        """
        Handle button click events.

        Args:
            button: Button that was clicked

        Returns:
            True if handled (bool)
        """
        # Override in subclasses
        return False

    def on_key_press(self, key):
        """
        Handle key press events.

        Args:
            key: pygame key constant

        Returns:
            True if handled (bool)
        """
        # Default key handling
        if key == pygame.K_ESCAPE:
            self.scene_manager.quit_game()
            return True
        return False

    def update(self, dt):
        """
        Update scene logic.

        Args:
            dt: delta time since last update (float)
        """
        # Update hover states for buttons
        mouse_pos = pygame.mouse.get_pos()
        self.button_group.update_hover_states(mouse_pos)

    def render(self):
        """Render the scene to the screen."""
        if not self.is_active:
            return

        # Clear screen
        self.screen.fill(self.ui_base.colors['background'])

        # Draw title
        self.ui_base.render_title(self.title, 50, 20)

        # Draw panels if they exist
        if self.story_panel:
            self.story_panel.display_text(
                self.scene_data.get('story_text', 'No story content loaded.'),
                "Story"
            )

        if self.info_panel:
            self.info_panel.display_text(
                self.scene_data.get('info_text', 'No information available.'),
                "Information"
            )

        # Draw buttons
        self.button_group.draw_all()

    def transition_to(self, scene_id, data=None):
        """
        Transition to another scene.

        Args:
            scene_id: ID of scene to transition to (str)
            data: Optional data to pass to next scene (dict)
        """
        self.scene_manager.transition_to(scene_id, data)

    def set_scene_data(self, data):
        """
        Set scene data from external source.

        Args:
            data: Dictionary containing scene data
        """
        self.scene_data = data or {}


class JSONScene(Scene):
    """Scene that loads content from JSON files."""

    def __init__(self, scene_manager, scene_id, json_file, title=None):
        # json_file: name of JSON file to load (str)
        super().__init__(scene_manager, scene_id, title or scene_id.replace('_', ' ').title())
        self.json_file = json_file

    def load_content(self):
        """Load content from JSON file."""
        json_loader = self.scene_manager.json_loader

        if self.json_file.endswith('_scenes.json'):
            # Load scene data
            scene_name = self.json_file.replace('_scenes.json', '')
            content = json_loader.get_scene_data(scene_name)
        else:
            # Load regular JSON file
            content = json_loader.load_file(self.json_file)

        if content:
            self.parse_json_content(content)
        else:
            self.scene_data = {
                'story_text': f'Failed to load content from {self.json_file}',
                'info_text': 'Content loading error'
            }

    def parse_json_content(self, content):
        """
        Parse JSON content and set up scene data.

        Args:
            content: Loaded JSON content (dict)
        """
        # Handle different JSON structures
        if 'chapters' in content:
            # Scene-based JSON structure
            self.parse_scene_chapters(content)
        elif 'classes' in content:
            # Character classes JSON
            self.parse_character_classes(content)
        elif 'story_text' in content:
            # Simple story JSON
            self.parse_simple_story(content)
        else:
            # Generic JSON
            self.scene_data = {
                'story_text': str(content),
                'info_text': f'Loaded {self.json_file}'
            }

    def parse_scene_chapters(self, content):
        """Parse scene with chapters structure."""
        self.title = content.get('title', self.title)

        # Get first chapter for display
        chapters = content.get('chapters', [])
        if chapters:
            first_chapter = chapters[0]
            story_text = first_chapter.get('story_text', '')
            description = first_chapter.get('description', '')

            if description:
                story_text = f"{description}\n\n{story_text}"

            self.scene_data = {
                'story_text': story_text,
                'info_text': f"Scene: {content.get('scene_id', 'Unknown')}\nChapters: {len(chapters)}"
            }

            # Create choice buttons
            self.create_choice_buttons(first_chapter.get('choices', []))
        else:
            self.scene_data = {
                'story_text': 'No chapters found in scene data.',
                'info_text': 'Scene loading error'
            }

    def parse_character_classes(self, content):
        """Parse character classes structure."""
        classes = content.get('classes', [])
        if classes:
            # Show first class as example
            first_class = classes[0]

            self.scene_data = {
                'story_text': f"Class: {first_class.get('name', 'Unknown')}\n\n{first_class.get('description', 'No description')}",
                'info_text': f"Available Classes: {len(classes)}\n\nSelect a class to begin your adventure."
            }

            # Create class selection buttons
            self.create_class_buttons(classes[:4])  # Show first 4 classes
        else:
            self.scene_data = {
                'story_text': 'No character classes found.',
                'info_text': 'Classes loading error'
            }

    def parse_simple_story(self, content):
        """Parse simple story structure."""
        self.title = content.get('title', self.title)
        self.scene_data = {
            'story_text': content.get('story_text', 'No story text found.'),
            'info_text': content.get('description', 'No additional information.')
        }

        # Create buttons for choices if available
        choices = content.get('choices', [])
        if choices:
            self.create_choice_buttons(choices)

    def create_choice_buttons(self, choices):
        """
        Create buttons for story choices.

        Args:
            choices: List of choice dictionaries
        """
        button_y = 460
        button_width = 500
        button_height = 35

        for i, choice in enumerate(choices[:4]):  # Limit to 4 choices
            choice_text = f"{choice.get('id', i+1)}: {choice.get('text', 'Unknown choice')}"

            button = Button(
                self.screen,
                50,
                button_y + (i * 40),
                button_width,
                button_height,
                choice_text,
                lambda c=choice: self.handle_choice(c)
            )
            self.button_group.add_button(button)

    def create_class_buttons(self, classes):
        """
        Create buttons for character class selection.

        Args:
            classes: List of class dictionaries
        """
        button_y = 460
        button_width = 200
        button_height = 35

        for i, char_class in enumerate(classes):
            class_name = char_class.get('name', f'Class {i+1}')

            button = Button(
                self.screen,
                50 + (i % 2) * 220,  # Two columns
                button_y + (i // 2) * 40,
                button_width,
                button_height,
                class_name,
                lambda c=char_class: self.handle_class_selection(c)
            )
            self.button_group.add_button(button)

    def handle_choice(self, choice):
        """
        Handle story choice selection.

        Args:
            choice: Selected choice dictionary
        """
        choice_id = choice.get('id', '')
        result = choice.get('result', {})

        print(f"Selected choice: {choice_id}")
        print(f"Result: {result.get('message', 'No result message')}")

        # Check if this leads to another scene
        next_chapter = result.get('next_chapter')
        if next_chapter:
            # For now, just print - we'll implement proper transitions later
            print(f"Would transition to: {next_chapter}")

    def handle_class_selection(self, char_class):
        """
        Handle character class selection.

        Args:
            char_class: Selected character class dictionary
        """
        class_name = char_class.get('name', 'Unknown')
        print(f"Selected class: {class_name}")

        # Update info panel to show selected class
        abilities = char_class.get('abilities', [])
        attributes = char_class.get('attributes', {})

        info_text = f"Selected: {class_name}\n\n"
        info_text += f"Strength: {attributes.get('strength', 0)}\n"
        info_text += f"Magic: {attributes.get('magic', 0)}\n"
        info_text += f"Charisma: {attributes.get('charisma', 0)}\n\n"

        if abilities:
            info_text += f"Special Ability:\n{abilities[0].get('name', 'None')}"

        self.scene_data['info_text'] = info_text
