import os
import json
import pandas as pd
import traceback
## Environmental value from .env file
from dotenv import load_dotenv

##LLM libraries
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks import get_openai_callback
import PyPDF2

## Load environmental variables from .env file
load_dotenv()

KEY= os.getenv("API_KEY")

##Create LLM object
llm= ChatOpenAI(openai_api_key=KEY, model_name='gpt-3.5-turbo', temperature=1.2)

##Create Prompt Template
TEMPLATE="""
Text: {text}
You are an expert information provider. Given above text, it is your job to provide appropritae answer in {tone} for the questions \
    asked. Make sure your \ response is in text utf-8 format.
    Question: {question}
"""

policy_read_prompt= PromptTemplate(
    input_variables= ['text', 'tone', 'question'],
    template= TEMPLATE
)

policy_read_chain= LLMChain(llm= llm, prompt=policy_read_prompt, output_key="policy_response", verbose=True)

generate_evaluate_chain= SequentialChain(
    chains= [policy_read_chain],
    input_variables= ['text', 'tone', 'question'],
    output_variables= ["policy_response"],
    verbose= True
)