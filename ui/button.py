"""
Button component for the Knights and Creatures game.
Provides clickable buttons with hover effects and event handling.
"""

import pygame
from .ui_base import UIBase


class Button(UIBase):
    """A clickable button with hover effects and customizable appearance."""

    def __init__(self, screen, x, y, width, height, text, callback=None):
        """
        Initialize a button.

        Args:
            screen: The pygame surface to draw on (pygame.Surface)
            x, y: Button position (int, int)
            width, height: Button dimensions (int, int)
            text: Text to display on the button (str)
            callback: Function to call when button is clicked (callable or None)
        """
        super().__init__(screen)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback

        # Button states
        self.is_hovered = False
        self.is_pressed = False
        self.is_enabled = True

        # Create button rectangle
        self.rect = pygame.Rect(x, y, width, height)

        # Button styling
        self.padding = 8
        self.border_radius = 5

    def handle_event(self, event):
        """
        Handle pygame events for the button.

        Args:
            event: The pygame event to handle (pygame.event.Event)

        Returns:
            True if the button was clicked, False otherwise (bool)
        """
        if not self.is_enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # Left click
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                if self.callback:
                    self.callback()
                return True
            self.is_pressed = False

        return False

    def update_hover_state(self, mouse_pos):
        """
        Update hover state based on mouse position.

        Args:
            mouse_pos: Current mouse position (tuple of x, y coordinates)
        """
        if self.is_enabled:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
        else:
            self.is_hovered = False

    def draw(self):
        """Draw the button to the screen."""
        # Determine button color based on state
        if not self.is_enabled:
            button_color = (50, 50, 50)
            text_color = (100, 100, 100)
        elif self.is_pressed:
            button_color = (50, 50, 70)
            text_color = self.colors['button_text']
        elif self.is_hovered:
            button_color = self.colors['button_hover']
            text_color = self.colors['button_text']
        else:
            button_color = self.colors['button']
            text_color = self.colors['button_text']

        # Draw button background with rounded corners (if supported)
        if hasattr(pygame.draw, 'rect') and self.border_radius > 0:
            try:
                # Try to use rounded rectangle (pygame 2.0+)
                pygame.draw.rect(self.screen, button_color, self.rect, border_radius=self.border_radius)
            except TypeError:
                # Fallback for older pygame versions
                pygame.draw.rect(self.screen, button_color, self.rect)
        else:
            pygame.draw.rect(self.screen, button_color, self.rect)

        # Draw button border
        border_color = self.colors['border']
        pygame.draw.rect(self.screen, border_color, self.rect, 2)

        # Draw button text (centered)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def set_enabled(self, enabled):
        """
        Enable or disable the button.

        Args:
            enabled: Whether the button should be enabled (bool)
        """
        self.is_enabled = enabled
        if not enabled:
            self.is_hovered = False
            self.is_pressed = False

    def set_text(self, text):
        """
        Update the button text.

        Args:
            text: New text for the button (str)
        """
        self.text = text

    def set_callback(self, callback):
        """
        Set or update the button's callback function.

        Args:
            callback: Function to call when button is clicked (callable)
        """
        self.callback = callback

    def get_rect(self):
        """
        Get the button's rectangle for collision detection.

        Returns:
            The button's pygame.Rect
        """
        return self.rect


class ButtonGroup:
    """A group of buttons for easier management."""

    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        """Add a button to the group."""
        self.buttons.append(button)

    def remove_button(self, button):
        """Remove a button from the group."""
        if button in self.buttons:
            self.buttons.remove(button)

    def handle_event(self, event):
        """
        Handle events for all buttons in the group.

        Args:
            event: The pygame event to handle (pygame.event.Event)

        Returns:
            The button that was clicked, or None
        """
        for button in self.buttons:
            if button.handle_event(event):
                return button
        return None

    def update_hover_states(self, mouse_pos):
        """Update hover states for all buttons."""
        for button in self.buttons:
            button.update_hover_state(mouse_pos)

    def draw_all(self):
        """Draw all buttons in the group."""
        for button in self.buttons:
            button.draw()

    def set_all_enabled(self, enabled):
        """Enable or disable all buttons in the group."""
        for button in self.buttons:
            button.set_enabled(enabled)
