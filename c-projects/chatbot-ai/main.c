#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_INPUT 256

// Function to convert string to lowercase
void to_lowercase(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

// Function to check if a string contains a substring
int contains(const char *str, const char *substr) {
    return strstr(str, substr) != NULL;
}

// Function to get chatbot response based on input
const char *get_response(const char *input) {
    char lower_input[MAX_INPUT];
    strcpy(lower_input, input);
    to_lowercase(lower_input);
    
    // Greeting patterns
    if (contains(lower_input, "hello") || contains(lower_input, "hi") || 
        contains(lower_input, "hey") || contains(lower_input, "greetings")) {
        return "Hello! How can I help you today?";
    }
    
    // Goodbye patterns
    if (contains(lower_input, "bye") || contains(lower_input, "goodbye") ||
        contains(lower_input, "exit") || contains(lower_input, "quit")) {
        return "Goodbye! It was nice talking to you.";
    }
    
    // Name patterns
    if (contains(lower_input, "name") || contains(lower_input, "who are you")) {
        return "I'm a simple chatbot created to demonstrate basic AI concepts.";
    }
    
    // How are you patterns
    if (contains(lower_input, "how are you") || contains(lower_input, "how do you feel")) {
        return "I'm just a program, but I'm functioning well! How about you?";
    }
    
    // Help patterns
    if (contains(lower_input, "help") || contains(lower_input, "what can you do")) {
        return "I can respond to basic greetings, questions about myself, and simple conversations. Try asking me about my name or how I'm doing!";
    }
    
    // Weather patterns
    if (contains(lower_input, "weather") || contains(lower_input, "temperature")) {
        return "I don't have access to real-time weather data, but I hope it's nice where you are!";
    }
    
    // Time patterns
    if (contains(lower_input, "time") || contains(lower_input, "what time")) {
        return "I don't have a clock, but you can check your device for the current time!";
    }
    
    // Question patterns
    if (contains(lower_input, "what") || contains(lower_input, "how") || 
        contains(lower_input, "why") || contains(lower_input, "when")) {
        return "That's an interesting question! I'm still learning, so I might not have the best answer.";
    }
    
    // Default response for unknown inputs
    return "I'm not sure how to respond to that. Could you try asking something else?";
}

int main() {
    char input[MAX_INPUT];
    
    printf("=== Simple Chatbot ===\n");
    printf("Type 'exit' to quit the conversation.\n\n");
    
    while (1) {
        printf("You: ");
        if (fgets(input, MAX_INPUT, stdin) == NULL) {
            break;
        }
        
        // Remove newline character
        input[strcspn(input, "\n")] = 0;
        
        // Check for exit command
        char lower_input[MAX_INPUT];
        strcpy(lower_input, input);
        to_lowercase(lower_input);
        
        if (contains(lower_input, "exit") || contains(lower_input, "quit") ||
            contains(lower_input, "bye") || contains(lower_input, "goodbye")) {
            printf("Chatbot: Goodbye! Thanks for chatting with me.\n");
            break;
        }
        
        // Get and display response
        const char *response = get_response(input);
        printf("Chatbot: %s\n\n", response);
    }
    
    return 0;
}
