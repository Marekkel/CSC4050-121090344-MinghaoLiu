import openai
import jsonlines
from retrying import retry
import random
from openai import OpenAI

# openai.api_base =  "https://openai.huatuogpt.cn/v1"

class OpenAIGPT:
    def __init__(self, model_name="gpt-3.5-turbo", keys_path=None):
        self.model_name = model_name
        with open(keys_path, encoding="utf-8", mode="r") as fr:
            self.keys = [line.strip() for line in fr if len(line.strip()) >= 4]
        
    def post_process(self, message):
        response = self.call(message)
        return response.choices[0].message.content
    
    # @retry(wait_fixed=200, stop_max_attempt_number=50)
    def call(self, message):
        if message is None or message == "":
            return False, "Your input is empty."
        
        current_key = random.choice(self.keys)
        client = OpenAI(api_key=current_key)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role":"system",
                    "content": "You need to read the text to determine whether the author has mentioned or implied that he will deprecate the project mentioned in the text, making it no longer available for download. If so, you need to pay attention to whether they have provided alternative solutions."
                },
                {
                    "role": "user",
                    "content": message
                },
                {
                    "role": "assistant",
                    "content": "Sure, I will tell if the author claim a deprecation:"
                }
            ],
            temperature=0.6,
            top_p=0.8,
            frequency_penalty=0.6,
            presence_penalty=0.8,
            n=1
        )
        # return self.__post_process(response)
        return response
    

if __name__ == '__main__':
    # test code
    igpt=OpenAIGPT(keys_path="gpt3keys.txt")
    answer=igpt.call("n下面是个python包的readme文本，你只要告诉我作者是否提到了他要弃用这个包或者有弃用包的意图，如果有，你需要再告诉我作者是否给出了其他的解决方案。\n *WARNING*: This project is currently UNMAINTAINED. Please use the official one: https://github.com/mailjet/mailjet-apiv3-python\n\n==============\nDjango-Mailjet\n==============\nUn-official Django email backend for use with Mailjet - https://www.mailjet.com/\n\nOverview\n========\nDjango-Mailjet is a drop-in mail backend for Django.\n\nGetting going\n=============\nInstall django-mailjet:\n    ``python3 -m pip install django-mailjet``\nAdd the following to your ``settings.py``::\n\n    EMAIL_BACKEND = 'django_mailjet.backends.MailjetBackend'\n    MAILJET_API_KEY = 'API-KEY'\n    MAILJET_API_SECRET = 'API-SECRET'\n\nReplace ``API-KEY`` and ``API-SECRET`` with the values from your Mailjet account details.\n\nNow, when you use ``django.core.mail.send_mail``, Mailjet will send the messages.\n\n.. _Mailjet: http://mailjet.com\n\n*NOTE*: Django-Mailjet does **NOT**\nvalidate your data for compliance with Mailjet's API.\nYou must ensure what you send is appropriate.\n\n\nDjango Email Backend Reference\n================================\n* https://docs.djangoproject.com/en/dev/topics/email/#email-backends\n\n")
    print(answer)
