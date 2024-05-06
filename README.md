# Adventure

Adventure Game

Authors: Aishwarya Bhethanabolta
Stevens Login: abhethan@stevens.edu
GitHub Repo: Adventure

Description

This repository contains the implementation of a text-based adventure game engine that loads and lets the player interact with a game world defined by a map file in JSON format. 

Features:

Map Loading:
The game engine's map loading functionality allows for the seamless integration of maps stored in JSON files. This feature enhances the game's versatility and dynamism by enabling the creation of diverse and immersive game environments. The engine meticulously validates the map data to ensure coherence and accuracy, thus preventing any potential errors that may arise during gameplay. This robust validation process guarantees that the game world remains consistent and engaging for players.

Player Interaction:
Upon entering the game, players are transported into a captivating world comprising various rooms, each with its unique description and exits. The game engine excels at interpreting player commands, enabling smooth movement, item manipulation, and other interactions within the game universe. Whether players are exploring new areas, picking up items, or navigating through intricate puzzles, the engine facilitates these interactions seamlessly, enhancing the overall gaming experience. With intuitive controls and responsive feedback, players can fully immerse themselves in the game world and embark on exciting adventures.


Extensions:

Help Command:
Players can utilize the help command to access a comprehensive list of available commands along with their descriptions, providing valuable guidance and assistance throughout gameplay.
What would you like to do? help
Available commands:
  go [direction] - Move in the specified direction (north, south, east, west).
  get [item] - Pick up an item from the current location.
  drop [item] - Drop an item from your inventory into the current location.
  inventory - Show the items you are carrying.
  look - Describe the current location.
  items - List all items in the current location.
  exits - Show all available exits from the current location.
  help - Display this help message.
  quit - Exit the game.

Drop and Inventory System:
The game incorporates an efficient inventory system allowing players to efficiently manage their items.
Players can employ the drop [item] command to seamlessly remove items from their inventory and place them in the current location.
Furthermore, the inventory command offers players a convenient way to inspect the items they are currently carrying.
> A green room

A green room with bright green walls.

Items: banana, bandana, bellows, deck of cards

Exits: East southeast west

 What would you like to do? drop bellows
You dropped the bellows.
What would you like to do? 

Direction Verbs:
Enhancing player convenience and gameplay fluidity, the game supports both full directions (north, south, east, west) and their corresponding abbreviations.
Players can effortlessly navigate through the game world using abbreviated commands for movement, ensuring a seamless and intuitive gaming experience.base)
O/P:aishwaryabhethanabotla@Aishwaryas-MacBook-Pro ~ % cd Desktop                   
(base) aishwaryabhethanabotla@Aishwaryas-MacBook-Pro Desktop % cd Adventure-main-8          
(base) aishwaryabhethanabotla@Aishwaryas-MacBook-Pro Adventure-main-8 % python3 adventure.py loop.map

> A white room

A white room with white walls.

Exits: North northwest east

What would you like to do? go n
You go north.


> A blue room

A blue room with blue walls.

Exits: West south east

What would you like to do? 




Testing:

The game engine underwent comprehensive testing procedures, encompassing both automated and manual approaches. Automated unit tests were meticulously crafted for each module's core functionality, utilizing pytest and similar frameworks. Manual testing involved playing through various scenarios and maps to verify seamless gameplay and bug-free operation. Additionally, rigorous testing was conducted on each extension to ensure its smooth integration and functionality within the game.

Known Issues:

During the development phase, we encountered a few bugs and challenges, such as occasional difficulties with parsing JSON map files and occasional glitches in the inventory system. However, thorough testing was conducted to identify and resolve these issues. Despite these challenges, no bugs were detected during our extensive testing of the game.


Acknowledgements

I extend my heartfelt gratitude to Professor Greenberg for his invaluable guidance and unwavering support during the development of this project.
