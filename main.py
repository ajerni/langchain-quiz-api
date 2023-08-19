import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from fastapi import FastAPI
from langchain.chains import LLMChain

from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

from helpers import Save

from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

chat = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)

system_template="You are a Quizmaster asking {level} questions in the area of {thema}. Always create a new question"
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template="Create {set_nr} sets of quiz questions to the given topic and return it each together with {number_of_answers} answers of which one is the correct answer. Indicate which answer is the correct one.\n{format_instructions}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(llm=chat, prompt=chat_prompt)

app = FastAPI(title="FastAPI Langchain Quiz")

#for input
class Quiz(BaseModel):
    level: str
    thema: str
    number_of_answers: str
    set_nr: int

#for output
class Quizset(BaseModel):
    set_nr: int = Field(description="Number of the Quiz-Set") 
    question: str = Field(description="A quiz question")
    answers: dict = Field(description="The corresponding answers to the questions")
    correct_answer: str = Field(description="The correct answer")

parser = PydanticOutputParser(pydantic_object=Quizset)

@app.post("/quiz")
async def generate_quizset(quiz: Quiz):
    result = chain.run(
        level=quiz.level,
        thema=quiz.thema,
        number_of_answers=quiz.number_of_answers,
        set_nr=quiz.set_nr,
        format_instructions=parser.get_format_instructions()
    )
   
    def parse_list(data):
        list_objs = data.split('\n')
        parsed_objs = []
        for list_obj in list_objs:
            parsed_objs.append(list_obj)    
        return parsed_objs
    data = parse_list(result)
    data = [item for item in data if item]
    parsed_data = [json.loads(item) for item in data]

    #parsed_data is a list of dicts
    for item in parsed_data:
        print(item["question"] + " " + item["answers"][item["correct_answer"]])
    
    Save.save_on_back4app(parsed_data)
    Save.save_on_redis(parsed_data)

    return parsed_data

if __name__ == "__main__":\
    print(chain.run(level="easy", thema="Programming", number_of_answers="2", set_nr=2, format_instructions="Give output as JSON object but to not include these backslash n in the output."))

# addition to test Postgres DB and container app on back4app:

system_template2="You are a helpful assistent with a good sense of humor."
system_message_prompt2 = SystemMessagePromptTemplate.from_template(system_template2)

human_template2="Reply to the following in a funny way: {question}. Maximum of 2 scentences in your reply."
human_message_prompt2 = HumanMessagePromptTemplate.from_template(human_template2)

chat_prompt2 = ChatPromptTemplate.from_messages([system_message_prompt2, human_message_prompt2])

chain2 = LLMChain(llm=chat, prompt=chat_prompt2)

@app.get("/fun")
async def funny_reply(question:str):

    result2 = chain2.run(question=question)
    Save.save_on_back4app(result2)
    return result2