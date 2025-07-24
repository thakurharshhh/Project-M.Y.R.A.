from gtts import gTTS
import playsound
import os

text = "Hello Boss!, Myra Here!"

# Remove previous audio if exists
if os.path.exists("myra.mp3"): 
    os.remove("myra.mp3")
# prevent from overlapping between voices.

# I have used Female English voice here.
tts = gTTS(text=text, lang='en', tld='co.uk')
tts.save("myra.mp3")
playsound.playsound("myra.mp3")
