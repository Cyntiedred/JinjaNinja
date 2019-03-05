import csv
import os
import datetime
import time
import connection


DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_HEADER_QUESTION = ["id","submission_time", "view_number","vote_number","title","message","image"]
DATA_HEADER_ANSWER = ["id","submission_time","vote_number","question_id","message","image"]
DATA_HEADER_LIST = ["id","title","answer","edit","delete"]
SUBMISSION_TIME = datetime.datetime.now().strftime("%s")


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute(""" 
                        SELECT *
                        FROM question;
                        """, )
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def get_new_question(cursor):
    cursor.execute("""
                    INSERT INTO question (title, message) 
                    VALUES ('');
                   """)
    new_question = cursor.fetchall()
    return new_question





def get_data_from_answers_csv():
    table = []
    with open('answer.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['submission_time'] = time.ctime(int(row['submission_time']))
            line = dict(row)
            table.append(line)
    return table


def write_answers_to_csv(add_to_file):
    with open('answer.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER_ANSWER)
        writer.writerow(add_to_file)


def write_into_csv(table):
    with open('question.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER_QUESTION)
        writer.writeheader()
        for dics in table:
            writer.writerow(dics)



def edit_question(table, id, edited_question):
    with open('temporary.csv', 'a') as csvfile:
        fieldnames = DATA_HEADER_QUESTION
        fieldnamewriter = csv.writer(csvfile)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        fieldnamewriter.writerow(fieldnames)
        for i in range(id):
            writer.writerow(table[i])
        writer.writerow(edited_question)
        for i in range(id, len(table)):
            writer.writerow(table[i])
        os.remove('question.csv')
        os.rename("temporary.csv",'question.csv')

'''
def edit_answer(table, id, edited_answer):
    with open('temporary.csv', 'a') as csvfile:
        fieldnames = DATA_HEADER_QUESTION
        fieldnamewriter = csv.writer(csvfile)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        fieldnamewriter.writerow(fieldnames)
        for i in range(id-1):
            writer.writerow(table[i])
        writer.writerow(edited_answer)
        for i in range(id, len(table)):
            writer.writerow(table[i])
        os.remove('answer.csv')
        os.rename("temporary.csv",'answer.csv')
'''

def add_submisson():
    return SUBMISSION_TIME

def add_question_to_file(story):

    with open('question.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER_QUESTION)
        writer.writerow(story)

