#include <iostream>
#include <vector>
#include <cmath>
#include <string>
#include <algorithm>

#define M_PI 3.14159265358979323846 // Define pi if not available

using namespace std;

class VoiceRecognition {
private:
    vector<vector<double>> commandTemplates;
    vector<string> commandNames;
    
public:
    VoiceRecognition() {
        // Initialize with some basic command templates
        commandNames = {"start", "stop", "left", "right", "up", "down"};
        
        // Simple template patterns (simulated MFCC-like features)
        commandTemplates = {
            {1.0, 2.0, 1.5, 0.8},  // start
            {0.5, 1.0, 0.8, 0.3},   // stop
            {2.0, 1.0, 1.2, 0.6},   // left
            {1.8, 0.9, 1.1, 0.7},   // right
            {1.2, 2.2, 1.8, 0.9},   // up
            {1.1, 2.1, 1.7, 0.8}    // down
        };
    }
    
    // Simulate audio processing - extract features from audio data
    vector<double> extractFeatures(const vector<double>& audioData) {
        // Simple feature extraction (simulated)
        vector<double> features;
        
        // Energy feature
        double energy = 0.0;
        for (double sample : audioData) {
            energy += sample * sample;
        }
        features.push_back(energy / audioData.size());
        
        // Zero-crossing rate
        int zeroCrossings = 0;
        for (size_t i = 1; i < audioData.size(); i++) {
            if (audioData[i] * audioData[i-1] < 0) {
                zeroCrossings++;
            }
        }
        features.push_back(static_cast<double>(zeroCrossings) / audioData.size());
        
        // Spectral centroid (simulated)
        features.push_back(0.5 + (energy / 1000.0));
        
        // Additional feature
        features.push_back(sqrt(energy));
        
        return features;
    }
    
    // Calculate Euclidean distance between two feature vectors
    double calculateDistance(const vector<double>& features1, const vector<double>& features2) {
        double distance = 0.0;
        for (size_t i = 0; i < features1.size(); i++) {
            double diff = features1[i] - features2[i];
            distance += diff * diff;
        }
        return sqrt(distance);
    }
    
    // Recognize command from audio data
    string recognizeCommand(const vector<double>& audioData) {
        if (audioData.empty()) {
            return "no_audio";
        }
        
        // Extract features from audio
        vector<double> features = extractFeatures(audioData);
        
        // Find closest matching template
        double minDistance = numeric_limits<double>::max();
        int bestMatchIndex = -1;
        
        for (size_t i = 0; i < commandTemplates.size(); i++) {
            double distance = calculateDistance(features, commandTemplates[i]);
            if (distance < minDistance) {
                minDistance = distance;
                bestMatchIndex = i;
            }
        }
        
        // Simple threshold for recognition confidence
        if (minDistance < 1.0 && bestMatchIndex != -1) {
            return commandNames[bestMatchIndex];
        } else {
            return "unknown";
        }
    }
    
    // Simulate audio recording
    vector<double> recordAudio(int durationMs = 1000, int sampleRate = 16000) {
        // Simulate recording by generating some audio-like data
        vector<double> audioData;
        int numSamples = (durationMs * sampleRate) / 1000;
        
        // Generate some simulated audio waveform
        for (int i = 0; i < numSamples; i++) {
            double time = static_cast<double>(i) / sampleRate;
            // Simulate voice with some harmonics
            double sample = sin(2 * M_PI * 200 * time) + 
                          0.5 * sin(2 * M_PI * 400 * time) +
                          0.3 * sin(2 * M_PI * 600 * time);
            audioData.push_back(sample);
        }
        
        return audioData;
    }
};

int main() {
    cout << "Voice Recognition Application" << endl;
    cout << "=============================" << endl;
    
    VoiceRecognition recognizer;
    
    // Simulate recording and recognizing different commands
    vector<string> testCommands = {"start", "stop", "left", "right", "up", "down"};
    
    for (const string& command : testCommands) {
        cout << "\nTesting command: " << command << endl;
        
        // Simulate recording audio for this command
        vector<double> audioData = recognizer.recordAudio();
        
        // Recognize the command
        string recognized = recognizer.recognizeCommand(audioData);
        
        cout << "Recognized as: " << recognized << endl;
        cout << "Accuracy: " << (recognized == command ? "CORRECT" : "INCORRECT") << endl;
    }
    
    // Test with unknown command
    cout << "\nTesting unknown command..." << endl;
    vector<double> unknownAudio = recognizer.recordAudio();
    string recognized = recognizer.recognizeCommand(unknownAudio);
    cout << "Recognized as: " << recognized << endl;
    
    cout << "\nVoice recognition demonstration completed." << endl;
    
    return 0;
}
