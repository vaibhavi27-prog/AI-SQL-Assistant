from google import genai
import mysql.connector

# Gemini Client
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ai_sql_assistant"
)

cursor = conn.cursor()

# User Question
question = input("Ask a question: ")

# Prompt for Gemini
prompt = f"""
You are an SQL expert.

Database Schema:

employees(
    id,
    name,
    department,
    salary
)

Convert the user's question into a valid MySQL query.

Rules:
1. Return ONLY SQL.
2. No explanation.
3. No markdown.
4. No backticks.

Question:
{question}
"""

# Generate SQL using Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

sql_query = response.text.strip()

print("\nGenerated SQL:")
print(sql_query)

# Execute SQL
try:
    cursor.execute(sql_query)

    rows = cursor.fetchall()

    print("\nResults:")
    for row in rows:
        print(row)

except Exception as e:
    print("Error:", e)

# Close connection
cursor.close()
conn.close()