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

    def go(self, direction):
        if direction in self.current_room["exits"]:
            next_room_name = self.current_room["exits"][direction]
            for room in self.map["rooms"]:
                if room["name"] == next_room_name:
                    self.current_room = room
                    print(f"You have moved {direction}.")
                    self.look()
                    return
            print("There is no room in that direction.")
        else:
            print("There is no exit in that direction.")

    def look(self):
        print(f"You are in {self.current_room['name']}.")
        print(self.current_room['desc'])
        if 'items' in self.current_room and self.current_room['items']:
            print("You see the following items in the room:")
            for item in self.current_room['items']:
                print(item)
        else:
            print("There are no items in this room.")
        print("Exits:")
        for direction, room_id in self.current_room['exits'].items():
            print(f"{direction}: {room_id}")

    def get(self, item):
        if 'items' in self.current_room and item in self.current_room['items']:
            self.player_inventory.append(item)
            self.current_room['items'].remove(item)
            print(f"You picked up {item}.")
        else:
            print(f"There is no {item} in this room.")

    def inventory(self):
        if self.player_inventory:
            print("Your inventory:")
            for item in self.player_inventory:
                print(item)
        else:
            print("Your inventory is empty.")

    def quit(self):
        print("Thanks for playing!")
        sys.exit(0)

    def play(self):
        while True:
            command = input("Enter a command: ").strip().lower()
            if command.startswith("go "):
                direction = command.split()[1]
                self.go(direction)
            elif command.startswith("get "):
                item = command.split()[1]
                self.get(item)
            elif command == "inventory":
                self.inventory()
            elif command == "look":
                self.look()
            elif command == "quit":
                self.quit()
            else:
                print("Invalid command.")

if __name__ == "__main__":
    game = TextAdventureGame("look.map")
    game.play()
