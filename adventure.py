import json
import sys

class Room:
    def __init__(self, name, desc, exits, items=None):
        self.name = name
        self.desc = desc
        self.exits = exits
        self.items = items if items else []

class GameEngine:
    def __init__(self, map_file):
        self.rooms = self.load_map(map_file)
        self.current_room = None
        self.inventory = []

    def load_map(self, map_file):
        try:
            with open(map_file, 'r') as file:
                map_data = json.load(file)
                rooms = {}
                for room_data in map_data["rooms"]:
                    exits = room_data.get("exits", {})
                    items = room_data.get("items", [])
                    room = Room(room_data["name"], room_data["desc"], exits, items)
                    rooms[room_data["name"]] = room
                return rooms
        except FileNotFoundError:
            print(f"Error: The file '{map_file}' was not found.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: The map file is not in valid JSON format.", file=sys.stderr)
            sys.exit(1)

    def start_game(self):
        print("Welcome to the Text Adventure Game!")
        self.current_room = self.rooms["start"]
        self.describe_room()

    def describe_room(self):
        print(f"> {self.current_room.name}\n")
        print(self.current_room.desc)
        print("\nItems:", ", ".join(self.current_room.items) if self.current_room.items else "No items")
        print("Exits:", ", ".join(self.current_room.exits.keys()))

    def process_command(self, command_input):
        command_parts = command_input.strip().split(maxsplit=1)
        command_name = command_parts[0].lower()
        if command_name == "go":
            self.go(command_parts[1].lower() if len(command_parts) > 1 else "")
        elif command_name == "look":
            self.describe_room()
        elif command_name == "get":
            self.get_item(command_parts[1].lower() if len(command_parts) > 1 else "")
        elif command_name == "inventory":
            self.show_inventory()
        elif command_name == "quit":
            self.quit_game()
        else:
            print("Unknown command.")

    def go(self, direction):
        if direction in self.current_room.exits:
            next_room_name = self.current_room.exits[direction]
            if next_room_name in self.rooms:
                self.current_room = self.rooms[next_room_name]
                self.describe_room()
            else:
                print("Invalid exit.")
        else:
            print("You can't go that way.")

    def get_item(self, item):
        if item in self.current_room.items:
            self.current_room.items.remove(item)
            self.inventory.append(item)
            print(f"You picked up the {item}.")
        else:
            print("That item is not here.")

    def show_inventory(self):
        print("Inventory:", ", ".join(self.inventory) if self.inventory else "You're not carrying anything.")

    def quit_game(self):
        print("Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]", file=sys.stderr)
        sys.exit(1)

    map_file = sys.argv[1]
    game = GameEngine(map_file)
    game.start_game()
    while True:
        command_input = input("\nWhat would you like to do? ")
        game.process_command(command_input)
