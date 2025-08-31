#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>
#include <cstdint>

using namespace std;

class VirtualMachine {
private:
    // Registers
    uint32_t PC;      // Program Counter
    uint32_t SP;      // Stack Pointer
    uint32_t A, B, C; // General purpose registers
    
    // Memory
    static const uint32_t MEMORY_SIZE = 1024;
    static const uint32_t STACK_SIZE = 256;
    static const uint32_t CODE_START = 0;
    static const uint32_t STACK_START = MEMORY_SIZE - STACK_SIZE;
    static const uint32_t DATA_START = 512;
    
    vector<uint32_t> memory;
    vector<uint32_t> stack;
    
    bool running;
    
public:
    // Instruction opcodes
    enum Opcode {
        HALT = 0,
        PUSH,
        POP,
        ADD,
        SUB,
        MUL,
        DIV,
        LOAD,
        STORE,
        MOV,
        JMP,
        JZ,
        JNZ,
        CALL,
        RET,
        PRINT,
        READ,
        NOP
    };
    
    VirtualMachine() : PC(0), SP(STACK_START), A(0), B(0), C(0), running(false) {
        memory.resize(MEMORY_SIZE, 0);
        stack.resize(STACK_SIZE, 0);
    }
    
    void loadProgram(const vector<uint32_t>& program) {
        for (size_t i = 0; i < program.size() && i < CODE_START + MEMORY_SIZE; i++) {
            memory[CODE_START + i] = program[i];
        }
    }
    
    void push(uint32_t value) {
        if (SP < STACK_START + STACK_SIZE) {
            stack[SP - STACK_START] = value;
            SP++;
        } else {
            cerr << "Stack overflow!" << endl;
            running = false;
        }
    }
    
    uint32_t pop() {
        if (SP > STACK_START) {
            SP--;
            return stack[SP - STACK_START];
        } else {
            cerr << "Stack underflow!" << endl;
            running = false;
            return 0;
        }
    }
    
    uint32_t fetch() {
        if (PC < MEMORY_SIZE) {
            return memory[PC++];
        } else {
            cerr << "Program counter out of bounds!" << endl;
            running = false;
            return HALT;
        }
    }
    
    void execute(uint32_t instruction) {
        uint32_t opcode = instruction & 0xFF;
        uint32_t operand = instruction >> 8;
        
        switch (opcode) {
            case HALT:
                running = false;
                cout << "Program halted" << endl;
                break;
                
            case PUSH:
                push(operand);
                break;
                
            case POP:
                pop();
                break;
                
            case ADD: {
                uint32_t b = pop();
                uint32_t a = pop();
                push(a + b);
                break;
            }
                
            case SUB: {
                uint32_t b = pop();
                uint32_t a = pop();
                push(a - b);
                break;
            }
                
            case MUL: {
                uint32_t b = pop();
                uint32_t a = pop();
                push(a * b);
                break;
            }
                
            case DIV: {
                uint32_t b = pop();
                uint32_t a = pop();
                if (b != 0) {
                    push(a / b);
                } else {
                    cerr << "Division by zero!" << endl;
                    running = false;
                }
                break;
            }
                
            case PRINT: {
                uint32_t value = pop();
                cout << "Output: " << value << endl;
                break;
            }
                
            case NOP:
                // Do nothing
                break;
                
            default:
                cerr << "Unknown opcode: " << opcode << endl;
                running = false;
                break;
        }
    }
    
    void run() {
        running = true;
        PC = CODE_START;
        
        cout << "Starting virtual machine..." << endl;
        
        while (running) {
            uint32_t instruction = fetch();
            execute(instruction);
            
            // Safety check to prevent infinite loops
            if (PC >= MEMORY_SIZE) {
                cerr << "Program counter exceeded memory bounds!" << endl;
                running = false;
            }
        }
        
        cout << "Virtual machine stopped" << endl;
    }
    
    void dumpState() {
        cout << "\n=== VM State Dump ===" << endl;
        cout << "PC: " << PC << endl;
        cout << "SP: " << SP << endl;
        cout << "A: " << A << ", B: " << B << ", C: " << C << endl;
        
        cout << "Stack (top 10): ";
        int start = max(0, static_cast<int>(SP - STACK_START) - 10);
        for (int i = start; i < SP - STACK_START; i++) {
            cout << stack[i] << " ";
        }
        cout << endl;
    }
};

int main() {
    cout << "Basic Virtual Machine" << endl;
    cout << "=====================" << endl;
    
    VirtualMachine vm;
    
    // Example program: (10 + 20) * 2
    vector<uint32_t> program = {
        (VirtualMachine::PUSH << 8) | 10,   // PUSH 10
        (VirtualMachine::PUSH << 8) | 20,   // PUSH 20
        VirtualMachine::ADD,                // ADD
        (VirtualMachine::PUSH << 8) | 2,    // PUSH 2
        VirtualMachine::MUL,                // MUL
        VirtualMachine::PRINT,              // PRINT
        VirtualMachine::HALT                // HALT
    };
    
    vm.loadProgram(program);
    vm.run();
    vm.dumpState();
    
    return 0;
}
