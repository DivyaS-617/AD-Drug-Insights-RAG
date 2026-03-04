import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import GoogleGenerativeAI

# 1. Setup the AI Brain (You need a free Gemini API Key)
import os
from dotenv import load_dotenv

load_dotenv() # This command opens the .env file
my_key = os.getenv("GOOGLE_API_KEY") # This "fetches" the key by its name

llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=my_key)

st.title("🛡️ Abu Dhabi Official Drug RAG")
st.write("Using data from DOH Shafafiya Dictionary")

# 2. Load the Official Master List
df = pd.read_excel("shafafiya_master.xlsx")

# 3. Create the RAG Agent (The AI that reads your Excel)
agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

# 4. Chat Interface
user_question = st.text_input("Ask about a drug (e.g., 'What is the unit price of Panadol?'):")

if user_question:
    with st.spinner("AI is searching the DOH Registry..."):
        # The AI "retrieves" the row from Excel and "generates" an answer
        response = agent.run(user_question)
        st.info(response)
