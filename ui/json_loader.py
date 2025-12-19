"""
JSON content loader for the Knights and Creatures game.
Handles loading and parsing of game content from JSON files.
"""

import json
import os


class JSONContentLoader:
    """Loads and manages game content from JSON files."""

    def __init__(self, data_directory="data"):
        """
        Initialize the JSON content loader.

        Args:
            data_directory: Path to the directory containing JSON files (str)
        """
        self.data_directory = data_directory
        self.loaded_content = {}

    def load_file(self, filename):
        """
        Load a specific JSON file.

        Args:
            filename: Name of the JSON file to load (str, with or without .json extension)

        Returns:
            Parsed JSON content as dictionary, or None if file not found
        """
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename += '.json'

        filepath = os.path.join(self.data_directory, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = json.load(file)
                self.loaded_content[filename] = content
                return content
        except FileNotFoundError:
            print(f"JSON file not found: {filepath}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file {filepath}: {e}")
            return None
        except Exception as e:
            print(f"Error loading JSON file {filepath}: {e}")
            return None

    def get_character_classes(self):
        """
        Load and return character class data.

        Returns:
            List of character class dictionaries, or None if not found
        """
        content = self.load_file('character_classes.json')
        if content and 'classes' in content:
            return content['classes']
        return None

    def get_scene_data(self, scene_name):
        """
        Load scene data by scene name.

        Args:
            scene_name: Name of the scene to load (str)

        Returns:
            Scene data dictionary, or None if not found
        """
        filename = f"{scene_name}_scenes.json"
        return self.load_file(filename)

    def get_start_game_data(self):
        """
        Load start game content.

        Returns:
            Start game data dictionary, or None if not found
        """
        return self.load_file('start_game.json')

    def get_game_state_schema(self):
        """
        Load the game state schema.

        Returns:
            Game state schema dictionary, or None if not found
        """
        return self.load_file('game_state_schema.json')

    def load_all_content(self):
        """
        Load all JSON files in the data directory.

        Returns:
            Dictionary with filename as key and content as value
        """
        all_content = {}

        if not os.path.exists(self.data_directory):
            print(f"Data directory not found: {self.data_directory}")
            return all_content

        for filename in os.listdir(self.data_directory):
            if filename.endswith('.json'):
                content = self.load_file(filename)
                if content:
                    all_content[filename] = content

        return all_content

    def get_cached_content(self, filename):
        """
        Get previously loaded content from cache.

        Args:
            filename: Name of the JSON file (str)

        Returns:
            Cached content or None if not found
        """
        if not filename.endswith('.json'):
            filename += '.json'
        return self.loaded_content.get(filename)

    def extract_sample_text(self, content_type="blue_stone"):
        """
        Extract real text content from JSON files for display.

        Args:
            content_type: Type of content to extract sample from (str)

        Returns:
            Dictionary with title and text samples extracted from JSON
        """
        sample_data = {
            'title': 'Knights and Creatures',
            'story_text': 'No content loaded - check JSON files.',
            'character_description': '',
            'scene_description': ''
        }

        # Extract real content from JSON files
        if content_type == "blue_stone":
            blue_stone_data = self.get_scene_data("blue_stone")
            if blue_stone_data:
                sample_data['title'] = blue_stone_data.get('title', 'Blue Stone Adventure')
                chapters = blue_stone_data.get('chapters', [])
                if chapters:
                    first_chapter = chapters[0]
                    sample_data['story_text'] = first_chapter.get('story_text', 'Chapter story not found')
                    sample_data['scene_description'] = first_chapter.get('description', 'Chapter description not found')
                    sample_data['character_description'] = f"Chapter: {first_chapter.get('title', 'Unknown')}"
                else:
                    sample_data['story_text'] = 'No chapters found in blue stone data'
            else:
                sample_data['story_text'] = 'Could not load blue stone scene data'

        elif content_type == "character_classes":
            classes_data = self.get_character_classes()
            if classes_data:
                sample_data['title'] = 'Choose Your Character Class'
                first_class = classes_data[0]
                sample_data['character_description'] = first_class.get('description', 'No description available')
                sample_data['story_text'] = f"Class: {first_class.get('name', 'Unknown')}\n\n{first_class.get('description', 'No description available')}"
                abilities = first_class.get('abilities', [])
                if abilities:
                    sample_data['scene_description'] = f"Special Ability: {abilities[0].get('name', 'Unknown')} - {abilities[0].get('description', 'No description')}"
                else:
                    sample_data['scene_description'] = 'No abilities found'
            else:
                sample_data['story_text'] = 'Could not load character classes data'

        elif content_type == "start_game":
            start_data = self.get_start_game_data()
            if start_data:
                sample_data['title'] = start_data.get('title', 'Begin Your Quest')
                sample_data['story_text'] = start_data.get('story_text', 'No story text found')
                sample_data['scene_description'] = start_data.get('description', 'No description found')
                sample_data['character_description'] = start_data.get('prompt', 'No prompt found')
            else:
                sample_data['story_text'] = 'Could not load start game data'

        return sample_data

    def reload_file(self, filename):
        """
        Force reload a specific JSON file (ignoring cache).

        Args:
            filename: Name of the JSON file to reload (str)

        Returns:
            Newly loaded content or None if error
        """
        if not filename.endswith('.json'):
            filename += '.json'

        # Remove from cache if present
        if filename in self.loaded_content:
            del self.loaded_content[filename]

        # Load fresh copy
        return self.load_file(filename)
