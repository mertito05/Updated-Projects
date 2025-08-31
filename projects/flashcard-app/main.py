import json
import os
import random

FLASHCARD_FILE = "flashcards.json"

def load_flashcards():
    """Load flashcards from JSON file"""
    if os.path.exists(FLASHCARD_FILE):
        with open(FLASHCARD_FILE, 'r') as file:
            return json.load(file)
    return []

def save_flashcards(flashcards):
    """Save flashcards to JSON file"""
    with open(FLASHCARD_FILE, 'w') as file:
        json.dump(flashcards, file, indent=2)

def add_flashcard(flashcards, front, back, category):
    """Add a new flashcard"""
    flashcard = {
        "id": len(flashcards) + 1,
        "front": front,
        "back": back,
        "category": category,
        "correct_count": 0,
        "incorrect_count": 0
    }
    flashcards.append(flashcard)
    save_flashcards(flashcards)
    print(f"Flashcard #{flashcard['id']} added successfully!")

def study_flashcards(flashcards):
    """Study flashcards"""
    if not flashcards:
        print("No flashcards available to study!")
        return
    
    print("Flashcard Study Session")
    print("=======================")
    
    # Filter flashcards that need more practice
    practice_flashcards = [fc for fc in flashcards if fc['incorrect_count'] > fc['correct_count']]
    
    if not practice_flashcards:
        practice_flashcards = flashcards.copy()
    
    random.shuffle(practice_flashcards)
    
    correct = 0
    total = len(practice_flashcards)
    
    for i, card in enumerate(practice_flashcards, 1):
        print(f"\nCard {i}/{total}")
        print(f"Category: {card['category']}")
        print(f"Front: {card['front']}")
        input("Press Enter to reveal the back...")
        print(f"Back: {card['back']}")
        
        answer = input("\nDid you get it right? (y/n): ").strip().lower()
        if answer == 'y':
            card['correct_count'] += 1
            print("✅ Correct!")
            correct += 1
        else:
            card['incorrect_count'] += 1
            print("❌ Incorrect - study this one more!")
        
        save_flashcards(flashcards)
    
    print(f"\nStudy session completed!")
    print(f"Score: {correct}/{total} ({correct/total*100:.1f}%)")

def view_flashcards(flashcards):
    """View all flashcards"""
    if not flashcards:
        print("No flashcards found!")
        return
    
    print("\nYour Flashcards:")
    print("================")
    for card in flashcards:
        print(f"Card #{card['id']}: {card['category']}")
        print(f"Front: {card['front']}")
        print(f"Back: {card['back']}")
        print(f"Stats: ✅ {card['correct_count']} ❌ {card['incorrect_count']}")
        print("-" * 50)

def view_stats(flashcards):
    """View study statistics"""
    if not flashcards:
        print("No flashcards found!")
        return
    
    total_cards = len(flashcards)
    total_correct = sum(card['correct_count'] for card in flashcards)
    total_incorrect = sum(card['incorrect_count'] for card in flashcards)
    total_attempts = total_correct + total_incorrect
    
    print("\nStudy Statistics")
    print("================")
    print(f"Total flashcards: {total_cards}")
    print(f"Total correct answers: {total_correct}")
    print(f"Total incorrect answers: {total_incorrect}")
    print(f"Total study attempts: {total_attempts}")
    
    if total_attempts > 0:
        accuracy = (total_correct / total_attempts) * 100
        print(f"Overall accuracy: {accuracy:.1f}%")
    
    # Show cards that need more practice
    weak_cards = [card for card in flashcards if card['incorrect_count'] > card['correct_count']]
    if weak_cards:
        print(f"\nCards needing more practice: {len(weak_cards)}")
        for card in weak_cards[:5]:  # Show top 5
            print(f"  - {card['front']} (✅{card['correct_count']} ❌{card['incorrect_count']})")

def main():
    flashcards = load_flashcards()
    
    # Add some sample flashcards if none exist
    if not flashcards:
        sample_flashcards = [
            {
                "front": "What is the capital of France?",
                "back": "Paris",
                "category": "Geography"
            },
            {
                "front": "2 + 2 = ?",
                "back": "4",
                "category": "Math"
            },
            {
                "front": "Chemical symbol for water",
                "back": "H₂O",
                "category": "Science"
            }
        ]
        for card in sample_flashcards:
            add_flashcard(flashcards, card['front'], card['back'], card['category'])
    
    print("Flashcard Application")
    print("====================")
    
    while True:
        print("\nOptions:")
        print("1. Study Flashcards")
        print("2. View All Flashcards")
        print("3. Add New Flashcard")
        print("4. View Statistics")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            study_flashcards(flashcards)
        
        elif choice == "2":
            view_flashcards(flashcards)
        
        elif choice == "3":
            front = input("Enter front of flashcard: ").strip()
            back = input("Enter back of flashcard: ").strip()
            category = input("Enter category: ").strip()
            add_flashcard(flashcards, front, back, category)
        
        elif choice == "4":
            view_stats(flashcards)
        
        elif choice == "5":
            print("Goodbye! Your flashcards have been saved.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
