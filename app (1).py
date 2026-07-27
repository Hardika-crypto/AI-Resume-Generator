import streamlit as st
#streamlit:web based app making
#lite python framework

st.title("AI Resume Maker")

st.markdowm("""## User can create or download AI 
created resume based on high ATS score""")

#---------Agent code----------
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
from langchain.messages import SystemMessage, HumanMessage
import numpy as np
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader

#===========API key load=================
GOOGLE_API_KEY = st.sidebar.text_input("GEMINI_API_KEY",type="password")
GROQ_API_KEY = st.sidebar.text_input("GROQ_API_KEY",type="password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type="password")

#========Model building============
model=ChatGoogleGenerativeAI(
    model='gemini-3.5-flash-lite',
    google_api_key=GOOGLE_API_KEY
)
def search_recent_news_jobs(query):
  """This function helps to search
  recent news or recent jobs
  related to given search query
  suppose user write python developer jobs
  IT should return trending news or job link"""
  client = TavilyClient(
      api_key = TAVILY_API_KEY
  )
  return client.search(query)


#agent creation
from langchain.agents import create_agent
agent = create_agent(
  model = model,
  tools =[search_recent_news_jobs]
)

#=========PROMPT GENERATOR============
def prompt_generator(agent):
  """This function help to give detailed prompt
  followed by chain of thoughts and persona based prompting,
  main task is to give detailed prompt to build resume for
  students or experienced person based on their given personal information"""
  prompt=""" you are a senior HR resume analyzer ,
  main task is to give detailed prompt to build resume for
  students or experienced person based on their given personal information
  system instruction I want  Model to generate resume in html format, include that in prompt"""
  response = agent.invoke(prompt)
  file_name='prompt.py'
  with open(file_name,'w') as f:
    f.write(response.content[-1]['text'])
  return "prompt file generated successfully,agent can read it"
prompt_generator(model)

#TOOL 2
def resume_maker_prompt():
  """this function just gives updated prompt for model"""
  with open('prompt.py','r') as f:
    prompt = f.read()
  return prompt
resume_maker_prompt()

#============ generate resume==========
prompt="""you are helpful AI assistant
with job resume maker, your task is to give
HTML format resume , with proper designing
using recent css and java sript code,
with profesional design format.
user will upload data and return htyml format resume"""
final_prompt = prompt + resume_maker_prompt()

user_details="""user details: given below:
Name :Hardika,
an aspiring student pursuing BCA HONS. from IINTM IPU
languages learned c,gen ai and agentic ai, web devlopment
LOCATION :delhi
color must be of dark  pink theme
add effects  """
query = final_prompt +user_details

if st.button("Generate Resume"):
  with st.spinner("Running Agent....."):
    

    response = agent.invoke({'messages':[{'role':'user','content':query}]})
    code =response['messages'][-1].content[-1]['text']
      #st.markdown(code)
    st.html(code,width="stretch", unsafe_allow_javascript=True)
    

