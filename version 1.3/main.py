import speech_recognition as sr
from gtts import gTTS
import os
import time
from difflib import get_close_matches
import webbrowser
import datetime
import wikipedia
import psutil

# Speak Function
def speak(text):
    try:
        filename = "response.mp3"
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                print("[ERROR]: File in use, retrying...")
                time.sleep(1)
                return
        tts = gTTS(text=text, lang='en', tld='co.uk')
        tts.save(filename)
        os.system(f'start /min {filename}')
        time.sleep(2)
    except Exception as e:
        print(f"[ERROR in speak()]: {e}")

# Listen Function
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry boss, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your connection.")
        return ""

# Custom Commands
def my_command(command):
    known_commands = {
        "hello": "Hello Boss! how r u?.",
        "myra": "Haaann Jii!",
        "oyeee myra": "Haaann Jii Haaann!",
        "how are you": "Fine boss, waiting for your command.",
        "your work": "I work as your personal AI assistant.",
        "kaise ho": "Ekdam Badhiya.",
        "mera name batyo": "Harsh Pratap Singh.",
        "tum kiski paglu ho": "maaiin harshhpagluuu hu.",
        "are you real": "I am as real as your imagination.",
        "what is your name": "My name is MYRA. Multimodal Yielding Responsive Assistant.",
        "what is ai": "AI means Artificial Intelligence, the simulation of human intelligence in machines.",
        "who is prime minister of india": "Narendra Modi is the current Prime Minister of India.",
        "i am hungry": "Boss, you should eat something light and healthy.",
        "play music": "Sorry boss, I can't play music yet, but it's on my upgrade list!"
    }

    if command in known_commands:
        speak(known_commands[command])
        return True
    else:
        close_match = get_close_matches(command, known_commands.keys(), n=1, cutoff=0.6)
        if close_match:
            speak(known_commands[close_match[0]])
            return True
        return False

# Command Executor
def execute_command(command):
    # Website or App Commands
    if "open" in command:
        if "chrome" in command:
            speak("Opening Chrome")
            os.system("start chrome")
        elif "notepad" in command:
            speak("Opening Notepad")
            os.system("start notepad")
        elif "youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        else:
            app = command.replace("open", "").strip()
            speak(f"Opening {app}")
            os.system(f"start {app}")

    elif "search" in command:
        query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}"
        speak(f"Searching for {query}")
        webbrowser.open(url)

    elif "wikipedia" in command or "who is" in command or "what is" in command:
        try:
            topic = command.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
            result = wikipedia.summary(topic, sentences=2)
            speak(f"According to Wikipedia, {result}")
        except Exception:
            speak("Sorry, I couldn't find anything on Wikipedia.")

# For battery
    elif "battery" in command:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "charging" if battery.power_plugged else "not charging"
            speak(f"Battery is at {percent} percent and is {plugged}.")
        else:
            speak("Battery status not available.")

# For time
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Boss, the time is {now}")

# For date
    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")

    else:
        speak(f"I didn't understand fully, but let me search it.")
        webbrowser.open(f"https://www.google.com/search?q={command}")

# Trigger Listener
def wait_for_trigger():
    while True:
        command = listen()
        if "hey myra" in command:
            speak("Yes Boss, I'm listening.")
            return
        elif command:
            print("Trigger not matched. Listening again...")

# Main Loop
if __name__ == "__main__":
    speak("Hello Boss!, MYRA is online. Say 'Hey Myra' to begin.")
    wait_for_trigger()

    while True:
        command = listen()
        
        # Interrupt check
        if "wait myra listen" in command:
            speak("Yes boss, interrupt accepted. I'm ready.")
            continue
        
        # Exit trigger
        if command in ["stop", "exit", "bye", "turn it off myra"]:
            speak("Going offline.")
            break

        # Check for known commands or execute
        if not my_command(command):
            execute_command(command)

