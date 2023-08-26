import os
import requests
from dotenv import load_dotenv
load_dotenv()
import random
from datetime import datetime
import json

class Save:
    @staticmethod #allows to use the method without instantiating the class
    def save_on_back4app(obj):
        headers = {
            'X-Parse-Application-Id': os.getenv('PARSE_APPLICATION'),
            'X-Parse-REST-API-Key': os.getenv('PARSE_KEY'),
            'Content-Type': 'application/json'
        }

        body = f'{{"quizset": "{obj}"}}'

        response = requests.post('https://parseapi.back4app.com/classes/Quiz', headers=headers, data=body)

        print(response.json())

    @staticmethod
    def save_on_redis(obj):
        headers = {
            'accept': 'application/json'
        }

        def generate_key():
            # Generate a random key of length 8
            return ''.join([random.choice('23456789abcdefghjklmnopqrstuvwxyz') for _ in range(8)])

        key = "quiz:" + generate_key()
        value = obj

        body = "{}"

        response = requests.post(f'https://fastapi-redis-crud.vercel.app/create?key={key}&value={value}', headers=headers, data=body)

        print(response.json())
    
    @staticmethod
    def save_on_redis_json(obj, topic):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        def generate_key():
            # Generate a random key of length 8
            return ''.join([random.choice('23456789abcdefghjklmnopqrstuvwxyz') for _ in range(8)])

        key = "json_quiz:" + generate_key()
        body = {"created":f"{datetime.now()}","topic":topic,"quizset":f"{obj}"}
        print(body)
        print(type(body))

        response = requests.post(f'https://fastapi-redis-crud.vercel.app/create_dict?key=t{key}', headers=headers, data=json.dumps(body))

        print(response.json())
        