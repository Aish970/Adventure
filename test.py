from adventure import TextAdventureGame

def play_game(map_file):
    game = TextAdventureGame(map_file)
    print("Welcome to the Text Adventure Game!")
    print("Type 'quit' at any time to exit.")

    while True:
        command = input("\nEnter a command: ").strip().lower()
        if command == "quit":
            game.quit()
        else:
            game.play_command(command)

if __name__ == "__main__":
    map_file = input("Enter the filename of the map file: ")
    play_game(map_file)
