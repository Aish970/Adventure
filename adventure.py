import json
import sys

class TextAdventureGame:
    def __init__(self, map_file):
        self.map = self.load_map(map_file)
        self.current_room = self.map["start"]
        self.player_inventory = []

    def load_map(self, map_file):
        with open(map_file, 'r') as file:
            try:
                map_data = json.load(file)
                self.validate_map(map_data)
                return map_data
            except json.JSONDecodeError:
                sys.stderr.write("Invalid JSON format in map file.\n")
                sys.exit(1)

    def validate_map(self, map_data):
        if "start" not in map_data or "rooms" not in map_data:
            sys.stderr.write("Map file must contain 'start' and 'rooms' keys.\n")
            sys.exit(1)

        room_names = set()
        for room in map_data["rooms"]:
            if "name" not in room or "desc" not in room or "exits" not in room:
                sys.stderr.write("Each room must have 'name', 'desc', and 'exits' keys.\n")
                sys.exit(1)

            if room["name"] in room_names:
                sys.stderr.write("Room names must be unique.\n")
                sys.exit(1)
            room_names.add(room["name"])

            for direction, room_id in room["exits"].items():
                if room_id not in room_names:
                    sys.stderr.write(f"Invalid exit in room '{room['name']}': {direction} points to non-existing room.\n")
                    sys.exit(1)

    # Other methods like play, go, look, get, inventory go here...
if __name__ == "__main__":
    game = TextAdventureGame("look.map")  # Replace "look.map" with the actual filename of your map
    game.play()
