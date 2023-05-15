import operator
import math
import PyPDF2
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import pyaudio
import webbrowser
import requests
from requests import get
import smtplib
import sys
import instaloader
import time
import pyautogui
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUi import Ui_jarvisUi
from pywikihow import search_wikihow
from bs4 import BeautifulSoup





engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)


# text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print(audio)

# to wish
def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning Sir, I am Jarvis,please tell me what can I do for you")
    elif hour == 12:
        speak("Good Noon Sir, I am Jarvis,please tell me what can I do for you")
    elif hour > 12 and hour <= 18:
        speak("Good Afternoon Sir, I am Jarvis,please tell me what can I do for you")
    else:
        speak("Good Evening Sir, I am Jarvis,please tell me what can I do for you")

        # speak("I am Jarvis,please tell me what I have to do")

def pdf_reader():
    book = open('Quantum (1).pdf','rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages are {pages}")
    speak("Sir please tell me the page I have to read")
    pg = int(input("Please enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('samarth21xxx022@akgec.ac.in', 'Samarth941')
    server.sendmail('samarth21xxx022@akgec.ac.in', to, content)
    server.close()

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
            # self.taskExecution()
            speak("please say wake up to continue")
            while True:
                self.query = self.takeCommand()
                if "wake up" in self.query or "hello" in self.query:
                    self.taskExecution()

    def takeCommand(self):
        #It takes microphone input from the user and returns string output

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            self.query = r.recognize_google(audio, language='en-in')
            print(f"User said: {self.query}\n")

        except Exception as e:
            # print(e)
            print("Say that again please...")
            return "None"
        return self.query

    def taskExecution(self):
        wishMe()
        while True:
            self.query = self.takeCommand().lower()
            # logics
            if 'open notepad' in self.query:
                npath = "C:\\Windows\\SysWOW64\\notepad.exe"
                os.startfile(npath)

            elif 'open command prompt' in self.query:
                os.system("start cmd")

            elif "how much battery is left" in self.query or 'battery percentage' in self.query:
                import psutil
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"Sir our system have {percentage} percent battery")
                if percentage >= 75:
                    speak("Sir we have enough battery to continue the work")
                elif percentage >= 40 and percentage < 75:
                    speak("Sir althrough there is much battery but I think we should connect our charger")
                elif percentage >= 15 and percentage <= 30:
                    speak("Sir I think it is necessary to connect the charger now")
                elif percentage < 15:
                    speak("Sir I don't think that working with low power is good please connect charger")

            elif "internet speed" in self.query:

                st = speedtest.Speedtest()
                dl = st.download()
                up = st.upload()
                speak(f"Sir we have {dl} bit per second downloading speed and {up} bit per second uploading speed")

            elif 'open camera' in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow("Webcam", img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break;
                        cap.release()
                        cv2.destroyAllWindows()

            elif 'play music' in self.query:
                music_dir = 'D:\music'
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif 'open code' in self.query:
                codePath = "C:\Program Files\Microsoft VS Code\Code.exe"
                os.startfile(codePath)

            elif 'open youtube' in self.query:
                webbrowser.open("youtube.com")

            elif 'open google' in self.query:
                speak("Sir,What should I search on Google")
                sm = self.takeCommand().lower()
                webbrowser.open(f"{sm}")

            elif 'open stackoverflow' in self.query:
                webbrowser.open("stackoverflow.com")

            elif "open whatsapp" in self.query:
                webbrowser.open("https://web.whatsapp.com/")

            elif 'ip address' in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")

            elif 'wikipedia' in self.query:
                speak('Searching Wikipedia...')
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open instagram' in self.query:
                webbrowser.open("instagram.com")

            elif 'send message' in self.query:
                kit.sendwhatmsg("+917505440541", "this is testing", 22, 30)

            # elif 'play song on youtube' in query:
            #     speak("Which song you wanna play")
            #     s = takeCommand().lower()
            #     kit.playonyt(f"{s}")

    #send email
            elif 'send email to sam' in self.query:
                try:
                 speak('what should i say')
                 content = self.takeCommand().lower()
                 to = "srivastavasamarth94@gmail.com"
                 sendEmail(to, content)
                 speak("Email has been sent")

                except Exception as e:
                    print(e)
                speak("Email can not be sent")


            #to check our location
            elif "where I am" in self.query or "where we are" in self.query:
                speak("wait sir, let me check")
                try:
                    ipAddress = get('https://api.ipify.org').text
                    print(ipAddress)
                    url = 'https://get.geojs.io/v1/ip/geo/'+ipAddress+'.json'
                    geo_requests = get(url)
                    geo_data = geo_requests.json()
                    city = geo_data['city']
                    country = geo_data['country']
                    speak(f"sir I am not sure but I think we are in {city} city of {country} country")
                except Exception as e:
                    speak("sorry sir, due to network issue i am not able to get our location")
                    pass


            # to check instagram profile
            elif 'Instagram profile' in self.query or 'profile on instagram' in self.query:
                speak("Sir please enter the username")
                name = input("Enter the username:")
                webbrowser.open(f'www.instagram.com/{name}')
                speak(f'sir here is the required profile')


             # to take screenshot
            elif 'take screenshot' in self.query:
               speak('Sir,please tell me the name of file')
               name = takeCommand().lower()
               speak("sir please hold on for few seconds, i am taking screenshot")
               time.sleep(3)
               img = pyautogui.screenshot()
               img.save(f"{name}.png")
               speak("The task has been completed sir")

            # to read pdf
            elif 'read pdf' in self.query:
                pdf_reader()

            #for calciulation
            elif 'do some calculation' in self.query or 'can you calculate' in self.query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Say what you want to calculate")
                    print("Listening...")
                    r.pause_threshold = 1
                    audio = r.listen(source)
                    my_string = r.recognize_google(audio)
                    print(my_string)
                    def get_operator(op):
                        return{
                            '+': operator.add,
                            '-': operator.sub,
                            'x': operator.mul,
                            'divided': operator.__truediv__
                        }[op]
                    def eval_binary_exp(op1,oper,op2):
                        op1,op2 = int(op1), int(op2)
                        return get_operator(oper)(op1,op2)
                    speak("Your result is")
                    print(eval_binary_exp(*(my_string.split())))




            #to hide the files
            elif "hide the files" in self.query or "hide this folder" in self.query or "visible for everyone" in self.query:
                speak("which file has to be hidden")
                condition = takeCommand().lower()
                if 'hide' in condition:
                    os.system("attrib +h /s /d")
                    speak("All the files have been hidden")
                elif 'visible' in condition:
                    os.system("attrib -h /s /d")
                    speak("files have been available for everyone")

                elif "leave it" in self.query or "leave for now" in self.query:
                    speak("ok sir")

            elif "temperature" in self.query:
                search = "temperature in ghaziabad"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"current {search} is {temp}")

            elif "activate how to do mod" in self.query:
                speak("How to do mod is activated tell me what you want to do")
                how = takeCommand().lower()
                max_results = 1
                how_to = search_wikihow(how, max_results)
                assert len(how_to) == 1
                how_to[0].print()
                speak(how_to[0].summary)

            elif 'hello' in self.query or 'hey' in self.query:
                speak("Hello sir, may I help you with something")

            elif 'how are you' in self.query:
                speak("I am fine sir, what about you?")

            elif 'good' in self.query or 'fine' in self.query:
                speak("good to hear that sir")

            elif 'sleep' in self.query:
                speak("Thanks for using me sir,have a good day")
                sys.exit()



startExecution = MainThread()

class Main(QMainWindow):
        def __init__(self):
            super().__init__()
            self.ui = Ui_jarvisUi()
            self.ui.setupUi(self)
            self.ui.pushButton_Start.clicked.connect(self.startTask)
            self.ui.pushButton_Exit.clicked.connect(self.close)
            self.ui.Chrome.clicked.connect(self.chrome_app)
            self.ui.Youtube.clicked.connect(self.yt_app)
            self.ui.Whatsapp.clicked.connect(self.whatsapp_app)

        def yt_app(self):
            webbrowser.open("youtube.com")

        def whatsapp_app(self):
            webbrowser.open("https://web.whatsapp.com/")

        def chrome_app(self):
            webbrowser.open("https://www.google.com/")

        def startTask(self):
          self.ui.label1 = QtGui.QMovie("../Gui/ExtraGui/fiugi.gif")
          self.ui.gif_1.setMovie(self.ui.label1)
          self.ui.label1.start()
          self.ui.label2 = QtGui.QMovie("../Gui/ExtraGui/live.gif")
          self.ui.gif_2.setMovie(self.ui.label2)
          self.ui.label2.start()
          self.ui.label3 = QtGui.QMovie("../Gui/VoiceReg/Aqua.gif")
          self.ui.gif_3.setMovie(self.ui.label3)
          self.ui.label3.start()
          self.ui.label4 = QtGui.QMovie("../Gui/ExtraGui/Earth.gif")
          self.ui.bg_4.setMovie(self.ui.label4)
          self.ui.label4.start()
          self.ui.label5 = QtGui.QMovie("E:\Gui\ExtraGui\Health_Template.gif")
          self.ui.label_2.setMovie(self.ui.label5)
          self.ui.label5.start()
          self.ui.label6 = QtGui.QMovie("../Gui/ExtraGui/gga.gif")
          self.ui.label_3.setMovie(self.ui.label6)
          self.ui.label6.start()
        # #   timer = QTimer(self)
        # #   timer.timeout.connect(self.showTime)
        # #   timer.start(999)
          startExecution.start()
        # #
        # #
        # # def showTime(self):
        # #       current_time = QTime.currentTime()
        # #       current_date = QDate.currentDate()
        # #       label_time = current_time.toString("hh:mm:ss")
        # #       label_date = current_date.toString(Qt.ISODate
        # #       self.ui.text_date.setText(label_date)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())



