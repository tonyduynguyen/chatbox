import re
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import smtplib, ssl  # to send email
import requests
import json
import easygui  # để hiển thị messagebox

class virtual_assistant:
    def __init__(self, ui):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)  # 0 = male, 1 = female
        self.activationWord = 'kem'  # Single word
        self.chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        webbrowser.register('chrome', None,
                            webbrowser.BackgroundBrowser(self.chrome_path))
        self.you = ""
        self.ui = ui

    def speak(self, text, voice=120):
        vivoice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
        self.engine.setProperty("voice", vivoice)
        self.engine.say(text)
        self.engine.runAndWait()

    def parseCommand(self):
        listener = sr.Recognizer()
        print('Listening for a command')

        with sr.Microphone() as source:
            listener.pause_threshold = 1
            # nghe trong vòng 5 giây
            input_speech = listener.listen(source, phrase_time_limit=5)

        try:
            print('Recognizing speech...')
            query = listener.recognize_google(input_speech, language='vi')
            #query = "siri send mail to tin hello my name is Tin"
            #query = "siri go to youtube.com film"
            #query = "siri weather london"
            print(f'The input speech was: {query}')
            self.ui.label_2.setText(query)

        except Exception as exception:
            print('Tôi không thể nghe bạn nói gì')
            self.speak('Tôi không thể nghe bạn nói gì')
            print(exception)

            return 'None'
        return query


    def search_wikipedia(self, keyword=''):
        searchResults = wikipedia.search(keyword)
        if not searchResults:
            return 'Không nhận được kết quả'
        try:
            wikiPage = wikipedia.page(searchResults[0])
        except wikipedia.DisambiguationError as error:
            wikiPage = wikipedia.page(error.options[0])
        print(wikiPage.title)
        wikiSummary = str(wikiPage.summary)
        return wikiSummary

    def getWeather(self, city):
        api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=06c921750b9a82d8f5d1294e1586276f"

        try:
            json_data = requests.get(api).json()
            condition = json_data['weather'][0]['main']
            temp = int(json_data['main']['temp'] - 273.15)

            final_info = condition + " " + str(temp) + "°C"
            return final_info
        except:
            return 'Không nhận diện được'

    def listOrDict(var):
        if isinstance(var, list):
            return var[0]['plaintext']
        else:
            return var['plaintext']

    def check_json(self, array):
        f = open('email_address.json')
        json_data = json.load(f)
        for x in json_data:
            # print(json_data[x]['name'])
            if json_data[x]['name'] in array:
                print(json_data[x]['name'])
                return json_data[x]
        return

    def set_youSpeech(self, you_speech):
        self.you = you_speech

    def exit(self):
        self.set_youSpeech("heo thoát")


    def main(self):
        self.speak('Chào bạn, tôi là heo.', 120)
        while True:
            computer_mounth = ""

            if self.you == "":
                may_nghe = self.parseCommand().lower().split()
            else:
                may_nghe = self.you.lower().split()

            if may_nghe[0] == self.activationWord:
                may_nghe.pop(0)
                # Set commands
                if may_nghe[0] == 'nói':
                    if 'chào' in may_nghe:
                        computer_mounth = "Chào bạn, hân hạnh được gặp bạn"
                        self.ui.label_3.setText(computer_mounth)
                        self.speak('Chào bạn, hân hạnh được gặp bạn')
                    else:
                        may_nghe.pop(0)  # Remove 'say'
                        speech = ' '.join(may_nghe)
                        computer_mounth = speech
                        self.ui.label_3.setText(computer_mounth)
                        self.speak(speech)
                #weather
                if may_nghe[0] == 'thời' and may_nghe[1] == 'tiết':
                    computer_mounth = "Thời tiết"
                    # may_nghe[0]: weather ; may_nghe[1]: london
                    # print(may_nghe[1])
                    result = self.getWeather(may_nghe[2])
                    # print(result)
                    self.ui.label_3.setText(result)
                    self.speak(result)



                # Navigation
                if may_nghe[0] == 'đi' and may_nghe[1] == 'đến':
                    computer_mounth = 'Đang mở... '
                    self.speak('Đang mở... ')
                    # Assume the structure is activation word + go to, so let's remove the next two words
                    may_nghe = ' '.join(may_nghe[2:])
                    print(may_nghe)  #google.com film funny
                    may_nghe = may_nghe.split(" ")  # ['google.com', 'film', 'funny']
                    # may_nghe[0] => google.com; may_nghe[1:] => ['film', 'funny']
                    if may_nghe[0] == 'google.com':
                        may_nghe = may_nghe[0] + "/search?q=" + "+".join(may_nghe[1:])
                        webbrowser.get('chrome').open_new(may_nghe)
                    if may_nghe[0] == "youtube.com":
                        may_nghe = may_nghe[0] + "/results?search_query=" + "+".join(may_nghe[1:])
                        webbrowser.get('chrome').open_new(may_nghe)
                    if may_nghe[0] == "open.spotify.com":
                        may_nghe = may_nghe[0] + "/search/" + "%20".join(may_nghe[1:])
                        webbrowser.get('chrome').open_new(may_nghe)
                    self.ui.label_3.setText(computer_mounth)


                if may_nghe[0] == 'gửi' and may_nghe[1] == 'mail':
                    name_email = self.check_json(may_nghe[2:10])
                    #print(name_email) {'name':'sdsdsd', 'email':'ajskasj@gmail.com'}
                    if name_email != None:
                        self.speak('Bắt đầu gửi email')
                        content = may_nghe[2:]
                        print(content)
                        port = 465  # For SSL
                        # https://www.youtube.com/watch?v=qk8nJmIRbxk
                        # link hướng dẫn lấy lấy mật khẩu
                        smtp_server = "smtp.gmail.com"
                        sender_email = "ngophitin2001@gmail.com"  # Enter your address
                        # receiver_email = "nptin2001@gmail.com"  # Enter receiver address
                        receiver_email = name_email['email']  # Enter receiver address
                        password = "saqllibnrderclkf"  # mật khẩu lấy từ hướng dẫn trên
                        print(' '.join(may_nghe[2:]))
                        # message = ' '.join(may_nghe[2:])
                        self.speak('nói nội dung email bạn muốn gửi')
                        message = self.parseCommand().lower()

                        context = ssl.create_default_context()
                        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                            server.login(sender_email, password)
                            server.sendmail(sender_email, receiver_email, message.encode('utf-8'))
                            computer_mounth = "Email đã được gửi"
                            self.speak('Email đã được gửi')
                    else:
                        computer_mounth = "Gửi email không thành công. Không tìm thấy email trong danh bạ"
                        self.speak(computer_mounth)
                    self.ui.label_3.setText(computer_mounth)


                # Wikipedia
                if may_nghe[0] == 'wiki':
                    may_nghe = ' '.join(may_nghe[1:])
                    computer_mounth = 'Truy vấn ngân hàng dữ liệu chung'
                    self.ui.label_3.setText(computer_mounth)
                    self.speak('Truy vấn ngân hàng dữ liệu chung')
                    self.ui.label_3.setText('Truy vấn ngân hàng dữ liệu chung')
                    # self.speak(self.search_wikipedia(may_nghe))
                    easygui.msgbox(self.search_wikipedia(may_nghe), title="simple gui")

                # Note taking
                if may_nghe[0] == 'ghi':
                    computer_mounth = 'Hãy nói cho tôi biết nội dung cần ghi'
                    self.ui.label_3.setText(computer_mounth)
                    self.speak(computer_mounth)
                    newNote = self.parseCommand().lower()
                    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                    with open('note_%s.txt' % now, 'w', encoding='utf-8') as newFile:
                        newFile.write(now)
                        newFile.write(' ')
                        newFile.write(newNote)
                    computer_mounth = 'Ghi chú đã viết'
                    self.speak('ghi chú đã viết')

                if may_nghe[0] == 'thoát':
                    self.set_youSpeech("") # để reset lại biến you -> tránh để lần lặp sau vẫn còn lưu chữ exit
                    computer_mounth = "Chào tạm biệt"
                    self.ui.label_3.setText(computer_mounth)
                    self.speak('Chào tạm biệt')
                    self.ui.groupBox.setHidden(True)
                    self.ui.pushButton.setHidden(False)
                    break
                self.set_youSpeech("")
                may_nghe = ''