import json

class TextAdventureGame:
    def __init__(self, map_file):
        self.map = self.load_map(map_file)
        self.current_room = self.map["start"]
        self.print_room_description(self.get_current_room_data())

    def load_map(self, map_file):
        with open(map_file, "r") as file:
            map_data = json.load(file)
            self.validate_map(map_data)
            return map_data

    def validate_map(self, map_data):
        if "start" not in map_data or "rooms" not in map_data:
            print("Invalid map: 'start' and 'rooms' keys are required.")
            exit(1)
        room_names = set()
        for room in map_data["rooms"]:
            if "name" not in room or "desc" not in room or "exits" not in room:
                print("Each room must have 'name', 'desc', and 'exits' keys.")
                exit(1)
            if room["name"] in room_names:
                print(f"Duplicate room name: {room['name']}. Room names must be unique.")
                exit(1)
            room_names.add(room["name"])
            for exit_direction, destination in room["exits"].items():
                if destination not in room_names:
                    print(f"Invalid exit in room '{room['name']}': {exit_direction} points to non-existing room '{destination}'.")
                    exit(1)

    def print_room_description(self, room_data):
        print(f"> {room_data['name']}\n")
        print(room_data["desc"])
        print("\nExits:", ", ".join(room_data["exits"].keys()))
        print("\nWhat would you like to do?")

    def execute_command(self, command):
        # Print the input command
        print("> " + command)

        # Convert the command to lowercase and split it into words
        command_parts = command.lower().split()

        # If the command is empty or None, prompt again
        if not command_parts:
            return

        # Extract the verb from the command
        verb = command_parts[0]

        # Define a list of valid verbs
        valid_verbs = ["go", "look", "inventory", "get", "quit"]

        # Check if the verb is valid
        if verb not in valid_verbs:
            print(f"Invalid command: '{verb}' is not recognized.")
            return

        # Execute the appropriate action based on the verb
        if verb == "go":
            if len(command_parts) < 2:
                print("Sorry, you need to 'go' somewhere.")
                return
            direction = " ".join(command_parts[1:])
            self.go(direction)
        elif verb == "look":
            self.look()
        elif verb == "inventory":
            self.inventory()
        elif verb == "get":
            if len(command_parts) < 2:
                print("Sorry, you need to 'get' something.")
                return
            item = " ".join(command_parts[1:])
            self.get(item)
        elif verb == "quit":
            print("Goodbye!")
            exit(0)

    def go(self, direction):
        current_room_data = self.get_current_room_data()
        exits = current_room_data["exits"]
        if direction in exits:
            self.current_room = exits[direction]
            self.print_room_description(self.get_current_room_data())
        else:
            print(f"There's no way to go {direction}.")

    def look(self):
        current_room_data = self.get_current_room_data()
        self.print_room_description(current_room_data)

    def inventory(self):
        print("You're not carrying anything.")  # Assuming inventory functionality is not implemented

    def get(self, item):
        print(f"There's no {item} anywhere.")  # Assuming item functionality is not implemented

    def get_current_room_data(self):
        for room in self.map["rooms"]:
            if room["name"] == self.current_room:
                return room
if __name__ == "__main__":
    game = TextAdventureGame("look.map")
    
    # Print initial room information
    game.look()
    
    # Enter input loop
    while True:
        command = input().strip()
        game.execute_command(command)


