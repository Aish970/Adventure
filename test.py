def main():
    print("Welcome to the Text Adventure Game!")
    print("Type 'quit' at any time to exit.")

    # Create the game instance
    game = TextAdventureGame("look.map")

    # Start the game loop
    while True:
        print("\nWhat would you like to do?")
        command = input("> ").strip().lower()

        # Check if the player wants to quit
        if command == "quit":
            game.quit()
            break

        # Process the player's command
        game.process_command(command)

if __name__ == "__main__":
    main()
