from main import SimpleChatbot

def test_chatbot():
    bot = SimpleChatbot()
    
    test_cases = [
        "hello",
        "how are you",
        "thank you",
        "goodbye",
        "what is python",
        "tell me something interesting"
    ]
    
    print("Testing Chatbot Responses:")
    print("=" * 40)
    
    for test_input in test_cases:
        response = bot.get_response(test_input)
        print(f"Input: '{test_input}'")
        print(f"Response: '{response}'")
        print("-" * 40)

if __name__ == "__main__":
    test_chatbot()
