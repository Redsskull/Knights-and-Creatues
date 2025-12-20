"""
UI package for Knights and Creatures game.
Contains all user interface components, scene management, and utilities.
"""

from .ui_base import UIBase, TextPanel
from .button import Button, ButtonGroup
from .json_loader import JSONContentLoader
from .scene import Scene, JSONScene
from .scene_manager import SceneManager
# from .demo_scene import DemoScene  # TODO: Create demo scene

__all__ = [
    'UIBase',
    'TextPanel',
    'Button',
    'ButtonGroup',
    'JSONContentLoader',
    'Scene',
    'JSONScene',
    'SceneManager',
    # 'DemoScene'  # TODO: Add when demo scene is created
]
