import os
import requests
from dotenv import load_dotenv
load_dotenv()

class Save:
    @staticmethod #allows to use the method without instantiating the class
    def save_on_back4app(obj):
        headers = {
            'X-Parse-Application-Id': os.getenv('PARSE-APPLICATION'),
            'X-Parse-REST-API-Key': os.getenv('PARSE-KEY'),
            'Content-Type': 'application/json'
        }

        body = f'{{"quizset": "{obj}"}}'

        response = requests.post('https://parseapi.back4app.com/classes/Quiz', headers=headers, data=body)

        print(response.json())