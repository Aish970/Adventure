import json
import sys

class Room:
    def __init__(self, name, desc, exits, items=None, locked=False, key=None):
        self.name = name
        self.desc = desc
        self.exits = exits
        self.items = items if items else []
        self.locked = locked
        self.key = key

class AdventureGame:
    def __init__(self, map_file):
        self.map_file = map_file
        self.game_map = None
        self.current_room = None
        self.player_inventory = []
        self.game_running = True
        self.load_map()

    def load_map(self):
        try:
            with open(self.map_file, 'r') as file:
                data = json.load(file)
                self.game_map = {room["name"]: Room(**room) for room in data["rooms"]}
                self.current_room = self.game_map[data["start"]]
        except FileNotFoundError:
            print("Error: Map file not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in the map file.")
            sys.exit(1)

    def start_game(self):
        print("Welcome to the Text Adventure Game!\n")
        self.describe_room(self.current_room)
        while self.game_running:
            try:
                command = input("> ").strip().lower()
                self.process_command(command)
            except EOFError:
                print("\nUse 'quit' to exit.")

    def process_command(self, command):
        command_parts = command.split()
        base_command = command_parts[0]

        if base_command == "go":
            if len(command_parts) < 2:
                print("Go where?")
                return
            direction = command_parts[1]
            self.move(direction)
        elif base_command == "get":
            if len(command_parts) < 2:
                print("Get what?")
                return
            item_name = " ".join(command_parts[1:])
            self.get_item(item_name)
        elif base_command == "look":
            self.describe_room(self.current_room)
        elif base_command == "inventory":
            self.show_inventory()
        elif base_command == "quit":
            print("Goodbye!")
            self.game_running = False
        else:
            print("Invalid command. Type 'help' for a list of commands.")

    def move(self, direction):
        next_room_name = self.current_room.exits.get(direction)
        if next_room_name:
            next_room = self.game_map.get(next_room_name)
            if next_room:
                self.current_room = next_room
                self.describe_room(self.current_room)
            else:
                print("Error: Invalid room name in the map file.")
        else:
            print("You can't go that way.")

    def get_item(self, item_name):
        if item_name in self.current_room.items:
            self.current_room.items.remove(item_name)
            self.player_inventory.append(item_name)
            print(f"You picked up {item_name}.")
        else:
            print(f"{item_name} is not here.")

    def show_inventory(self):
        if self.player_inventory:
            print("Inventory:")
            for item in self.player_inventory:
                print("-", item)
        else:
            print("Your inventory is empty.")

    def describe_room(self, room):
        print(f"\n> {room.name}\n\n{room.desc}\n")
        if room.items:
            print("Items in the room:", ", ".join(room.items))
        exits = ", ".join(room.exits.keys())
        print(f"Exits: {exits}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 adventure.py [map_file]")
        sys.exit(1)
    map_file = sys.argv[1]
    game = AdventureGame(map_file)
    game.start_game()

if __name__ == "__main__":
    main()
