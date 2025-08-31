# Quiz App

A multiple-choice quiz application that allows users to take quizzes and add their own questions.

## Features
- Multiple-choice quiz with randomized questions
- Score tracking and percentage calculation
- Add custom questions to the quiz database
- View all available questions
- Persistent storage using JSON file

## How to Run
```bash
python main.py
```

## Usage
1. **Start Quiz**: Take the quiz with randomized questions
2. **Add Question**: Add new questions to the quiz database
3. **View Questions**: See all available questions
4. **Exit**: Close the application

## Quiz Format
- Each question has 4 options
- Questions are shuffled for variety
- Score is calculated as percentage of correct answers

## Data Storage
Questions are stored in `quiz_data.json` with the following structure:
- question: The question text
- options: List of 4 possible answers
- correct_answer: The correct answer text

## Default Questions
The app comes with 5 default general knowledge questions:
1. Capital of France
2. Red Planet
3. Basic math
4. Shakespeare's works
5. Largest ocean

## Customization
You can easily add your own questions on any topic through the "Add Question" menu option.
