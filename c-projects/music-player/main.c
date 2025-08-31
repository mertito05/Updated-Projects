#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#define MAX_SONGS 50
#define MAX_TITLE_LENGTH 100
#define MAX_ARTIST_LENGTH 100

typedef struct {
    int id;
    char title[MAX_TITLE_LENGTH];
    char artist[MAX_ARTIST_LENGTH];
    int duration; // in seconds
} Song;

Song playlist[MAX_SONGS];
int song_count = 0;

void load_sample_songs() {
    // Sample songs data
    Song songs[] = {
        {1, "Bohemian Rhapsody", "Queen", 355},
        {2, "Hotel California", "Eagles", 391},
        {3, "Sweet Child O' Mine", "Guns N' Roses", 356},
        {4, "Billie Jean", "Michael Jackson", 294},
        {5, "Smells Like Teen Spirit", "Nirvana", 301}
    };
    
    for (int i = 0; i < 5; i++) {
        playlist[song_count++] = songs[i];
    }
}

void display_playlist() {
    if (song_count == 0) {
        printf("No songs in playlist.\n");
        return;
    }
    
    printf("\n=== Playlist ===\n");
    printf("ID\tTitle\t\t\tArtist\t\tDuration\n");
    printf("------------------------------------------------------------\n");
    
    for (int i = 0; i < song_count; i++) {
        int minutes = playlist[i].duration / 60;
        int seconds = playlist[i].duration % 60;
        printf("%d\t%-20s\t%-15s\t%d:%02d\n", 
               playlist[i].id, 
               playlist[i].title, 
               playlist[i].artist,
               minutes, seconds);
    }
}

void play_song(int song_id) {
    if (song_id < 1 || song_id > song_count) {
        printf("Invalid song ID.\n");
        return;
    }
    
    Song *song = &playlist[song_id - 1];
    int minutes = song->duration / 60;
    int seconds = song->duration % 60;
    
    printf("\nNow playing: %s - %s (%d:%02d)\n", 
           song->artist, song->title, minutes, seconds);
    
    // Simulate playback with a progress bar
    printf("Progress: [");
    for (int i = 0; i < 20; i++) {
        printf("#");
        fflush(stdout);
        Sleep(100); // Simulate time passing (Windows compatible)
    }
    printf("] 100%%\n");
    printf("Playback complete!\n");
}

void add_song() {
    if (song_count >= MAX_SONGS) {
        printf("Playlist is full!\n");
        return;
    }
    
    Song new_song;
    new_song.id = song_count + 1;
    
    printf("Enter song title: ");
    scanf(" %[^\n]", new_song.title);
    printf("Enter artist: ");
    scanf(" %[^\n]", new_song.artist);
    printf("Enter duration in seconds: ");
    scanf("%d", &new_song.duration);
    
    playlist[song_count] = new_song;
    song_count++;
    printf("Song added successfully!\n");
}

int main() {
    int choice;
    int song_id;
    
    // Load sample songs
    load_sample_songs();
    
    printf("=== Simple Music Player ===\n");
    
    while (1) {
        printf("\nMenu:\n");
        printf("1. Display Playlist\n");
        printf("2. Play Song\n");
        printf("3. Add Song\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                display_playlist();
                break;
            case 2:
                printf("Enter song ID to play: ");
                scanf("%d", &song_id);
                play_song(song_id);
                break;
            case 3:
                add_song();
                break;
            case 4:
                printf("Goodbye!\n");
                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
    
    return 0;
}
