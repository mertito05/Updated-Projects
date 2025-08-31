# Memory Game

A classic memory matching game where players flip cards to find matching pairs.

## Features
- **4x4 Grid**: 16 cards with 8 matching pairs
- **Randomized Layout**: Cards are shuffled for each game
- **Visual Feedback**: Cards show their values when flipped
- **Win Detection**: Game ends when all pairs are matched
- **Simple Interface**: Easy-to-use Tkinter GUI

## How to Run
```bash
python main.py
```

## Game Rules
1. Click on any card to flip it and reveal its value
2. Click on another card to try to find a matching pair
3. If the two cards match, they stay face up
4. If they don't match, they flip back over
5. Continue until all pairs are found

## Game Mechanics
- Only two cards can be flipped at a time
- Cards automatically flip back if they don't match
- Game ends with a win message when all pairs are found

## Customization
You can easily modify the game by:
- Changing the grid size
- Using images instead of numbers
- Adding a move counter or timer
- Implementing different difficulty levels

## Note
This is a basic implementation. For a more polished game, you could add:
- Card images or colors
- Score tracking
- Multiple difficulty levels
- Sound effects
- Restart button
