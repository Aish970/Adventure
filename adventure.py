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
        self.current_location = 0
        self.player_inventory = []
        self.game_running = True
        self.load_map()

    def load_map(self):
        with open(self.map_file, 'r') as file:
            self.game_map = json.load(file)
        print("Game map loaded successfully:", self.game_map)

    def start_game(self):
        self.look()
        while self.game_running:
            try:
                print("What would you like to do?", end=" ")
                command = input().strip().lower()
                new_location = self.process_command(command)
                while new_location:
                    print("What would you like to do?", end=" ")
                    command = input().strip().lower()
                    new_location = self.process_command(command)
            except EOFError:
                print("\nUse 'quit' to exit.")
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def process_command(self, command):
        command_parts = command.split()
        base_command = command_parts[0]
        print("Base command:", base_command)

        # Check if command is an abbreviation and get its full form
        if base_command in direction_abbreviations.values() or base_command in direction_abbreviations:
            return self.move_player(direction_abbreviations.get(base_command, base_command))
        elif base_command == "go":
            # Handle 'go' followed by a direction
            if len(command_parts) > 1:
                direction = direction_abbreviations.get(command_parts[1], command_parts[1])
                return self.move_player(direction)
            else:
                print("Sorry, you need to 'go' somewhere.")
                return None
        elif base_command == "look":
            self.look()
            return None
        elif base_command == "get":
            self.handle_get_command(command_parts)
            return None
        elif base_command == "inventory" or base_command == "inv":
            self.show_inventory()
            return None
        elif base_command == "quit":
            print("Goodbye!")
            self.game_running = False
            return None
        else:
            print("Invalid command. Try 'help' for a list of valid commands.")
            return None

    def move_player(self, direction):
        current_location = self.game_map[self.current_location]
        print("Current location:", current_location)
        if direction in current_location["exits"]:
            next_location_index = current_location["exits"][direction]
            self.current_location = next_location_index
            print(f"You go {direction}. Current location index: {self.current_location}")
            self.look()
        else:
            print(f"There's no way to go {direction}.\n")

    def look(self):
        location = self.game_map[self.current_location]
        print(f"> {location['name']}\n")
        print(f"{location['desc']}\n")
        items = location.get("items", [])
        if items:
            print("Items:", ", ".join(items))
        exits = location.get("exits", {})
        exits_description = " ".join(exits.keys())
        print(f"Exits: {exits_description}\n")

    def handle_get_command(self, command_parts):
        if len(command_parts) > 1:
            item_abbr = " ".join(command_parts[1:])
            self.get_item_by_abbr(item_abbr)
        else:
            print("Sorry, you need to 'get' something.")

    def get_item_by_abbr(self, item_abbr):
        location = self.game_map[self.current_location]
        matching_items = [item for item in location.get("items", []) if item.lower().startswith(item_abbr.lower())]
        if len(matching_items) == 1:
            self.pick_up_item(matching_items[0])
        elif len(matching_items) > 1:
            self.ask_for_item_clarification(matching_items)
        else:
            print(f"There's no {item_abbr} anywhere.")

    def ask_for_item_clarification(self, matching_items):
        print(f"Did you want to get the {' or '.join(matching_items)}?")
        choice = input("What would you like to do? ").strip().lower()
        if choice in matching_items:
            self.pick_up_item(choice)
        else:
            print("Invalid item choice.")

    def pick_up_item(self, item_name):
        location = self.game_map[self.current_location]
        if item_name in location.get("items", []):
            location["items"].remove(item_name)
            self.player_inventory.append(item_name)
            print(f"You pick up the {item_name}.")
        else:
            print(f"There's no {item_name} here.")

    def show_inventory(self):
        if self.player_inventory:
            print("Inventory:")
            for item in self.player_inventory:
                print(f"  {item}")
        else:
            print("You're not carrying anything.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 adventure.py [map_file]")
        return
    map_file = sys.argv[1]
    game = AdventureGame(map_file)
    game.start_game()

if __name__ == "__main__":
    main()
