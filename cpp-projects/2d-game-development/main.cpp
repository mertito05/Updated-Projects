#include <SDL.h>
#include <iostream>
#include <string>

const int SCREEN_WIDTH = 800;
const int SCREEN_HEIGHT = 600;
const int PLAYER_SIZE = 50;
const int PLAYER_SPEED = 5;

SDL_Window* window = nullptr;
SDL_Renderer* renderer = nullptr;

class Player {
public:
    int x, y;
    int width, height;
    
    Player(int startX, int startY, int w, int h) : x(startX), y(startY), width(w), height(h) {}
    
    void move(int dx, int dy) {
        x += dx;
        y += dy;
        
        // Boundary checking
        if (x < 0) x = 0;
        if (y < 0) y = 0;
        if (x > SCREEN_WIDTH - width) x = SCREEN_WIDTH - width;
        if (y > SCREEN_HEIGHT - height) y = SCREEN_HEIGHT - height;
    }
    
    void render() {
        SDL_Rect playerRect = {x, y, width, height};
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // Red color
        SDL_RenderFillRect(renderer, &playerRect);
    }
};

bool initSDL() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cout << "SDL could not initialize! SDL_Error: " << SDL_GetError() << std::endl;
        return false;
    }
    
    window = SDL_CreateWindow("2D Game", 
                             SDL_WINDOWPOS_UNDEFINED, 
                             SDL_WINDOWPOS_UNDEFINED, 
                             SCREEN_WIDTH, 
                             SCREEN_HEIGHT, 
                             SDL_WINDOW_SHOWN);
    
    if (window == nullptr) {
        std::cout << "Window could not be created! SDL_Error: " << SDL_GetError() << std::endl;
        return false;
    }
    
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == nullptr) {
        std::cout << "Renderer could not be created! SDL_Error: " << SDL_GetError() << std::endl;
        return false;
    }
    
    return true;
}

void closeSDL() {
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
}

int main(int argc, char* args[]) {
    if (!initSDL()) {
        return 1;
    }
    
    Player player(SCREEN_WIDTH / 2 - PLAYER_SIZE / 2, 
                 SCREEN_HEIGHT / 2 - PLAYER_SIZE / 2, 
                 PLAYER_SIZE, PLAYER_SIZE);
    
    bool quit = false;
    SDL_Event e;
    
    while (!quit) {
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                quit = true;
            }
        }
        
        // Handle keyboard input
        const Uint8* currentKeyStates = SDL_GetKeyboardState(nullptr);
        if (currentKeyStates[SDL_SCANCODE_UP]) player.move(0, -PLAYER_SPEED);
        if (currentKeyStates[SDL_SCANCODE_DOWN]) player.move(0, PLAYER_SPEED);
        if (currentKeyStates[SDL_SCANCODE_LEFT]) player.move(-PLAYER_SPEED, 0);
        if (currentKeyStates[SDL_SCANCODE_RIGHT]) player.move(PLAYER_SPEED, 0);
        
        // Clear screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);
        
        // Render player
        player.render();
        
        // Update screen
        SDL_RenderPresent(renderer);
        
        // Cap the frame rate
        SDL_Delay(16); // ~60 FPS
    }
    
    closeSDL();
    return 0;
}
