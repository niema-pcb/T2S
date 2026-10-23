import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
for i, v in enumerate(voices):
    print(i, v.name)
    
voice = int(input("Select a voice by index: "))
engine.setProperty('voice', voices[voice].id)   

text = input("what should I say? ")
engine.setProperty('rate', 150)  # Set the speech rate (words per minute)
engine.setProperty('volume', 1.0)  # Set the volume (0.0 to 1.0)

engine.say(text)
engine.runAndWait()