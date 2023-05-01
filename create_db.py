import sqlite3
import pandas as pd
import os

def create_database(cursor):
    sql_command = """CREATE TABLE IF NOT EXISTS qa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject VARCHAR(500),
    question VARCHAR(500),
    correct_answer VARCHAR(500),
    choice_a VARCHAR(500),
    choice_b VARCHAR(500),
    choice_c VARCHAR(500),
    choice_d VARCHAR(500)
    );"""

    cursor.execute(sql_command)

def add_qa_pair(cursor, question, answer):
    sql_command = f"""INSERT INTO qa (question, answer) VALUES ("{question}", "{answer}");"""
    cursor.execute(sql_command)

def list_qa(cursor):
    cursor.execute("SELECT COUNT(*) FROM qa;")
    count = cursor.fetchone()[0]
    print(f"Number of rows in 'qa' table: {count}")
    cursor.execute("SELECT * FROM qa;")
    ans = cursor.fetchall()
    for i in ans:
        print(i)

def delete_all(cursor):
    sql_command = """DELETE FROM qa;"""
    cursor.execute(sql_command)

def print_db(cursor):
    cursor.execute("SELECT COUNT(*) FROM qa;")
    count = cursor.fetchone()[0]
    print(f"Number of rows in 'qa' table: {count}")
    cursor.execute("SELECT * FROM qa;")
    ans = cursor.fetchall()
    for i in ans:
        print(i)
        break

def extract_qa_pairs(cursor, path):
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            filepath = os.path.join(path, filename)
            df = pd.read_csv(filepath, delimiter=",", index_col=0)
            for _, row in df.iterrows():
                question = row["Questions"]
                correct_answer = row["Correct"]
                choice_a = row["A"]
                choice_b = row["B"]
                choice_c = row["C"]
                choice_d = row["D"]
                cursor.execute("""
                INSERT INTO qa (subject, question, correct_answer, choice_a, choice_b, choice_c, choice_d)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (filename[:-4],question, correct_answer, choice_a, choice_b, choice_c, choice_d))
    

if __name__ == '__main__':
    connection = sqlite3.connect('questions_and_answers.db')
    cursor = connection.cursor()
    create_database(cursor)
    extract_qa_pairs(cursor, "./csv_files/")
    connection.commit()
    print_db(cursor)
    connection.close()

