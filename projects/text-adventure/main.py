import random

class Game:
    def __init__(self):
        self.rooms = {
            'start': {
                'description': 'You are in a dark room. There is a door to the north.',
                'exits': {'north': 'hallway'}
            },
            'hallway': {
                'description': 'You are in a long hallway. There are doors to the east and west.',
                'exits': {'east': 'kitchen', 'west': 'bathroom', 'south': 'start'}
            },
            'kitchen': {
                'description': 'You are in a kitchen. There is a fridge and a table.',
                'exits': {'west': 'hallway'}
            },
            'bathroom': {
                'description': 'You are in a bathroom. There is a shower and a sink.',
                'exits': {'east': 'hallway'}
            }
        }
        self.current_room = 'start'
        self.inventory = []

    def describe_room(self):
        room = self.rooms[self.current_room]
        print(room['description'])
        print("Exits:", ', '.join(room['exits'].keys()))

    def move(self, direction):
        room = self.rooms[self.current_room]
        if direction in room['exits']:
            self.current_room = room['exits'][direction]
            self.describe_room()
        else:
            print("You can't go that way!")

    def take_item(self, item):
        if item in self.inventory:
            print(f"You already have {item}.")
        else:
            self.inventory.append(item)
            print(f"You have taken {item}.")

    def show_inventory(self):
        if self.inventory:
            print("You have:", ', '.join(self.inventory))
        else:
            print("Your inventory is empty.")

def main():
    game = Game()
    game.describe_room()

    while True:
        command = input("\n> ").strip().lower()
        if command in ['quit', 'exit']:
            print("Thanks for playing!")
            break
        elif command in ['north', 'south', 'east', 'west']:
            game.move(command)
        elif command.startswith('take '):
            item = command.split(' ', 1)[1]
            game.take_item(item)
        elif command == 'inventory':
            game.show_inventory()
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
