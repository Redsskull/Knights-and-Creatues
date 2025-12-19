"""
Base UI components for the Knights and Creatures game.
Provides text rendering, wrapping, and basic UI functionality.
"""

import pygame
import textwrap


class UIBase:
    """Base class for UI components with common functionality."""

    def __init__(self, screen):
        # screen: pygame.Surface
        self.screen = screen
        self.font_size = 18
        self.font = pygame.font.Font(None, self.font_size)
        self.title_font = pygame.font.Font(None, 28)

        # Color scheme
        self.colors = {
            'background': (30, 30, 50),
            'text': (255, 255, 255),
            'title': (200, 200, 255),
            'button': (70, 70, 90),
            'button_hover': (90, 90, 110),
            'button_text': (255, 255, 255),
            'panel': (40, 40, 60),
            'border': (100, 100, 120)
        }

    def wrap_text(self, text, max_width):
        """
        Wrap text to fit within the specified pixel width.

        Args:
            text: The text to wrap (str)
            max_width: Maximum width in pixels (int)

        Returns:
            List of wrapped text lines
        """
        # Calculate approximate characters per line based on font
        char_width = self.font.size('A')[0]  # Average character width
        chars_per_line = max_width // char_width

        # Use textwrap to break the text
        wrapped_lines = textwrap.wrap(text, width=chars_per_line)

        # Double-check that lines fit and re-wrap if necessary
        final_lines = []
        for line in wrapped_lines:
            if self.font.size(line)[0] <= max_width:
                final_lines.append(line)
            else:
                # If line is still too long, break it more aggressively
                words = line.split()
                current_line = ""
                for word in words:
                    test_line = current_line + (" " if current_line else "") + word
                    if self.font.size(test_line)[0] <= max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            final_lines.append(current_line)
                        current_line = word
                if current_line:
                    final_lines.append(current_line)

        return final_lines

    def render_text(self, text, x, y, color=None, max_width=None, font=None):
        """
        Render text to the screen with optional wrapping.

        Args:
            text: Text to render (str)
            x, y: Position to start rendering (int, int)
            color: Text color, defaults to self.colors['text'] (tuple of 3 ints)
            max_width: Maximum width for text wrapping, optional (int)
            font: Font to use, defaults to self.font (pygame.font.Font)

        Returns:
            The y-coordinate after the last line of text (int)
        """
        if color is None:
            color = self.colors['text']
        if font is None:
            font = self.font

        if max_width:
            lines = self.wrap_text(text, max_width)
        else:
            lines = [text]

        line_height = font.get_height() + 2  # Add small spacing between lines
        current_y = y

        for line in lines:
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (x, current_y))
            current_y += line_height

        return current_y

    def render_title(self, text, x, y, color=None):
        """
        Render title text using the title font.

        Args:
            text: Title text to render (str)
            x, y: Position to start rendering (int, int)
            color: Text color, defaults to self.colors['title'] (tuple of 3 ints)

        Returns:
            The y-coordinate after the title (int)
        """
        if color is None:
            color = self.colors['title']

        return self.render_text(text, x, y, color, font=self.title_font)

    def draw_panel(self, x, y, width, height, background_color=None, border_color=None, border_width=2):
        """
        Draw a panel with background and optional border.

        Args:
            x, y: Top-left corner position (int, int)
            width, height: Panel dimensions (int, int)
            background_color: Background color, defaults to self.colors['panel'] (tuple of 3 ints)
            border_color: Border color, defaults to self.colors['border'] (tuple of 3 ints)
            border_width: Width of border in pixels (int)

        Returns:
            The pygame.Rect representing the panel area
        """
        if background_color is None:
            background_color = self.colors['panel']
        if border_color is None:
            border_color = self.colors['border']

        panel_rect = pygame.Rect(x, y, width, height)

        # Draw background
        pygame.draw.rect(self.screen, background_color, panel_rect)

        # Draw border
        if border_width > 0:
            pygame.draw.rect(self.screen, border_color, panel_rect, border_width)

        return panel_rect

    def get_text_dimensions(self, text, font=None):
        """
        Get the dimensions of rendered text.

        Args:
            text: Text to measure (str)
            font: Font to use, defaults to self.font (pygame.font.Font)

        Returns:
            Tuple of (width, height) in pixels
        """
        if font is None:
            font = self.font
        return font.size(text)


class TextPanel(UIBase):
    """A panel specifically designed for displaying wrapped text content."""

    def __init__(self, screen, x, y, width, height):
        # screen: pygame.Surface
        super().__init__(screen)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.padding = 10
        self.content_width = width - (self.padding * 2)
        self.content_height = height - (self.padding * 2)

    def display_text(self, text, title=""):
        """
        Display text in the panel with optional title.

        Args:
            text: Main text content to display (str)
            title: Optional title text (str)
        """
        # Clear and draw panel background
        self.draw_panel(self.x, self.y, self.width, self.height)

        current_y = self.y + self.padding

        # Render title if provided
        if title:
            current_y = self.render_title(title, self.x + self.padding, current_y)
            current_y += 10  # Extra spacing after title

        # Render main text with wrapping
        self.render_text(text, self.x + self.padding, current_y,
                        max_width=self.content_width)
