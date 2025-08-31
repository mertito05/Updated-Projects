# Hangman Game

A classic text-based Hangman game where players guess letters to reveal a hidden word.

## Features
- **Random Word Selection**: Words chosen from a predefined list
- **Visual Hangman**: ASCII art display of the hangman figure
- **Letter and Word Guessing**: Guess individual letters or the entire word
- **Input Validation**: Ensures valid guesses and prevents duplicates
- **6 Tries**: Traditional hangman rules with 6 incorrect guesses allowed

## How to Run
```bash
python main.py
```

## Game Rules
1. A random word is chosen from the word list
2. Players guess letters one at a time
3. Correct letters are revealed in the word
4. Incorrect guesses reduce the number of remaining tries
5. Players can also guess the entire word
6. Game ends when the word is guessed or tries run out

## Word List
The game includes these words:
- python
- hangman
- programming
- development
- challenge

## Hangman Stages
The game displays different stages of the hangman figure:
- 6 tries remaining: No hangman
- 5 tries: Head
- 4 tries: Head and body
- 3 tries: Head, body, and one arm
- 2 tries: Head, body, and both arms
- 1 try: Head, body, arms, and one leg
- 0 tries: Complete hangman figure

## Customization
You can easily modify the game by:
- Adding more words to the word list
- Changing the number of allowed tries
- Adding difficulty levels
- Implementing a scoring system

## Example Gameplay
```
Let's play Hangman!
_____
Please guess a letter or word: a
Good job! That letter is in the word.
_ a _ _ _
Please guess a letter or word: e
Sorry, that letter is not in the word.
