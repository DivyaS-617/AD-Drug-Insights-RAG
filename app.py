import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import os

# 1. Page configuration
st.set_page_config(page_title="Abu Dhabi Drug Insights (Mock)", layout="wide")

st.title("💊 Abu Dhabi Drug Insights - Drug Master Explorer")
st.write("This application uses the 'Drug_master.xlsx' mock data file to search for drug information.")

# 2. Setup API Key from Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Missing GOOGLE_API_KEY in Secrets. Please add it to your Streamlit Cloud settings.")
    st.stop()

# 3. Load the Mock Data File
# We have renamed this from shafafiya_master.xlsx to Drug_master.xlsx
try:
    df = pd.read_excel("Drug_master.xlsx", engine="openpyxl")
    st.success("Successfully loaded 'Drug_master.xlsx'")
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.info("Check if the file is named 'Drug_master.xlsx' on GitHub and is not corrupted.")
    st.stop()

# 4. Create the AI RAG Agent
# This 'agent' reads your Excel data and answers questions
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

# 5. User Interface for Chat
st.divider()
user_question = st.text_input("Ask a question about the drugs (e.g., 'What is the package price for Panadol?'):")

if user_question:
    with st.spinner("Searching the Drug Master..."):
        try:
            # Pushed 4 spaces to the right of 'try'
            response = agent.invoke({"input": user_question})["output"]
            st.write("### AI Response:")
            st.info(response)
        except Exception as e:
            # Aligned exactly under 'try'
            st.error(f"An error occurred: {e}")
# 6. Data Preview (Optional checkbox)
if st.checkbox("Show Data Preview (Top 10 rows)"):
    st.dataframe(df.head(10))
