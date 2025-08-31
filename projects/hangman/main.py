import random

def choose_word():
    """Choose a random word from a predefined list"""
    words = ["python", "hangman", "programming", "development", "challenge"]
    return random.choice(words)

def display_hangman(tries):
    """Display the hangman based on the number of incorrect tries"""
    stages = [
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |   
           |
        """,
        """
           ------
           |    |
           |    O
           |    
           |   
           |
        """,
        """
           ------
           |    |
           |    
           |    
           |   
           |
        """,
        """
           ------
           |    
           |    
           |    
           |   
           |
        """,
        """
           ------
           |    
           |    
           |    
           |   
           |
        """
    ]
    return stages[tries]

def play():
    """Main game function"""
    word = choose_word()
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    
    print("Let's play Hangman!")
    
    while not guessed and tries > 0:
        print(display_hangman(tries))
        print(word_completion)
        guess = input("Please guess a letter or word: ").lower()
        
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed that letter.")
            elif guess not in word:
                print("Sorry, that letter is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good job! That letter is in the word.")
                guessed_letters.append(guess)
                word_completion = "".join([letter if letter in guessed_letters else "_" for letter in word])
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed that word.")
            elif guess != word:
                print("Sorry, that is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Invalid input. Please try again.")
        
    if guessed:
        print(f"Congratulations! You guessed the word: {word}.")
    else:
        print(display_hangman(tries))
        print(f"Sorry, you ran out of tries. The word was: {word}.")

if __name__ == "__main__":
    play()
