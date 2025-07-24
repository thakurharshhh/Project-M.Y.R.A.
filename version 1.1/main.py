import speech_recognition as sr
from gtts import gTTS
import os
import time
from difflib import get_close_matches

# Speak Function
def speak(text):
    try:
        filename = "response.mp3"
        
        # Safely remove existing file
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                print("[ERROR]: File is in use, waiting 1 second...")
                time.sleep(1)
                return
        
        # Convert text to speech
        tts = gTTS(text=text, lang='en', tld='co.uk')
        tts.save(filename)
        os.system(f'start /min {filename}')  # Plays in default system player (minimized)

        time.sleep(2)  # Allow playback to complete before next iteration
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

# Custom Command's Here
def my_command(command):
    known_commands = {
        "hello": "Hello Boss! myra is online.",
        "myra": "Yess Boss!",
        "how are you": "Fine boss waiting for your command.",
        "your work": "I works as your personal AI assistant.",
        "kaise ho": "Ekdam Badhiya.",
        "mera name batyo": "Harsh Pratap Singh.",
        "tum kiski paglu ho": "maaiin harshhpagluuu hu."
    }

    if command in known_commands:
        speak(known_commands[command])
        return True
    else:
        close_match = get_close_matches(command, known_commands.keys(), n=1, cutoff=0.6)
        if close_match:
            speak(known_commands[close_match[0]])
        else:
            speak("I'm not sure.")
        return False

# Main Loop
if __name__ == "__main__":
    while True:
        command = listen()
        if command in ["stop", "exit", "bye","turn it off myra"]: # exit commands 
            speak("Going offline.")
            break
        my_command(command)

