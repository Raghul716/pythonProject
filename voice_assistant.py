import speech_recognition as sr

def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say a command (e.g., 'Play Radiohead'):")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
