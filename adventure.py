class TextAdventureGame:
    def __init__(self, map_file):
        # Initialize game state
        self.map = load_map(map_file)
        self.current_room = self.map.start_room
        self.player_inventory = []

    def play(self):
        print(self.current_room.description)
        while True:
            command = input("What would you like to do? ").strip().lower()
            if command.startswith("go"):
                self.go(command[3:].strip())
            elif command == "look":
                self.look()
            elif command.startswith("get"):
                self.get(command[4:].strip())
            elif command == "inventory":
                self.inventory()
            elif command == "quit":
                print("Goodbye!")
                break
            else:
                print("I don't understand that command.")

    def go(self, direction):
        if direction in self.current_room.exits:
            self.current_room = self.map.rooms[self.current_room.exits[direction]]
            print(self.current_room.description)
        else:
            print("There's no way to go {}.".format(direction))

    def look(self):
        print(self.current_room.description)

    def get(self, item):
        if item in self.current_room.items:
            self.player_inventory.append(item)
            self.current_room.items.remove(item)
            print("You pick up the {}.".format(item))
        else:
            print("There's no {} here.".format(item))

    def inventory(self):
        if self.player_inventory:
            print("Inventory:")
            for item in self.player_inventory:
                print("  " + item)
        else:
            print("You're not carrying anything.")

# Example usage:
if __name__ == "__main__":
    game = TextAdventureGame("map.txt")
    game.play(
