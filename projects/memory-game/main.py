import tkinter as tk
import random

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.root.geometry("400x400")
        
        self.cards = []
        self.flipped_cards = []
        self.matched_pairs = 0
        self.total_pairs = 8
        
        self.create_cards()
        self.create_widgets()
    
    def create_cards(self):
        """Create a list of cards with pairs"""
        card_values = list(range(1, self.total_pairs + 1)) * 2
        random.shuffle(card_values)
        self.cards = card_values
    
    def create_widgets(self):
        """Create the game grid"""
        self.buttons = []
        for i in range(4):
            row = []
            for j in range(4):
                button = tk.Button(self.root, text="", width=10, height=5,
                                   command=lambda i=i, j=j: self.flip_card(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
    
    def flip_card(self, i, j):
        """Handle card flip"""
        if len(self.flipped_cards) < 2 and self.buttons[i][j]['text'] == "":
            self.buttons[i][j]['text'] = self.cards[i * 4 + j]
            self.flipped_cards.append((i, j))
            
            if len(self.flipped_cards) == 2:
                self.root.after(1000, self.check_match)
    
    def check_match(self):
        """Check if the two flipped cards match"""
        (i1, j1), (i2, j2) = self.flipped_cards
        if self.cards[i1 * 4 + j1] == self.cards[i2 * 4 + j2]:
            self.matched_pairs += 1
            if self.matched_pairs == self.total_pairs:
                self.show_win_message()
        else:
            self.buttons[i1][j1]['text'] = ""
            self.buttons[i2][j2]['text'] = ""
        
        self.flipped_cards = []
    
    def show_win_message(self):
        """Display a win message"""
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)
        
        win_label = tk.Label(self.root, text="You Win!", font=("Arial", 24))
        win_label.grid(row=4, column=0, columnspan=4)
    
def main():
    """Main function to run the memory game"""
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
