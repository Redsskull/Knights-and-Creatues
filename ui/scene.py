"""
Enhanced Scene management system for Knights and Creatures game.
Provides base Scene class with improved input handling, keyboard navigation, and scene transition functionality.
"""

import pygame
from .ui_base import UIBase, TextPanel
from .button import Button, ButtonGroup


class Scene:
    """Base class for all game scenes with enhanced input handling."""

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

        # Input handling
        self.input_blocked = False
        self.transition_in_progress = False

        # Animation state
        self.fade_alpha = 0
        self.scene_transition_time = 0

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

        # Enable button group keyboard navigation
        self.button_group.set_keyboard_navigation(True)
        self.input_blocked = False
        self.transition_in_progress = False

    def exit(self):
        """Called when leaving this scene."""
        self.is_active = False
        self.input_blocked = True

    def handle_event(self, event):
        """
        Handle pygame events for this scene.

        Args:
            event: pygame event to handle

        Returns:
            True if event was handled, False otherwise (bool)
        """
        if not self.is_active or self.input_blocked:
            return False

        # Handle button events first
        clicked_button = self.button_group.handle_event(event)
        if clicked_button:
            return self.on_button_click(clicked_button)

        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            return self.on_key_press(event.key, event.mod)

        # Handle mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self.on_mouse_click(event.pos, event.button)

        return False

    def on_button_click(self, button):
        """
        Handle button click events.

        Args:
            button: Button that was clicked

        Returns:
            True if handled (bool)
        """
        # Default implementation - override in subclasses
        print(f"Button clicked: {button.text}")
        return True

    def on_key_press(self, key, mod):
        """
        Handle key press events.

        Args:
            key: pygame key constant
            mod: pygame key modifier constant

        Returns:
            True if handled (bool)
        """
        # Global key handling
        if key == pygame.K_ESCAPE:
            self.scene_manager.quit_game()
            return True

        # Number keys for quick choice selection
        if pygame.K_1 <= key <= pygame.K_9:
            choice_index = key - pygame.K_1
            if choice_index < self.button_group.get_button_count():
                self.button_group.select_button(choice_index)
                button = self.button_group.get_selected_button()
                if button and button.callback:
                    button.callback()
                return True

        # F keys for testing and debugging
        if key == pygame.K_F5:
            self.reload_scene()
            return True
        elif key == pygame.K_F12:
            self.toggle_debug_info()
            return True

        return False

    def on_mouse_click(self, pos, button):
        """
        Handle mouse click events.

        Args:
            pos: Mouse position (x, y)
            button: Mouse button pressed (1=left, 2=middle, 3=right)

        Returns:
            True if handled (bool)
        """
        # Right-click for context menu (future implementation)
        if button == 3:
            self.show_context_menu(pos)
            return True

        return False

    def show_context_menu(self, pos):
        """Show context menu at position (placeholder for future implementation)."""
        print(f"Context menu requested at {pos}")

    def reload_scene(self):
        """Reload the current scene (for debugging)."""
        print(f"Reloading scene: {self.scene_id}")
        self.is_initialized = False
        self.button_group.clear()
        self.initialize()

    def toggle_debug_info(self):
        """Toggle debug information display."""
        print(f"Debug info toggle for scene: {self.scene_id}")

    def update(self, dt):
        """
        Update scene logic.

        Args:
            dt: delta time since last update (float)
        """
        # Update buttons
        self.button_group.update_all(dt)

        # Update hover states for buttons
        mouse_pos = pygame.mouse.get_pos()
        self.button_group.update_hover_states(mouse_pos)

        # Update scene-specific logic
        self.update_scene_logic(dt)

    def update_scene_logic(self, dt):
        """
        Update scene-specific logic. Override in subclasses.

        Args:
            dt: delta time since last update (float)
        """
        pass

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

        # Draw scene-specific content
        self.render_scene_content()

        # Draw keyboard hints
        self.render_keyboard_hints()

    def render_scene_content(self):
        """Render scene-specific content. Override in subclasses."""
        pass

    def render_keyboard_hints(self):
        """Render keyboard navigation hints."""
        if self.button_group.get_button_count() > 0:
            hints = [
                "Arrow Keys: Navigate",
                "Enter/Space: Select",
                "1-9: Quick Select",
                "ESC: Exit"
            ]

            y_offset = self.screen.get_height() - 100
            font = pygame.font.Font(None, 20)

            for i, hint in enumerate(hints):
                text_surface = font.render(hint, True, (150, 150, 150))
                self.screen.blit(text_surface, (10, y_offset + i * 20))

    def transition_to(self, scene_id, data=None):
        """
        Transition to another scene.

        Args:
            scene_id: ID of scene to transition to (str)
            data: Optional data to pass to next scene (dict)
        """
        if not self.transition_in_progress:
            self.transition_in_progress = True
            self.scene_manager.transition_to(scene_id, data, use_transition=False)

    def set_scene_data(self, data):
        """
        Set scene data from external source.

        Args:
            data: Dictionary containing scene data
        """
        self.scene_data = data or {}

    def block_input(self, blocked=True):
        """
        Block or unblock input handling.

        Args:
            blocked: Whether input should be blocked (bool)
        """
        self.input_blocked = blocked

    def add_choice_button(self, choice_id, text, callback, keyboard_key=None):
        """
        Add a choice button to the scene.

        Args:
            choice_id: Unique identifier for the choice (str)
            text: Display text for the button (str)
            callback: Function to call when clicked (callable)
            keyboard_key: Optional keyboard shortcut (pygame key constant)
        """
        button_count = self.button_group.get_button_count()
        button_y = 460 + (button_count * 40)

        button = Button(
            self.screen,
            50,
            button_y,
            500,
            35,
            text,
            callback,
            keyboard_key
        )

        self.button_group.add_button(button)
        return button

    def clear_choice_buttons(self):
        """Clear all choice buttons from the scene."""
        self.button_group.clear()


