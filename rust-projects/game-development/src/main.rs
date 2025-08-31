use std::io;
use std::time::Duration;
use std::thread;

struct Game {
    player_x: i32,
    player_y: i32,
    score: u32,
    game_over: bool,
}

impl Game {
    fn new() -> Self {
        Game {
            player_x: 10,
            player_y: 10,
            score: 0,
            game_over: false,
        }
    }

    fn update(&mut self) {
        // Simple game logic - move player randomly
        self.player_x += rand::random::<i32>() % 3 - 1;
        self.player_y += rand::random::<i32>() % 3 - 1;
        
        // Keep player within bounds (0-20)
        self.player_x = self.player_x.clamp(0, 20);
        self.player_y = self.player_y.clamp(0, 20);
        
        // Increase score
        self.score += 1;
        
        // Simple game over condition
        if self.score > 50 {
            self.game_over = true;
        }
    }

    fn render(&self) {
        // Clear screen (simple approach)
        print!("\x1B[2J\x1B[1;1H");
        
        println!("Simple Rust Game");
        println!("Score: {}", self.score);
        println!("Player position: ({}, {})", self.player_x, self.player_y);
        
        // Draw simple grid
        for y in 0..=20 {
            for x in 0..=20 {
                if x == self.player_x && y == self.player_y {
                    print!("P");
                } else if x == 0 || x == 20 || y == 0 || y == 20 {
                    print!("#");
                } else {
                    print!(".");
                }
            }
            println!();
        }
        
        if self.game_over {
            println!("\nGame Over! Final Score: {}", self.score);
        }
    }
}

fn main() {
    let mut game = Game::new();
    
    println!("Starting simple game...");
    println!("Press Ctrl+C to exit");
    
    // Simple game loop
    while !game.game_over {
        game.update();
        game.render();
        
        // Wait a bit
        thread::sleep(Duration::from_millis(200));
        
        // Check for user input (non-blocking)
        let mut input = String::new();
        if io::stdin().read_line(&mut input).is_ok() {
            if input.trim().eq_ignore_ascii_case("quit") {
                break;
            }
        }
    }
    
    println!("Thanks for playing!");
}
