from openai import OpenAI
import json

class AI:
    def __init__(self, apikey, model):
        self.apikey = apikey
        self.model = model
        self.client = OpenAI(api_key=self.apikey)
        self.jsonTemplate = {
            "title": "the book title",
            "description": "a short description of the book",
            "chapters": [
                {
                    "chapter": "chapter number as integer",
                    "topic": "main topic of the chapter",
                    "sub-topics": [
                        {
                            "topic": "title of sub-topic"
                        }
                    ]
                }
            ]
        }

    def chat(self, systemMsg, prompt):
        if systemMsg == '':
            systemMsg = 'You are an author with immense knowledge on a variety of topics.'

        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {'role': 'system', 'content': systemMsg},
                {'role': 'user', 'content': prompt}
            ]
        )

        return [response.choices[0].message.content, response]

    def chatWithContext(self, systemMsg, ogPrompt, aiOutline, newPrompt):
        if systemMsg == '':
            systemMsg = 'You are an author with immense knowledge on a variety of topics.'

        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {'role': 'system', 'content': systemMsg},
                {'role': 'user', 'content': str(ogPrompt)},
                {'role': 'assistant', 'content': str(aiOutline)},
                {'role': 'user', 'content': str(newPrompt)}
            ]
        )

        return response.choices[0].message.content

    def WriteBook(self, systemMsg, topic, chapters, points):
        # topic = input('What is your book topic?: ')
        # chapters = int(input('How many chapters will your book have?: '))
        # points = int(input('How many topics will be discussed each chapter?: '))
        prompt = f"Write me an outline for a book. This book will be about {topic}. It will have {str(chapters)} chapters, with each chapter having {str(points)} sub-sections. You will format your response in JSON as follows: {str(self.jsonTemplate)}"

        try:
            response = self.chat(prompt, systemMsg)
            outline = json.loads(response[0])

            for chapter in outline['chapters']:
                for topic in chapter['sub-topics']:
                    topic['content'] = self.chatWithContext(systemMsg, prompt, outline, f'Please write me the content for the sub-topic of: {topic}. DO NOT TITLE THE SUB-TOPIC, ONLY WRITE THE CONTENT!')

            book = ''

            book += f'<h1 id="h">{outline["title"]}</h1><br><h3>{outline["description"]}</h3>'
            for chapter in outline['chapters']:
                book += f'<br><h2 id="h">{chapter["topic"]}</h2>'
                for topic in chapter['sub-topics']:
                    topic['content'] = topic['content'].replace("\n\n", "<br><br>")
                    book += f'<br><h3 id="h">{topic["topic"]}</h3><br><p>{topic["content"]}</p>'
            return [book, True, outline['title']]
        except:
            return ['This website uses the ChatGPT API to build your books from the ground up. If your request is inappropriate or any other errors come up within the generation process, you will see this page.', False]