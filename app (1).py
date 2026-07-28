import streamlit as st
#streamlit:web based app making
#lite python framework
st.title("AI Resume Maker")
st.markdown("""## User can create or download AI 
created resume based on high ATS score""")

#=========Agent code==========
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
from PIL import image

#===========API key load=================
GOOGLE_API_KEY = st.sidebar.text_input("GEMINI_API_KEY",type="password")
GROQ_API_KEY= st.sidebar.text_input("GROQ_API_KEY",type="password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type="password")
if not(GOOGLE_API_KEY) and not (GROQ_API_KEY) and not (TAVILY_API_KEY):
    st.sidebar.warning("PASS API KEY")
    st.stop()
else:
    st.success("API KEY LOADED")

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
#============UPLOAD IMAGE=============
uploaded_file = st.sidebar.fileuploader(
    "choose an image file",
     type=["jpg","jpeg","png","webp"])
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.sidebar.image(image, caption="uploaded image",use_container_width=True)
    
     
if image.mode in ("RGBA","p"):
    image = image.convert("RGB")
    base_name=os.path.splitext(uploaded_file.name)[0]
    save_path =f"{base_name}.jpg"

#3 save the image to the current working directory
image.save(save_path,"JPEG")
st.sidebar.success(f"image generated successfully saves as '{save_path}'!")
except Exception as e:
st.error(f"error processing image: {e}")

#============ generate resume==========
prompt="""you are helpful AI assistant
with job resume maker, your task is to give
HTML format resume , with proper designing
using recent css and java sript code,
with profesional design format.
user will upload data and return htyml format resume"""
final_prompt = prompt + resume_maker_prompt()

user_details = f"""user details: given below:
Resume info: {user_info}
Photo: {uploaded_file }
Photo present in current directory with name as 
uploaded_file, and once resume generated give
download button in same html code.
Default if not given: Give Python Developer Resume"""


query = final_prompt +user_details

if st.button("Generate Resume"):
  with st.spinner("Running Agent....."):
    

    response = agent.invoke({'messages':[{'role':'user','content':query}]})
    code =response['messages'][-1].content[-1]['text']
    #st.markdown(code)
    st.html(code,width="stretch", unsafe_allow_javascript=True)
    

