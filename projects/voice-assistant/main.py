import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        
        # Set voice properties
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female
        self.engine.setProperty('rate', 150)
        
        self.greetings = [
            "Hello! How can I help you?",
            "Hi there! What can I do for you?",
            "Hey! Ready to assist you.",
            "Greetings! How may I be of service?"
        ]
        
        self.responses = {
            'time': self.get_time,
            'date': self.get_date,
            'search': self.search_web,
            'open': self.open_application,
            'joke': self.tell_joke,
            'weather': self.get_weather,
            'news': self.get_news
        }
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice input"""
        try:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("Processing...")
            text = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
            
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError:
            self.speak("Sorry, I'm having trouble with the speech service.")
            return ""
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything. Please try again.")
            return ""
    
    def get_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        self.speak(f"The current time is {time_str}")
    
    def get_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        self.speak(f"Today is {date_str}")
    
    def search_web(self, query):
        """Search the web"""
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        self.speak(f"Here are the search results for {query}")
    
    def open_application(self, app_name):
        """Open applications"""
        apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'browser': 'chrome.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe'
        }
        
        if app_name in apps:
            os.system(f"start {apps[app_name]}")
            self.speak(f"Opening {app_name}")
        else:
            self.speak(f"Sorry, I don't know how to open {app_name}")
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
        joke = random.choice(jokes)
        self.speak(joke)
    
    def get_weather(self):
        """Get weather information"""
        self.speak("I'm sorry, weather functionality is not implemented yet. You can ask me to search for weather information instead.")
    
    def get_news(self):
        """Get news headlines"""
        self.speak("I'm sorry, news functionality is not implemented yet. You can ask me to search for news instead.")
    
    def process_command(self, command):
        """Process voice commands"""
        command = command.lower()
        
        if any(word in command for word in ['hello', 'hi', 'hey']):
            self.speak(random.choice(self.greetings))
        
        elif 'time' in command:
            self.get_time()
        
        elif 'date' in command:
            self.get_date()
        
        elif 'search' in command:
            query = command.replace('search', '').strip()
            if query:
                self.search_web(query)
            else:
                self.speak("What would you like me to search for?")
        
        elif 'open' in command:
            app = command.replace('open', '').strip()
            if app:
                self.open_application(app)
            else:
                self.speak("What would you like me to open?")
        
        elif 'joke' in command:
            self.tell_joke()
        
        elif 'weather' in command:
            self.get_weather()
        
        elif 'news' in command:
            self.get_news()
        
        elif any(word in command for word in ['exit', 'quit', 'goodbye', 'stop']):
            self.speak("Goodbye! Have a great day!")
            return False
        
        else:
            self.speak("I'm not sure how to help with that. Try asking for time, date, or search something.")
        
        return True
    
    def run(self):
        """Main loop for the voice assistant"""
        self.speak("Voice Assistant activated. How can I help you?")
        
        running = True
        while running:
            command = self.listen()
            if command:
                running = self.process_command(command)

def main():
    """Main function"""
    assistant = VoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
