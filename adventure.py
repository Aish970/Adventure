import sys
import json

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
        self.game_map = {}
        self.current_location = None
        self.player_inventory = []
        self.game_running = True
        self.load_map()

    def load_map(self):
        try:
            with open(self.map_file, 'r') as file:
                map_data = json.load(file)
                rooms = map_data.get("rooms", [])
                for index, room_data in enumerate(rooms):
                    self.game_map[index] = room_data
                self.current_location = map_data.get("start", 0)  # Set the starting location index
        except FileNotFoundError:
            print(f"Error: File '{self.map_file}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{self.map_file}'.")

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

    def process_command(self, command):
        command_parts = command.split()
        base_command = command_parts[0]

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
        elif base_command == "drop":
            self.handle_drop_command(command_parts)
            return None
        elif base_command == "inventory":
            self.show_inventory()
            return None
        elif base_command == "items":
            self.show_items()
            return None
        elif base_command == "help":
            self.show_help()
            return None
        elif base_command == "exits":
            self.show_exits()
            return None
        elif base_command == "quit":
            print("Goodbye!")
            self.game_running = False
            return None
        else:
            print("Invalid command. Try 'help' for a list of valid commands.")
            return None

    def move_player(self, direction):
        current_location = self.game_map.get(self.current_location)
        if current_location:
            if direction in current_location["exits"]:
                next_location_index = current_location["exits"][direction]
                if next_location_index in self.game_map:  # Check if the next location index is valid
                    next_location = self.game_map[next_location_index]
                    # Move the player to the next location
                    self.current_location = next_location_index
                    print(f"You go {direction}.")
                    print()
                    self.look()
                    self.check_conditions()
                else:
                    print(f"There's no way to go {direction}.")
            else:
                print(f"There's no way to go {direction}.")
        else:
            print("Error: Current location data not found.")

    def check_conditions(self):
        location = self.game_map.get(self.current_location)
        if location:
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
        else:
            print("Error: Current location data not found.")

    def look(self):
        location = self.game_map.get(self.current_location)
        if location:
            self.check_conditions()
            print(f"> {location['name']}\n")
            print(f"{location['desc']}\n")
            items = location.get("items", [])
            if items:
                items_str = ", ".join(items)
                if len(items) > 1:
                    print(f"Items: {items_str}\n")
                else:
                    print(f"Items: {items_str}\n")
            exits = location.get("exits", {})
            exits_description = " ".join(exits.keys())
            print(f"Exits: {exits_description}\n")
        else:
            print("Error: Current location data not found.")

    def handle_get_command(self, command_parts):
        if len(command_parts) > 1:
            item_abbr = " ".join(command_parts[1:])
            self.get_item_by_abbr(item_abbr)
            self.check_conditions()
        else:
            print("Sorry, you need to 'get' something.")

    def get_item_by_abbr(self, item_abbr):
        location = self.game_map.get(self.current_location)
        if location:
            matching_items = [item for item in location.get("items", []) if item.lower().startswith(item_abbr.lower())]
            if len(matching_items) == 1:
                self.pick_up_item(matching_items[0])
            elif len(matching_items) > 1:
                self.ask_for_item_clarification(matching_items)
            else:
                print("There's no " + str(item_abbr) + " anywhere.")
        else:
            print("Error: Current location data not found.")

    def ask_for_item_clarification(self, matching_items):
        items_str = ", ".join(matching_items[:-1]) + f", or the {matching_items[-1]}"
        print(f"Did you want to get the {items_str}?")
        choice = input("What would you like to do? ").strip().lower()
        if choice in matching_items:
            self.pick_up_item(choice)
        else:
            print("Invalid item choice.")

    def pick_up_item(self, item_name):
        location = self.game_map.get(self.current_location)
        if location:
            if item_name in location.get("items", []):
                location["items"].remove(item_name)
                self.player_inventory.append(item_name)
                print(f"You pick up the {item_name}.")
                # Immediately check for win/lose conditions after picking up an item
                self.check_conditions()
            else:
                print(f"Error: '{item_name}' not found in current location.")
        else:
            print("Error: Current location data not found.")

    def handle_drop_command(self, command_parts):
        if len(command_parts) > 1:
            item = " ".join(command_parts[1:])
            if item in self.player_inventory:
                self.player_inventory.remove(item)
                location = self.game_map.get(self.current_location)
                if location:
                    location.setdefault("items", []).append(item)
                    print(f"You dropped the {item}.")
                else:
                    print("Error: Current location data not found.")
            else:
                print(f"You don't have {item} in your inventory.")
        else:
            print("You must specify an item to drop.")

    def show_inventory(self):
        if self.player_inventory:
            print("Inventory:")
            for i in self.player_inventory:
                print(" ", i)
        else:
            print("You're not carrying anything.")

    def show_items(self):
        location = self.game_map.get(self.current_location)
        if location:
            items = location.get("items", [])
            if items:
                print("Items in this location:", ", ".join(items))
            else:
                print("There are no items here.")
        else:
            print("Error: Current location data not found.")

    def show_exits(self):
        location = self.game_map.get(self.current_location)
        if location:
            exits = location.get("exits", {})
            if exits:
                print("Available exits:", " ".join(exits.keys()))
            else:
                print("There are no exits from here.")
        else:
            print("Error: Current location data not found.")

    def show_help(self):
        print("Available commands:")
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
        return
    map_file = sys.argv[1]
    game = AdventureGame(map_file)
    game.start_game()


if __name__ == "__main__":
    main()
