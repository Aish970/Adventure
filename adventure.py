import json
import sys

abbreviations = {
    "g": ["get", "go"],
    "i": ["items", "inventory"],
    "inv": "inventory"
    # Additional abbreviations as needed
}

direction_abbreviations = {
    "n": "north",
    "e": "east",
    "s": "south",
    "w": "west",
    "ne": "northeast",
    "nw": "northwest",
    "se": "southeast",
    "sw": "southwest",
    # Extend with other abbreviations as needed
}

class AdventureGame:
    def __init__(self, map_file):
        self.map_file = map_file
        self.game_map = None
        self.current_location = None
        self.player_inventory = []
        self.game_running = True
        self.load_map()

    def load_map(self):
        try:
            with open(self.map_file, 'r') as file:
                self.game_map = json.load(file)
                # Check if the map contains any locations
                if not self.game_map:
                    print("Error: Map file does not contain any locations.")
                    sys.exit(1)
                # Ensure location indices start from 0
                if min(self.game_map.keys()) != 0:
                    print("Error: Map file does not start with location index 0.")
                    sys.exit(1)
                self.current_location = 0  # Set a default starting location index
        except FileNotFoundError:
            print("Error: Map file not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in the map file.")
            sys.exit(1)

    def start_game(self):
        self.look()
        while self.game_running:
            try:
                command = input("> ").strip().lower()
                self.process_command(command)
            except EOFError:
                print("\nUse 'quit' to exit.")

    def process_command(self, command):
        command_parts = command.split()
        base_command = command_parts[0]

        # Check if command is an abbreviation and get its full form
        if base_command in abbreviations:
            if isinstance(abbreviations[base_command], list):
                full_command = abbreviations[base_command][0]
            else:
                full_command = abbreviations[base_command]
            self.execute_command(full_command, command_parts[1:])
        else:
            self.execute_command(base_command, command_parts[1:])

    def execute_command(self, command, args):
        if command == "go":
            self.move_player(args)
        elif command == "look":
            self.look()
        elif command == "get":
            self.handle_get_command(args)
        elif command == "drop":
            self.handle_drop_command(args)
        elif command == "inventory":
            self.show_inventory()
        elif command == "items":
            self.show_items()
        elif command == "help":
            self.show_help()
        elif command == "exits":
            self.show_exits()
        elif command == "quit":
            print("Goodbye!")
            self.game_running = False
        else:
            print("Invalid command. Try 'help' for a list of valid commands.")

    def move_player(self, direction):
        current_location = self.game_map.get(self.current_location, {})
        exits = current_location.get("exits", {})
        next_location_index = exits.get(direction[0])
        if next_location_index:
            self.current_location = next_location_index
            self.look()
            self.check_conditions()
        else:
            print(f"There's no way to go {direction[0]}.")

    def check_conditions(self):
        location = self.game_map.get(self.current_location, {})
        conditions = location.get("conditions", {})

        # Check winning condition
        win_condition = conditions.get("win")
        if win_condition and win_condition["item"] in self.player_inventory:
            print(win_condition["message"])
            self.game_running = False
        elif conditions.get("lose"):
            lose_condition = conditions.get("lose")
            print(lose_condition["message"])
            self.game_running = False

    def look(self):
        location = self.game_map.get(self.current_location, {})
        self.check_conditions()
        print(f"\n> {location.get('name', '')}\n")
        print(f"{location.get('desc', '')}\n")
        items = location.get("items", [])
        if items:
            print("Items:", ", ".join(items))
        else:
            print("No items in this location.")
        exits = location.get("exits", {})
        exits_description = ", ".join(exits.keys())
        print(f"Exits: {exits_description}")

    def handle_get_command(self, args):
        if args:
            item_abbr = args[0]
            self.get_item_by_abbr(item_abbr)
            self.check_conditions()
        else:
            print("Sorry, you need to 'get' something.")

    def get_item_by_abbr(self, item_abbr):
        location = self.game_map.get(self.current_location, {})
        matching_items = [item for item in location.get("items", []) if item.lower().startswith(item_abbr.lower())]
        if len(matching_items) == 1:
            self.pick_up_item(matching_items[0])
        elif len(matching_items) > 1:
            self.ask_for_item_clarification(matching_items)
        else:
            print(f"There's no {item_abbr} anywhere.")

    def ask_for_item_clarification(self, matching_items):
        print(f"Did you want to get the {' '.join(matching_items)}?")
        choice = input("What would you like to do? ").strip().lower()
        if choice in matching_items:
            self.pick_up_item(choice)
        else:
            print("Invalid item choice.")

    def pick_up_item(self, item_name):
        location = self.game_map.get(self.current_location, {})
        if item_name in location.get("items", []):
            location["items"].remove(item_name)
            self.player_inventory.append(item_name)
            print(f"You pick up the {item_name}.")
            self.check_conditions()

    def handle_drop_command(self, args):
        if args:
            item = args[0]
            if item in self.player_inventory:
                self.player_inventory.remove(item)
                self.game_map.setdefault(self.current_location, {}).setdefault("items", []).append(item)
                print(f"You dropped the {item}.")
            else:
                print(f"You don't have {item} in your inventory.")
        else:
            print("You must specify an item to drop.")

    def show_inventory(self):
        if self.player_inventory:
            print("\nInventory:")
            for item in self.player_inventory:
                print("  ", item)
        else:
            print("\nYou're not carrying anything.")

    def show_items(self):
        location = self.game_map.get(self.current_location, {})
        items = location.get("items", [])
        if items:
            print("\nItems in this location:", ", ".join(items))
        else:
            print("\nThere are no items here.")

    def show_exits(self):
        location = self.game_map.get(self.current_location, {})
        exits = location.get("exits", {})
        if exits:
            print("\nExits:", ", ".join(exits.keys()))
        else:
            print("\nThere are no exits from here.")

    def show_help(self):
        print("\nAvailable commands:")
        print("  go [direction] - Move in the specified direction (north, south, east, west).")
        print("  get [item] - Pick up an item from the current location.")
        print("  drop [item] - Drop an item from your inventory into the current location.")
        print("  inventory - Show the items you are carrying.")
        print("  look - Describe the current location.")
        print("  items - List all items in the current location.")
        print("  exits - Show all available exits from the current location.")
        print("  help - Display this help message.")
        print("  quit - Exit the game.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 adventure.py [map_file]")
        sys.exit(1)
    map_file = sys.argv[1]
    game = AdventureGame(map_file)
    game.start_game()

if __name__ == "__main__":
    main()
