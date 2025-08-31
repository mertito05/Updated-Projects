import json
import os
import random
import time

QUIZ_FILE = "quiz_questions.json"

def load_questions():
    """Load quiz questions from JSON file"""
    if os.path.exists(QUIZ_FILE):
        with open(QUIZ_FILE, 'r') as file:
            return json.load(file)
    return []

def save_questions(questions):
    """Save quiz questions to JSON file"""
    with open(QUIZ_FILE, 'w') as file:
        json.dump(questions, file, indent=2)

def add_question(questions, question, options, correct_answer):
    """Add a new quiz question"""
    new_question = {
        "id": len(questions) + 1,
        "question": question,
        "options": options,
        "correct_answer": correct_answer
    }
    questions.append(new_question)
    save_questions(questions)
    print(f"Question #{new_question['id']} added successfully!")

def take_quiz(questions):
    """Take the quiz"""
    if not questions:
        print("No questions available for the quiz!")
        return
    
    print("Starting Quiz!")
    print("==============")
    
    score = 0
    total_questions = len(questions)
    
    # Shuffle questions for variety
    shuffled_questions = questions.copy()
    random.shuffle(shuffled_questions)
    
    for i, q in enumerate(shuffled_questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for j, option in enumerate(q['options'], 1):
            print(f"  {j}. {option}")
        
        try:
            user_answer = int(input("\nEnter your answer (1-4): ").strip())
            if 1 <= user_answer <= len(q['options']):
                if q['options'][user_answer - 1] == q['correct_answer']:
                    print("✅ Correct!")
                    score += 1
                else:
                    print(f"❌ Wrong! The correct answer was: {q['correct_answer']}")
            else:
                print("❌ Invalid choice! Skipping...")
        except ValueError:
            print("❌ Please enter a valid number! Skipping...")
        
        time.sleep(1)  # Brief pause between questions
    
    print(f"\nQuiz Completed!")
    print("================")
    print(f"Your score: {score}/{total_questions}")
    percentage = (score / total_questions) * 100
    print(f"Percentage: {percentage:.1f}%")
    
    if percentage >= 80:
        print("🎉 Excellent!")
    elif percentage >= 60:
        print("👍 Good job!")
    elif percentage >= 40:
        print("😊 Not bad!")
    else:
        print("💪 Keep practicing!")

def view_questions(questions):
    """View all quiz questions"""
    if not questions:
        print("No questions found!")
        return
    
    print("\nQuiz Questions:")
    print("===============")
    for q in questions:
        print(f"Question #{q['id']}: {q['question']}")
        for j, option in enumerate(q['options'], 1):
            print(f"  {j}. {option}")
        print(f"Correct Answer: {q['correct_answer']}")
        print("-" * 50)

def main():
    questions = load_questions()
    
    # Add some sample questions if none exist
    if not questions:
        sample_questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct_answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct_answer": "Mars"
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4"
            }
        ]
        questions.extend(sample_questions)
        save_questions(questions)
    
    print("Quiz Application")
    print("================")
    
    while True:
        print("\nOptions:")
        print("1. Take Quiz")
        print("2. View All Questions")
        print("3. Add New Question")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            take_quiz(questions)
        
        elif choice == "2":
            view_questions(questions)
        
        elif choice == "3":
            question = input("Enter the question: ").strip()
            options = []
            for i in range(4):
                option = input(f"Enter option {i+1}: ").strip()
                options.append(option)
            correct_answer = input("Enter the correct answer: ").strip()
            add_question(questions, question, options, correct_answer)
        
        elif choice == "4":
            print("Goodbye! Your quiz questions have been saved.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
