import asyncio
import requests
from os import environ
from bardapi import Bard
from Bard import Chatbot
from Bard import AsyncChatbot

class bard_bot():
    def __init__(self,  __BARD_API_KEY):
        self.session_var = requests.Session()
        self.session_var.headers = {
            "Host" : "bard.google.com",
            "X-Same-Domain" : "1",
            "User-Agent" : "Chrome",
            "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin" : "https://bard.google.com",
            "Referer" : "https://bard.google.com/",
        }
        self.session_var.cookies.set("__Secure-1PSID", __BARD_API_KEY)
        self.bard_chat = Bard(token=__BARD_API_KEY, session=self.session_var, timeout=30)
        self.bot_plus_flag = True

    def __init__(self, Secure_1PSID, Secure_1PSIDTS):
        self.bard_chat = Chatbot(Secure_1PSID, Secure_1PSIDTS)

    def Chat(self, input_info):
        #reply = bard_chat.ask("What is the meaning of life?")
        #reply = bard_chat.ask("What is LLaMA Model?")
        #reply = bard_chat.ask("do you upgrade to Gemini?")
        reply = self.bard_chat.ask(input_info)
        print(reply['content'])
        return reply['content']

    def Img(self, Path):
        if self.bot_plus_flag:
            image = open(Path, 'rb').read()
            reply = self.bard_bot.ask_about_image('What is in the image', image)
            print(reply['content'])
            return reply['content']
        else: print('Bard is not plus version.\r\n')

async def async_chat(text):
    if __name__ == '__main__':
        async_bot = await AsyncChatbot.create(Secure_1PSID, Secure_1PSIDTS)
        reply = await async_bot.ask(text)
        print(reply['content'])
        return reply['content']
    
Secure_1PSID = environ.get("Bard_Secure_1PSID")
Secure_1PSIDTS = environ.get("Bard_Secure_1PSIDTS")
API_KEY = environ.get("BARD_API_KEY")
# print(Secure_1PSID)
# print(Secure_1PSIDTS)
# print(API_KEY)

# ai_machine_plus = bard_bot(API_KEY)
# ai_machine = bard_bot(Secure_1PSID, Secure_1PSIDTS)