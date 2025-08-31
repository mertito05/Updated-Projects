import random
import re

class SimpleChatbot:
    def __init__(self):
        self.responses = {
            'hello': [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! Nice to meet you!"
            ],
            'how are you': [
                "I'm doing great, thank you!",
                "I'm just a program, but I'm functioning well!",
                "All systems operational! How about you?"
            ],
            'name': [
                "I'm a simple chatbot created to assist you.",
                "You can call me ChatBot!",
                "I'm your friendly neighborhood chatbot."
            ],
            'bye': [
                "Goodbye! Have a great day!",
                "See you later!",
                "Bye! Come back anytime!"
            ],
            'thanks': [
                "You're welcome!",
                "Happy to help!",
                "Anytime!"
            ],
            'default': [
                "That's interesting! Tell me more.",
                "I see. What else would you like to know?",
                "Could you rephrase that?",
                "I'm still learning. Can you ask something else?"
            ]
        }
        
        self.patterns = {
            r'hello|hi|hey': 'hello',
            r'how are you|how do you do': 'how are you',
            r'what is your name|who are you': 'name',
            r'bye|goodbye|see you': 'bye',
            r'thank|thanks|appreciate': 'thanks'
        }

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # Check for patterns
        for pattern, category in self.patterns.items():
            if re.search(pattern, user_input):
                return random.choice(self.responses[category])
        
        # Default response if no pattern matches
        return random.choice(self.responses['default'])

    def chat(self):
        print("ChatBot: Hello! I'm a simple chatbot. Type 'quit' to exit.")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("ChatBot: Goodbye!")
                break
                
            if not user_input.strip():
                print("ChatBot: Please type something!")
                continue
                
            response = self.get_response(user_input)
            print(f"ChatBot: {response}")

def main():
    chatbot = SimpleChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()
