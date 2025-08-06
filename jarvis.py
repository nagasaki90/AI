import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import openai

# ✅ Set your OpenRouter API key and endpoint
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key_prefix = "Bearer"

# 🔊 Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio)
            print("You:", query)
            return query.lower()
        except sr.WaitTimeoutError:
            speak("No voice detected.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
        except sr.RequestError:
            speak("Speech service error.")
    return ""

def ask_openrouter(question):
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error from OpenRouter: {str(e)}"

def handle_command(query):
    if "open youtube" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in query:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "play music" in query:
        music_dir = "C:/Users/Public/Music"  # ✅ CHANGE to your real path
        try:
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing music.")
            else:
                speak("No songs found in the folder.")
        except:
            speak("Could not access music folder.")
    elif "time" in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {time}")
    elif "exit" in query or "stop" in query:
        speak("Goodbye.")
        exit()
    else:
        speak("Let me think...")
        answer = ask_openrouter(query)
        speak(answer)

# ✅ MAIN PROGRAM LOOP
if __name__ == "__main__":
    speak("Hello! I am Jarvis. How can I assist you?")
    while True:
        command = listen()
        if command:
            handle_command(command)
