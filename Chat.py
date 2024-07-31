
import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import platform
import wikipedia

listner = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listner.listen(source , timeout=2 , phrase_time_limit=3)
        command = listner.recognize_google(voice)
        command = command.lower()
        print(command)

    except Exception as e: 
        print("Enter command")

class Process:
    a = 0
    def open_website(command):
        replacement = command.replace("open ",".")
        webbrowser.open(f'https://WWW{replacement}.com')
    
    def calculate(command):
        try:
            numbers = [str(num) for num in range(10)]
            if any(num for num in numbers):
                ans = eval(command)
                print("the answer is " + str(ans))
                talk("the answer is " + str(ans))

        except Exception:
            return
        
    def open_application(command):
        replacement = command.replace("start ","")
        try:
            system_platform = platform.system()
            if system_platform == "Windows":
                subprocess.run(["start", replacement], shell=True)
            elif system_platform == "Darwin":
                subprocess.run(["open", "-a", replacement])

            elif system_platform == "Linux":
                subprocess.run([replacement])
            else:
                print("Unsupported operating system")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def information_search(command):
        replacement = command.replace("search " , "")
        try:
            global result
            result = wikipedia.summary(replacement, sentences = 2) 
            print(result)
            talk("Here is your search result")
        except:
            print("Unknown Error : search not found /: \n Check your connection")

    def reset_history():
        history_text = """search History <~>\n======================\n"""
        with open('History.txt', "w") as history:
            history.write(history_text)
            talk("History has been reset")

    def search_result(content):
        with open("searches.txt" , "w") as result_file :
                result_file.write(content)

    def write_history(command):
        with open("History.txt" , "a") as history:
            history.write(f"{command}\n")

print("Hey there, your keyboard is ready")
talk("Hey there, your keyboard is ready")        
mic = False
def perform():
    global command
    global mic
    if mic == True:
        command = take_command()
    else:
        command = input("YOU: ")

    if command == "mic in":
        mic = True
    # elif "open" in command:
    #     Process.open_website(command)
    elif "start" in command:
        Process.open_application(command)
    elif "search" in command:
        Process.information_search(command)
        Process.search_result(result)
    elif "reset history" in command:
        Process.reset_history()
    else:
        return 1

    Process.calculate(command)
    Process.write_history(command)

command = None
while command != "$":
    perform()
