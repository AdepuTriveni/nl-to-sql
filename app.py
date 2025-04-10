from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import re

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini function
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    response = model.generate_content([prompt[0], question])
    return response.text

# SQL read function
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    conn.commit()
    conn.close()
    return rows, column_names

# Function to clean Gemini's response
def clean_sql_response(text):
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL).strip().replace("```sql", "").replace("```", "").strip()

# Prompt for Gemini
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION, MARKS.
    For example:
    - "How many entries of records are present?" -> SELECT COUNT(*) FROM STUDENT;
    - "Tell me all the students studying in Data Science class?" -> SELECT * FROM STUDENT WHERE CLASS="Data Science";
    - "What is the average marks of students?" -> SELECT AVG(MARKS) FROM STUDENT;
    """
]

# 🟩 Streamlit UI
st.set_page_config(page_title="Text-to-SQL Gemini App", layout="wide")
st.title("🧠 Natural Language to SQL with Gemini")

question = st.text_input("Enter your question:")

if question:
    response = get_gemini_response(question, prompt)
    cleaned_sql = clean_sql_response(response)

    st.subheader("Generated SQL Query:")
    st.code(cleaned_sql, language='sql')

    try:
        results, columns = read_sql_query(cleaned_sql, "student.db")
        st.subheader("Query Results:")
        if results:
            st.dataframe([dict(zip(columns, row)) for row in results])
        else:
            st.write("No results found.")
    except Exception as e:
        st.error(f"Error running SQL query: {e}")
