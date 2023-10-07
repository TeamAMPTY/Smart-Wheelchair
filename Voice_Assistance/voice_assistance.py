import openai
import pyttsx3
import speech_recognition as sr
import time

openai.api_key = "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"

engine = pyttsx3.init()


session_active = False
conversation_history = []

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None  

def generate_response(prompt, retry_count=3):
    try:
        time.sleep(5)  
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response["choices"][0]["text"]
    except openai.error.APIConnectionError as e:
        print(f"Error communicating with OpenAI: {e}")
        if retry_count > 0:
            print(f"Retrying after a delay... Attempts left: {retry_count}")
            time.sleep(5)
            return generate_response(prompt, retry_count - 1)
        else:
            print("Max retries reached. Unable to get response.")
            return None

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def start_session():
    global session_active
    global conversation_history
    session_active = True
    conversation_history = []
    print("Session started. You can now ask questions.")

def stop_session():
    global session_active
    session_active = False
    print("Session stopped. Say 'Genius' to start a new session.")

def record_audio_to_file(filename, source, timeout=None):
    recognizer = sr.Recognizer()
    source.pause_threshold = 1
    audio = recognizer.listen(source, phrase_time_limit=None, timeout=timeout)
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())

def main():
    global session_active
    global conversation_history

    while True:
        if not session_active:
            print("Say 'Genius' to start a new session...")
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                audio = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio)
                    if transcription.lower() == "genius":
                        start_session()
                except Exception as e:
                    print("An error occurred: {}".format(e))

        else:
            print("Say your question or 'Stop' to end the session...")
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                source.pause_threshold = 1
                try:
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open("input.wav", "wb") as f:
                        f.write(audio.get_wav_data())

                    text = transcribe_audio_to_text("input.wav")
                    if text:
                        print(f"You said: {text}")

                        if "stop" in text.lower():
                            stop_session()
                            continue

                        conversation_history.append(text)

                        prompt = " ".join(conversation_history)

                        response = generate_response(prompt)
                        print(f"GPT-3 says: {response}")

                        speak_text(response)

                        conversation_history = []

                except Exception as e:
                    print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