class JSONScene(Scene):
    """Scene that loads content from JSON files with enhanced input handling."""

    def __init__(self, scene_manager, scene_id, json_file, title=None):
        # json_file: name of JSON file to load (str)
        super().__init__(scene_manager, scene_id, title or scene_id.replace('_', ' ').title())
        self.json_file = json_file
        self.current_choice_data = {}
        self.pending_transition = None
        self.current_chapter = ''
        self.scene_chapters = {}

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
            # Scene-based JSON structure with chapters
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

        # Store all chapters for navigation
        chapters = content.get('chapters', [])
        self.scene_chapters = {chapter.get('chapter_id', ''): chapter for chapter in chapters}

        if chapters:
            first_chapter = chapters[0]
            self.load_chapter(first_chapter)
        else:
            self.scene_data = {
                'story_text': 'No chapters found in scene data.',
                'info_text': 'Scene loading error'
            }

    def load_chapter(self, chapter):
        """Load a specific chapter's content."""
        story_text = chapter.get('story_text', '')
        description = chapter.get('description', '')

        if description:
            story_text = f"{description}\n\n{story_text}"

        prompt = chapter.get('prompt', '')
        if prompt:
            story_text = f"{story_text}\n\n{prompt}"

        self.scene_data = {
            'story_text': story_text,
            'info_text': f"Chapter: {chapter.get('title', 'Unknown')}\nScene: {self.scene_id}"
        }

        # Create choice buttons with keyboard shortcuts
        self.clear_choice_buttons()
        self.create_choice_buttons(chapter.get('choices', []))

        # Store current chapter for multi-chapter scenes
        self.current_chapter = chapter.get('chapter_id', '')

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

            # Create class selection buttons with keyboard shortcuts
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
        Create buttons for story choices with keyboard shortcuts.

        Args:
            choices: List of choice dictionaries
        """
        self.clear_choice_buttons()

        for i, choice in enumerate(choices[:9]):  # Limit to 9 choices for number keys
            choice_text = f"{choice.get('text', 'Unknown choice')}"
            keyboard_key = getattr(pygame, f'K_{i+1}') if i < 9 else None

            # Store choice data for handling
            choice_id = choice.get('id', str(i+1))
            self.current_choice_data[choice_id] = choice

            self.add_choice_button(
                choice_id,
                f"{i+1}. {choice_text}",
                lambda c=choice: self.handle_choice(c),
                keyboard_key
            )

    def create_class_buttons(self, classes):
        """
        Create buttons for character class selection with keyboard shortcuts.

        Args:
            classes: List of class dictionaries
        """
        self.clear_choice_buttons()

        for i, char_class in enumerate(classes):
            class_name = char_class.get('name', f'Class {i+1}')
            keyboard_key = getattr(pygame, f'K_{i+1}') if i < 9 else None

            self.add_choice_button(
                f"class_{i}",
                f"{i+1}. {class_name}",
                lambda c=char_class: self.handle_class_selection(c),
                keyboard_key
            )

    def handle_choice(self, choice):
        """
        Handle story choice selection.

        Args:
            choice: Selected choice dictionary
        """
        choice_id = choice.get('id', '')

        # Support both 'outcome' (start_game.json) and 'result' (blue_stone_scenes.json) formats
        outcome = choice.get('outcome') or choice.get('result', {})

        print(f"Selected choice: {choice_id}")

        # Show choice result message
        message = outcome.get('message', 'No result message')
        print(f"Result: {message}")

        # Update info panel with result
        self.scene_data['info_text'] = f"Choice: {choice.get('text', 'Unknown')}\n\nResult: {message}"

        # Store choice in game data
        self.scene_manager.set_game_data(f'last_choice_{self.scene_id}', choice_id)

        # Check for scene transitions - support both formats
        next_scene = outcome.get('next_scene') or outcome.get('next_chapter')

        if next_scene:
            # Store the transition target and set timer
            self.pending_transition = next_scene
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 second delay
        else:
            # If no next scene but outcome is successful, try default progression
            if outcome.get('success', False):
                # For start_game scene, go to character selection
                if self.scene_id == 'start_game':
                    self.pending_transition = 'character_select'
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
                # For blue_stone scene completion, progress to next stone
                elif self.scene_id == 'blue_stone':
                    # Store blue stone completion and move to yellow stone
                    self.scene_manager.set_game_data('has_blue_stone', True)
                    self.pending_transition = 'yellow_stone'
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
                else:
                    print("Choice completed - no further progression defined")

    def handle_class_selection(self, char_class):
        """
        Handle character class selection.

        Args:
            char_class: Selected character class dictionary
        """
        class_name = char_class.get('name', 'Unknown')
        print(f"Selected class: {class_name}")

        # Store selection in game data
        self.scene_manager.set_game_data('selected_class', char_class)

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

        # Set up transition after class selection
        self.pending_transition = 'blue_stone'  # Default next scene after character selection
        pygame.time.set_timer(pygame.USEREVENT + 2, 2000)  # 2 second delay

    def handle_event(self, event):
        """
        Enhanced event handling for JSON scenes.

        Args:
            event: pygame event to handle

        Returns:
            True if event was handled (bool)
        """
        # Handle custom timer events
        if event.type == pygame.USEREVENT + 1:
            # Choice selection delay finished
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer
            if hasattr(self, 'pending_transition') and self.pending_transition:
                next_target = self.pending_transition
                self.pending_transition = None

                # Check if it's a chapter transition within the same scene
                if next_target in self.scene_chapters:
                    # Load the next chapter
                    next_chapter = self.scene_chapters[next_target]
                    self.load_chapter(next_chapter)
                else:
                    # Transition to a different scene
                    self.transition_to(next_target)
            return True

        elif event.type == pygame.USEREVENT + 2:
            # Class selection delay finished
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # Cancel timer
            if hasattr(self, 'pending_transition') and self.pending_transition:
                next_scene = self.pending_transition
                self.pending_transition = None
                self.transition_to(next_scene)
            else:
                # Default: go to blue_stone scene after character selection
                self.transition_to('blue_stone')
            return True

        # Call parent event handling
        return super().handle_event(event)

    def render_scene_content(self):
        """Render JSON scene specific content."""
        # Add any JSON-specific rendering here
        pass
