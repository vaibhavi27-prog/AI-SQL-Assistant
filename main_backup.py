import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ai_sql_assistant"
)

cursor = conn.cursor()

question = input("Ask a question: ")

if "salary" in question.lower():

    cursor.execute(
        "SELECT * FROM employees WHERE salary > 60000"
    )

elif "it" in question.lower():

    cursor.execute(
        "SELECT * FROM employees WHERE department='IT'"
    )

elif "employee" in question.lower():

    cursor.execute(
        "SELECT * FROM employees"
    )

else:
    print("I don't understand the question.")
    exit()

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()