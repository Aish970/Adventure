import sys
import json

class TextAdventureGame:
    def __init__(self, map_file):
        self.rooms = {}
        self.current_room = None
        self.inventory = []
        self.load_map(map_file)

    def load_map(self, map_file):
        with open(map_file, "r") as file:
            map_data = json.load(file)
            self.rooms = {room["name"]: room for room in map_data["rooms"]}
            self.current_room = map_data["start"]

    def print_room_description(self):
        current_room_data = self.rooms[self.current_room]
        print(f"> {current_room_data['name']}\n")
        print(current_room_data["desc"])
        if "items" in current_room_data:
            print("\nItems:", ", ".join(current_room_data["items"]))
        print("\nExits:", ", ".join(current_room_data["exits"].keys()))
        print("\nWhat would you like to do?")

    def execute_command(self, command):
        command = command.strip().lower()
        if not command:
            return
        if command == "quit":
            print("Goodbye!")
            sys.exit(0)
        elif command == "look":
            self.print_room_description()
        elif command.startswith("go "):
            direction = command[3:]
            self.go(direction)
        elif command.startswith("get "):
            item = command[4:]
            self.get(item)
        elif command == "inventory":
            self.show_inventory()
        else:
            print(f"Invalid command: '{command}' is not recognized.")

    def go(self, direction):
        current_room_data = self.rooms[self.current_room]
        exits = current_room_data["exits"]
        if direction in exits:
            self.current_room = exits[direction]
            self.print_room_description()
        else:
            print(f"There's no way to go {direction}.")

    def get(self, item):
        current_room_data = self.rooms[self.current_room]
        if "items" in current_room_data and item in current_room_data["items"]:
            print(f"You pick up the {item}.")
            current_room_data["items"].remove(item)
            self.inventory.append(item)
        else:
            print(f"There's no {item} anywhere.")

    def show_inventory(self):
        if self.inventory:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")
        else:
            print("You're not carrying anything.")

if __name__ == "__main__":
    map_file = "look.map"  # Change this to your map filename
    game = TextAdventureGame(map_file)
    game.print_room_description()
    while True:
        command = input().strip()
        game.execute_command(command)

