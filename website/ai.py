from openai import OpenAI
import json

API_KEY = 'sk-proj-Dccj5qj6YpBPdebmGS4vT3BlbkFJy0MV75L9WGIcybWdYbKD'

client = OpenAI(api_key=API_KEY)

model = 'gpt-3.5-turbo-0125'

def chat(prompt):
    response = client.chat.completions.create(
        model = model,
        messages = [
            {'role': 'system', 'content': 'You are an author with immense knowledge on a variety of topics.'},
            {'role': 'user', 'content': prompt}
        ]
    )

    return response.choices[0].message.content

def chatWithContext(ogPrompt, aiOutline, newPrompt):
    response = client.chat.completions.create(
        model = model,
        messages = [
            {'role': 'system', 'content': 'You are an author with immense knowledge on a variety of topics.'},
            {'role': 'user', 'content': str(ogPrompt)},
            {'role': 'assistant', 'content': str(aiOutline)},
            {'role': 'user', 'content': str(newPrompt)}
        ]
    )

    return response.choices[0].message.content

jsonTemplate = {
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

def WriteBook(topic, chapters, points):
    # topic = input('What is your book topic?: ')
    # chapters = int(input('How many chapters will your book have?: '))
    # points = int(input('How many topics will be discussed each chapter?: '))
    prompt = f"Write me an outline for a book. This book will be about {topic}. It will have {str(chapters)} chapters, with each chapter having {str(points)} sub-sections. You will format your response in JSON as follows: {str(jsonTemplate)}"

    outline = json.loads(chat(prompt))

    for chapter in outline['chapters']:
        for topic in chapter['sub-topics']:
            topic['content'] = chatWithContext(prompt, outline, f'Please write me the content for the sub-topic of: {topic}. DO NOT TITLE THE SUB-TOPIC, ONLY WRITE THE CONTENT!')

    book = ''

    book += f'<h1 id="h">{outline["title"]}</h1><br><h3>{outline["description"]}</h3>'
    for chapter in outline['chapters']:
        book += f'<br><h2 id="h">{chapter["topic"]}</h2>'
        for topic in chapter['sub-topics']:
            topic['content'] = topic['content'].replace("\n\n", "<br><br>")
            book += f'<br><h3 id="h">{topic["topic"]}</h3><br><p>{topic["content"]}</p>'

    return book