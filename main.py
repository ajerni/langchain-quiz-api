import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from fastapi import FastAPI
from langchain.chains import LLMChain

from pydantic import BaseModel

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

@app.get("/quizset")
async def get_quiz_questions(level:str, thema:str, number_of_answers:str, set_nr:int, format_instructions:str):
    result = chain.run(level=level, thema=thema, number_of_answers=number_of_answers, set_nr=set_nr, format_instructions=format_instructions)
    return result

class Quiz(BaseModel):
    level: str
    thema: str
    number_of_answers: str
    set_nr: int

@app.post("/quiz_json")
def get_quizset_json(quiz: Quiz):
    result = chain.run(
        level=quiz.level,
        thema=quiz.thema,
        number_of_answers=quiz.number_of_answers,
        set_nr=quiz.set_nr,
        format_instructions="Format the output as JSON file with set_nr"
    )
    return result

if __name__ == "__main__":
    print(chain.run(level="easy", thema="Programming", number_of_answers="2", set_nr=2, format_instructions="Give output as JSON object"))
