import pyttsx3  
engine = pyttsx3.init()  
text = "Python is a great programming language"  
engine.say(text)  
engine.runAndWait()  