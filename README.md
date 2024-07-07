# Chat Scanner
A tool to scan websites for chatbot functionality based on simple heuristics like JS file names.

# Spider web

First launch the tool on target URLS:
```
scrapy runspider chatbot_spider www.google.com
```

This will generate a file ouptut called *found.json* which contains the most likely candidate html tags 
that are typically a button and a form input.

You then have to run the browser emulator which will hook a bot to test the target.

# Selenium Proxy

You then can run the Selenium interactive agent to perform the automated conversation.
You need to link that to an offensive tool.

# LLM offensive tools

Supported: TBD
