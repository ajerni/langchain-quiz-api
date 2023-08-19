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

class Quiz(BaseModel):
    level: str
    thema: str
    number_of_answers: str
    set_nr: int

@app.post("/quiz")
async def generate_quizset(quiz: Quiz):
    result = chain.run(
        level=quiz.level,
        thema=quiz.thema,
        number_of_answers=quiz.number_of_answers,
        set_nr=quiz.set_nr,
        format_instructions="The response must not contain any newline characters '\n'. The response should be a single string containing the entire output, without any line breaks or carriage returns. Any newline characters in the output should be replaced with spaces to ensure that the output is a single continuous string."
    )
    result_without_linebreacks = result.replace("\n", " ")
    result_without_linebreacks = result_without_linebreacks.replace("\nr", " ")
    result_without_linebreacks = result_without_linebreacks.replace("\r", " ")
    result_without_linebreacks.strip()

    Save.save_on_back4app(result_without_linebreacks)
    return result_without_linebreacks

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