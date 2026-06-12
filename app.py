from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import mysql.connector
import os

# Load .env file
load_dotenv()

app = Flask(__name__)

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def home():

    result = []
    sql_query = ""
    columns = []

    if request.method == "POST":

        question = request.form["question"]

        try:
            # MySQL Connection
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="ai_sql_assistant"
            )

            cursor = conn.cursor()

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

            # Generate SQL
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            sql_query = response.text.strip()

            print("Generated SQL:", sql_query)

            # Execute SQL
            cursor.execute(sql_query)

            result = cursor.fetchall()

            # Get column names
            columns = [col[0] for col in cursor.description]

            cursor.close()
            conn.close()

        except Exception as e:

            columns = ["Error"]

            result = [[str(e)]]

    return render_template(
        "index.html",
        result=result,
        sql_query=sql_query,
        columns=columns
    )

if __name__ == "__main__":
    app.run(debug=True)