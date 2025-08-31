# Simple Chatbot

A basic rule-based chatbot that uses pattern matching and predefined responses to engage in conversations.

## Features
- Pattern-based response generation
- Handles greetings, farewells, questions, and general conversation
- Preprocesses user input for better matching
- Random response selection for variety
- Simple command-line interface

## How it Works
The chatbot uses regular expressions to match user input against predefined patterns and selects appropriate responses from categorized response sets.

## Response Categories
- Greetings (hello, hi, hey, etc.)
- Farewells (bye, goodbye, etc.)
- How are you questions
- Thank you expressions
- General questions
- Default responses

## How to Run
```bash
python main.py
```

## Usage
- Start a conversation by typing messages
- The chatbot will respond based on pattern matching
- Type 'quit', 'exit', or 'bye' to end the conversation

## Customization
You can customize the chatbot by:
1. Modifying the `responses.json` file (if it exists)
2. Adding new patterns and responses in the code
3. Extending the pattern matching logic

## Note
This is a simple rule-based chatbot. For more advanced natural language processing, consider using libraries like NLTK, spaCy, or machine learning approaches.
