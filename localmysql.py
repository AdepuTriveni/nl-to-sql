from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import mysql.connector
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini function
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    response = model.generate_content([prompt[0], question])
    cleaned_sql = response.text.replace("```sql", "").replace("```", "").strip()
    return cleaned_sql

# MySQL read function
def read_sql_query(sql):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="student"  # Change this if your DB name is different
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = cursor.column_names
        conn.close()
        return columns, rows
    except mysql.connector.Error as err:
        return None, f"MySQL error: {err}"

# Prompt to Gemini
prompt = [
    """You are an expert in converting English questions to SQL query!
The SQL database contains the following tables: student, employee, marks, courses, department, etc.

- The `student` table has columns: id, name, class, section
- The `employee` table has columns: id, name, department, salary, job
- The `marks` table has columns: student_id, subject, marks

For example:
- "How many students are in class 10?" -> SELECT COUNT(*) FROM student WHERE class = '10';
- "List employees in HR department" -> SELECT * FROM employee WHERE department = 'HR';
- "Get average marks in Math" -> SELECT AVG(marks) FROM marks WHERE subject = 'Math';
"""
]

# Streamlit UI
st.set_page_config(page_title="Local MySQL + Gemini", layout="wide")
st.title("💬 Natural Language to SQL - MySQL Edition")

question = st.text_input("Ask your question:")

if question:
    response = get_gemini_response(question, prompt)
    st.subheader("🧠 Generated SQL Query:")
    st.code(response, language='sql')

    columns, result = read_sql_query(response)

    if columns:
        st.subheader("📊 Query Results:")
        st.dataframe([dict(zip(columns, row)) for row in result])
    else:
        st.error(result)
