"""
Enhanced Button component for the Knights and Creatures game.
Provides clickable buttons with hover effects, keyboard navigation, and selection highlighting.
"""

import pygame
from .ui_base import UIBase


class Button(UIBase):
    """A clickable button with hover effects, keyboard navigation, and customizable appearance."""

    def __init__(self, screen, x, y, width, height, text, callback=None, keyboard_key=None):
        """
        Initialize a button.

        Args:
            screen: The pygame surface to draw on (pygame.Surface)
            x, y: Button position (int, int)
            width, height: Button dimensions (int, int)
            text: Text to display on the button (str)
            callback: Function to call when button is clicked (callable or None)
            keyboard_key: Pygame key constant for keyboard activation (int or None)
        """
        super().__init__(screen)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.keyboard_key = keyboard_key

        # Button states
        self.is_hovered = False
        self.is_pressed = False
        self.is_enabled = True
        self.is_selected = False  # For keyboard navigation
        self.is_focused = False   # Alternative selection state

        # Create button rectangle
        self.rect = pygame.Rect(x, y, width, height)

        # Button styling
        self.padding = 8
        self.border_radius = 5

        # Animation properties
        self.hover_animation_progress = 0.0
        self.animation_speed = 8.0
        self.press_animation_progress = 0.0

        # Sound effects (placeholder for future implementation)
        self.hover_sound = None
        self.click_sound = None

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

        # Mouse events
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.is_hovered
            self.is_hovered = self.rect.collidepoint(event.pos)

            # Play hover sound on first hover
            if self.is_hovered and not was_hovered and self.hover_sound:
                # self.hover_sound.play()  # Uncomment when sound system is ready
                pass

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # Left click
                self.is_pressed = True
                return False  # Don't trigger callback yet

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                return self._trigger_callback()
            self.is_pressed = False

        # Keyboard events
        elif event.type == pygame.KEYDOWN:
            # Check for specific key binding
            if self.keyboard_key and event.key == self.keyboard_key:
                return self._trigger_callback()

            # Check for Enter/Space when selected
            elif self.is_selected and event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                return self._trigger_callback()

        return False

    def _trigger_callback(self):
        """Internal method to trigger the callback with effects."""
        if self.callback:
            # Play click sound
            if self.click_sound:
                # self.click_sound.play()  # Uncomment when sound system is ready
                pass

            # Visual feedback
            self.press_animation_progress = 1.0

            # Execute callback
            self.callback()
            return True
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

    def update(self, dt):
        """
        Update button animations and state.

        Args:
            dt: Delta time since last update (float)
        """
        # Update hover animation
        target_hover = 1.0 if self.is_hovered else 0.0
        if self.hover_animation_progress != target_hover:
            if self.hover_animation_progress < target_hover:
                self.hover_animation_progress = min(1.0,
                    self.hover_animation_progress + self.animation_speed * dt)
            else:
                self.hover_animation_progress = max(0.0,
                    self.hover_animation_progress - self.animation_speed * dt)

        # Update press animation
        if self.press_animation_progress > 0.0:
            self.press_animation_progress = max(0.0,
                self.press_animation_progress - self.animation_speed * 2 * dt)

    def draw(self):
        """Draw the button to the screen with enhanced visual effects."""
        # Calculate colors based on state and animations
        base_button_color = self.colors['button']
        hover_color = self.colors['button_hover']

        if not self.is_enabled:
            button_color = (50, 50, 50)
            text_color = (100, 100, 100)
            border_color = (70, 70, 70)
        else:
            # Interpolate button color based on hover animation
            hover_factor = self.hover_animation_progress
            button_color = self._interpolate_color(base_button_color, hover_color, hover_factor)

            # Add press effect
            if self.is_pressed or self.press_animation_progress > 0:
                press_factor = max(0.3 if self.is_pressed else 0, self.press_animation_progress * 0.3)
                button_color = self._darken_color(button_color, press_factor)

            text_color = self.colors['button_text']
            border_color = self.colors['border']

        # Adjust rect for press animation
        draw_rect = self.rect.copy()
        if self.is_pressed:
            draw_rect.x += 1
            draw_rect.y += 1

        # Draw selection highlight for keyboard navigation
        if self.is_selected or self.is_focused:
            selection_rect = pygame.Rect(draw_rect.x - 3, draw_rect.y - 3,
                                       draw_rect.width + 6, draw_rect.height + 6)
            pygame.draw.rect(self.screen, (255, 255, 100), selection_rect, 3)

        # Draw button background with rounded corners (if supported)
        self._draw_rounded_rect(button_color, draw_rect)

        # Draw button border
        border_width = 3 if (self.is_selected or self.is_focused) else 2
        pygame.draw.rect(self.screen, border_color, draw_rect, border_width)

        # Draw button text (centered)
        font_size_modifier = 0.95 if self.is_pressed else 1.0
        text_surface = self.font.render(self.text, True, text_color)

        if font_size_modifier != 1.0:
            # Scale text slightly when pressed
            new_size = (int(text_surface.get_width() * font_size_modifier),
                       int(text_surface.get_height() * font_size_modifier))
            text_surface = pygame.transform.scale(text_surface, new_size)

        text_rect = text_surface.get_rect(center=draw_rect.center)
        self.screen.blit(text_surface, text_rect)

        # Draw keyboard shortcut hint
        if self.keyboard_key and self.is_enabled:
            self._draw_keyboard_hint()

    def _draw_rounded_rect(self, color, rect):
        """Draw a rounded rectangle."""
        if hasattr(pygame.draw, 'rect') and self.border_radius > 0:
            try:
                # Try to use rounded rectangle (pygame 2.0+)
                pygame.draw.rect(self.screen, color, rect, border_radius=self.border_radius)
            except TypeError:
                # Fallback for older pygame versions
                pygame.draw.rect(self.screen, color, rect)
        else:
            pygame.draw.rect(self.screen, color, rect)

    def _draw_keyboard_hint(self):
        """Draw keyboard shortcut hint in corner of button."""
        key_name = pygame.key.name(self.keyboard_key).upper()
        if len(key_name) > 3:
            key_name = key_name[:3]

        hint_font = pygame.font.Font(None, 16)
        hint_surface = hint_font.render(key_name, True, (200, 200, 200))
        hint_rect = hint_surface.get_rect()
        hint_rect.topright = (self.rect.right - 4, self.rect.top + 2)

        # Draw small background
        bg_rect = pygame.Rect(hint_rect.x - 2, hint_rect.y,
                             hint_rect.width + 4, hint_rect.height)
        pygame.draw.rect(self.screen, (0, 0, 0, 100), bg_rect)

        self.screen.blit(hint_surface, hint_rect)

    def _interpolate_color(self, color1, color2, factor):
        """Interpolate between two colors."""
        factor = max(0.0, min(1.0, factor))
        return tuple(int(c1 + (c2 - c1) * factor) for c1, c2 in zip(color1, color2))

    def _darken_color(self, color, factor):
        """Darken a color by a factor."""
        return tuple(int(c * (1.0 - factor)) for c in color)

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
            self.is_selected = False

    def set_selected(self, selected):
        """
        Set the button as selected (for keyboard navigation).

        Args:
            selected: Whether the button should be selected (bool)
        """
        self.is_selected = selected

    def set_focused(self, focused):
        """
        Set the button as focused (alternative to selected).

        Args:
            focused: Whether the button should be focused (bool)
        """
        self.is_focused = focused

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

    def set_keyboard_key(self, key):
        """
        Set or update the keyboard shortcut for this button.

        Args:
            key: Pygame key constant (int)
        """
        self.keyboard_key = key

    def get_rect(self):
        """
        Get the button's rectangle for collision detection.

        Returns:
            The button's pygame.Rect
        """
        return self.rect

    def is_point_inside(self, point):
        """
        Check if a point is inside the button.

        Args:
            point: (x, y) coordinates to check

        Returns:
            True if point is inside button (bool)
        """
        return self.rect.collidepoint(point)


