#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sstream>

enum TokenType {
    TOKEN_IDENTIFIER,
    TOKEN_NUMBER,
    TOKEN_OPERATOR,
    TOKEN_ASSIGN,
    TOKEN_PRINT,
    TOKEN_EOF
};

struct Token {
    TokenType type;
    std::string value;
    int line;
};

class Lexer {
private:
    std::string source;
    size_t position;
    int line;
    
public:
    Lexer(const std::string& src) : source(src), position(0), line(1) {}
    
    Token getNextToken() {
        while (position < source.size()) {
            char current = source[position];
            
            // Skip whitespace
            if (isspace(current)) {
                if (current == '\n') line++;
                position++;
                continue;
            }
            
            // Identifier or keyword
            if (isalpha(current)) {
                std::string identifier;
                while (position < source.size() && isalnum(source[position])) {
                    identifier += source[position++];
                }
                
                if (identifier == "print") {
                    return {TOKEN_PRINT, identifier, line};
                }
                return {TOKEN_IDENTIFIER, identifier, line};
            }
            
            // Number
            if (isdigit(current)) {
                std::string number;
                while (position < source.size() && isdigit(source[position])) {
                    number += source[position++];
                }
                return {TOKEN_NUMBER, number, line};
            }
            
            // Operators and assignment
            if (current == '=') {
                position++;
                return {TOKEN_ASSIGN, "=", line};
            }
            
            if (current == '+' || current == '-' || current == '*' || current == '/') {
                std::string op(1, current);
                position++;
                return {TOKEN_OPERATOR, op, line};
            }
            
            // Unknown character
            std::string unknown(1, current);
            position++;
            return {TOKEN_OPERATOR, unknown, line};
        }
        
        return {TOKEN_EOF, "", line};
    }
};

class Parser {
private:
    Lexer& lexer;
    Token currentToken;
    std::map<std::string, int> variables;
    
    void eat(TokenType type) {
        if (currentToken.type == type) {
            currentToken = lexer.getNextToken();
        } else {
            std::cout << "Syntax error at line " << currentToken.line << std::endl;
            exit(1);
        }
    }
    
    int factor() {
        Token token = currentToken;
        if (token.type == TOKEN_NUMBER) {
            eat(TOKEN_NUMBER);
            return std::stoi(token.value);
        } else if (token.type == TOKEN_IDENTIFIER) {
            eat(TOKEN_IDENTIFIER);
            return variables[token.value];
        }
        return 0;
    }
    
    int term() {
        int result = factor();
        
        while (currentToken.type == TOKEN_OPERATOR && 
               (currentToken.value == "*" || currentToken.value == "/")) {
            Token op = currentToken;
            eat(TOKEN_OPERATOR);
            
            if (op.value == "*") {
                result *= factor();
            } else {
                result /= factor();
            }
        }
        
        return result;
    }
    
    int expr() {
        int result = term();
        
        while (currentToken.type == TOKEN_OPERATOR && 
               (currentToken.value == "+" || currentToken.value == "-")) {
            Token op = currentToken;
            eat(TOKEN_OPERATOR);
            
            if (op.value == "+") {
                result += term();
            } else {
                result -= term();
            }
        }
        
        return result;
    }
    
public:
    Parser(Lexer& l) : lexer(l) {
        currentToken = lexer.getNextToken();
    }
    
    void parse() {
        while (currentToken.type != TOKEN_EOF) {
            if (currentToken.type == TOKEN_PRINT) {
                eat(TOKEN_PRINT);
                std::string varName = currentToken.value;
                eat(TOKEN_IDENTIFIER);
                std::cout << variables[varName] << std::endl;
            } else if (currentToken.type == TOKEN_IDENTIFIER) {
                std::string varName = currentToken.value;
                eat(TOKEN_IDENTIFIER);
                eat(TOKEN_ASSIGN);
                int value = expr();
                variables[varName] = value;
            }
        }
    }
};

int main() {
    std::string source = 
        "x = 5\n"
        "y = 10\n"
        "z = x + y\n"
        "print z\n";
    
    std::cout << "=== Simple Compiler ===\n";
    std::cout << "Source code:\n" << source << std::endl;
    
    Lexer lexer(source);
    Parser parser(lexer);
    
    std::cout << "Execution result:\n";
    parser.parse();
    
    return 0;
}
