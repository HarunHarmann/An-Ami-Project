from functions import Assistant
Amiy = Assistant("Amiy") #Create an instance and name it "Assistant"

if __name__ == '__main__':
    Amiy.speak("Hi, I am Amiy. How can I help you?")
    while True:
        said = Amiy.getCommand()
        result = Amiy.reply(said)
        if(result == "; leaving"):
            break
        
        