class ButtonGroup:
    """A group of buttons with keyboard navigation support."""

    def __init__(self):
        self.buttons = []
        self.selected_index = -1
        self.keyboard_navigation_enabled = True

    def add_button(self, button):
        """Add a button to the group."""
        self.buttons.append(button)

        # Auto-select first button if this is the first one
        if len(self.buttons) == 1 and self.keyboard_navigation_enabled:
            self.select_button(0)

    def remove_button(self, button):
        """Remove a button from the group."""
        if button in self.buttons:
            self.buttons.remove(button)

            # Adjust selection if needed
            if self.selected_index >= len(self.buttons):
                self.selected_index = len(self.buttons) - 1

            self._update_selection_display()

    def handle_event(self, event):
        """
        Handle events for all buttons in the group.

        Args:
            event: The pygame event to handle (pygame.event.Event)

        Returns:
            The button that was clicked, or None
        """
        # Handle keyboard navigation
        if self.keyboard_navigation_enabled and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                self.select_previous()
                return None
            elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                self.select_next()
                return None
            elif event.key == pygame.K_TAB:
                if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
                    self.select_previous()
                else:
                    self.select_next()
                return None

        # Handle button events
        for button in self.buttons:
            if button.handle_event(event):
                return button

        return None

    def select_button(self, index):
        """
        Select a button by index for keyboard navigation.

        Args:
            index: Index of button to select (int)
        """
        if 0 <= index < len(self.buttons):
            self.selected_index = index
            self._update_selection_display()

    def select_next(self):
        """Select the next button in the group."""
        if self.buttons:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
            self._update_selection_display()

    def select_previous(self):
        """Select the previous button in the group."""
        if self.buttons:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
            self._update_selection_display()

    def get_selected_button(self):
        """
        Get the currently selected button.

        Returns:
            Selected Button instance or None
        """
        if 0 <= self.selected_index < len(self.buttons):
            return self.buttons[self.selected_index]
        return None

    def _update_selection_display(self):
        """Update the visual selection state of all buttons."""
        for i, button in enumerate(self.buttons):
            button.set_selected(i == self.selected_index)

    def update_hover_states(self, mouse_pos):
        """Update hover states for all buttons."""
        for button in self.buttons:
            button.update_hover_state(mouse_pos)

    def update_all(self, dt):
        """Update all buttons in the group."""
        for button in self.buttons:
            button.update(dt)

    def draw_all(self):
        """Draw all buttons in the group."""
        for button in self.buttons:
            button.draw()

    def set_all_enabled(self, enabled):
        """Enable or disable all buttons in the group."""
        for button in self.buttons:
            button.set_enabled(enabled)

    def set_keyboard_navigation(self, enabled):
        """
        Enable or disable keyboard navigation for the group.

        Args:
            enabled: Whether keyboard navigation should be enabled (bool)
        """
        self.keyboard_navigation_enabled = enabled

        if not enabled:
            # Clear all selections
            for button in self.buttons:
                button.set_selected(False)
            self.selected_index = -1
        elif self.buttons and self.selected_index == -1:
            # Auto-select first button
            self.select_button(0)

    def clear(self):
        """Remove all buttons from the group."""
        self.buttons.clear()
        self.selected_index = -1

    def get_button_count(self):
        """
        Get the number of buttons in the group.

        Returns:
            Number of buttons (int)
        """
        return len(self.buttons)

    def find_button_by_text(self, text):
        """
        Find a button by its text content.

        Args:
            text: Text to search for (str)

        Returns:
            Button instance or None if not found
        """
        for button in self.buttons:
            if button.text == text:
                return button
        return None
