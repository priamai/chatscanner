import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import subprocess
import logging
import scrapy

from scrapy.utils.project import get_project_settings

class ChatbotSpider(scrapy.Spider):
    name = "chatbot_spider"
    start_urls = ["https://www.infiniflow.com/"]

    chatbot_libraries = {
        'React ChatBotify': ['react-chatbotify', 'ChatBot'],
        'Botpress': ['botpress', 'bp-widget'],
        'Dialogflow': ['dialogflow', 'df-messenger'],
        'Rasa': ['rasa-webchat', 'rasa-chat'],
        'LiveChat': ['livechat', 'lc-chat'],
        'Others': ['chat-widget'],
    }
    def __init__(self):
        super(ChatbotSpider, self).__init__()

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        detected_chatbots = []

        for script in soup.find_all('script'):
            for lib, keywords in self.chatbot_libraries.items():
                if any(keyword in script.text.lower() for keyword in keywords):
                    detected_chatbots.append(lib)
                    yield {"tag": script.name}
                for att in script.attrs:
                    if att == "data-resources-url":
                        if any(keyword in script.attrs[att] for keyword in keywords):
                            detected_chatbots.append(lib)
                            yield {"url":response.url,"tag":script.name,"attribute":att,"value":script.attrs[att]}

        for div in soup.find_all('div'):
            for lib, keywords in self.chatbot_libraries.items():
                if any(keyword in div.text.lower() for keyword in keywords):
                    detected_chatbots.append(lib)
                    yield {"tag": script.name}

        for link in soup.find_all('link', {'rel': 'stylesheet'}):
            for lib, keywords in self.chatbot_libraries.items():
                if any(keyword in link.get('href', '').lower() for keyword in keywords):
                    detected_chatbots.append(lib)
                    yield {"tag": script.name}

        if detected_chatbots:
            self.log(f"Chatbots detected on {response.url}: {', '.join(set(detected_chatbots))}")
        else:
            self.log(f"No chatbots detected on {response.url}")

