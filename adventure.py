import sys
import json

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
                game_map = json.load(file)
                start = game_map.get("start")
                rooms = game_map.get("rooms", [])
                self.game_map = {room["name"]: room for room in rooms}
                self.current_location = start
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
                self.process_command(command)
            except EOFError:
                print("\nUse 'quit' to exit.")

    def process_command(self, command):
        command_parts = command.split()
        base_command = command_parts[0]

        if base_command in ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]:
            self.move_player(base_command)
        elif base_command == "go":
            if len(command_parts) > 1:
                direction = command_parts[1]
                self.move_player(direction)
            else:
                print("Sorry, you need to 'go' somewhere.")
        elif base_command == "look":
            self.look()
        elif base_command == "get":
            self.handle_get_command(command_parts)
        elif base_command == "drop":
            self.handle_drop_command(command_parts)
        elif base_command == "inventory":
            self.show_inventory()
        elif base_command == "items":
            self.show_items()
        elif base_command == "help":
            self.show_help()
        elif base_command == "exits":
            self.show_exits()
        elif base_command == "quit":
            print("Goodbye!")
            self.game_running = False
        else:
            print("Invalid command. Try 'help' for a list of valid commands.")

    def move_player(self, direction):
        current_location = self.game_map.get(self.current_location)
        if current_location:
            if direction in current_location["exits"]:
                next_location_name = current_location["exits"][direction]
                if next_location_name in self.game_map:
                    self.current_location = next_location_name
                    print(f"You go {direction.capitalize()}.")
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
            print(f"\n> {location['name']}")
            print(f"{location['desc']}")
            items = location.get("items", [])
            if items:
                print("Items:", ", ".join(items))
            exits = location.get("exits", {})
            exits_description = " ".join(exits.keys()).capitalize()
            print(f"Exits: {exits_description}\n")
        else:
            print("Error: Current location data not found.")

    def handle_get_command(self, command_parts):
        if len(command_parts) > 1:
            item_abbr = " ".join(command_parts[1:])
            self.get_item_by_abbr(item_abbr)
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
                print(f"There's no {item_abbr} anywhere.")
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
