#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <memory>
#include <chrono>
#include <thread>

class Process {
public:
    int pid;
    std::string name;
    int priority;
    int burst_time;
    int memory_required;
    
    Process(int id, const std::string& n, int prio, int burst, int mem)
        : pid(id), name(n), priority(prio), burst_time(burst), memory_required(mem) {}
    
    void execute() {
        std::cout << "Executing process " << name << " (PID: " << pid << ")" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(burst_time));
        std::cout << "Process " << name << " completed." << std::endl;
    }
};

class MemoryManager {
private:
    int total_memory;
    int available_memory;
    
public:
    MemoryManager(int total) : total_memory(total), available_memory(total) {}
    
    bool allocate(int size) {
        if (size <= available_memory) {
            available_memory -= size;
            return true;
        }
        return false;
    }
    
    void deallocate(int size) {
        available_memory += size;
    }
    
    int get_available_memory() const {
        return available_memory;
    }
};

class Scheduler {
private:
    std::queue<std::shared_ptr<Process>> ready_queue;
    MemoryManager& memory_manager;
    
public:
    Scheduler(MemoryManager& mm) : memory_manager(mm) {}
    
    void add_process(std::shared_ptr<Process> process) {
        if (memory_manager.allocate(process->memory_required)) {
            ready_queue.push(process);
            std::cout << "Process " << process->name << " added to ready queue." << std::endl;
        } else {
            std::cout << "Not enough memory for process " << process->name << std::endl;
        }
    }
    
    void run() {
        while (!ready_queue.empty()) {
            auto process = ready_queue.front();
            ready_queue.pop();
            
            process->execute();
            memory_manager.deallocate(process->memory_required);
        }
    }
};

class FileSystem {
private:
    struct File {
        std::string name;
        std::string content;
        int size;
    };
    
    std::vector<File> files;
    
public:
    void create_file(const std::string& name, const std::string& content) {
        File file{name, content, static_cast<int>(content.size())};
        files.push_back(file);
        std::cout << "Created file: " << name << " (" << content.size() << " bytes)" << std::endl;
    }
    
    void list_files() {
        std::cout << "\nFile System Contents:" << std::endl;
        std::cout << "====================" << std::endl;
        for (const auto& file : files) {
            std::cout << file.name << " - " << file.size << " bytes" << std::endl;
        }
    }
};

int main() {
    std::cout << "=== Basic Operating System Simulation ===" << std::endl;
    
    // Initialize system components
    MemoryManager memory_manager(1024); // 1KB total memory
    Scheduler scheduler(memory_manager);
    FileSystem file_system;
    
    // Create some processes
    auto p1 = std::make_shared<Process>(1, "Browser", 1, 2, 256);
    auto p2 = std::make_shared<Process>(2, "Text Editor", 2, 1, 128);
    auto p3 = std::make_shared<Process>(3, "Calculator", 3, 1, 64);
    
    // Add processes to scheduler
    scheduler.add_process(p1);
    scheduler.add_process(p2);
    scheduler.add_process(p3);
    
    // Create some files
    file_system.create_file("document.txt", "Hello, this is a sample document.");
    file_system.create_file("notes.md", "# Important Notes\n- Meeting at 2PM\n- Finish project");
    
    // Run the scheduler
    std::cout << "\nStarting process execution..." << std::endl;
    scheduler.run();
    
    // List files
    file_system.list_files();
    
    std::cout << "\nSimulation completed." << std::endl;
    return 0;
}
