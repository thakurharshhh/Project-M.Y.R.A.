from gtts import gTTS
import playsound
import os

text = "Hello Boss!, Friday Here!"

# Remove previous audio if exists
if os.path.exists("friday.mp3"): # It will helps to prevent colision of two running command boices
    os.remove("friday.mp3")

# Use UK English voice (British female style)
tts = gTTS(text=text, lang='en', tld='co.uk')
tts.save("friday.mp3")
playsound.playsound("friday.mp3")
