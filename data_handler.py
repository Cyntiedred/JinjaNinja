import csv
import os
import datetime
import time



DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_HEADER_QUESTION = ["id","submission_time", "view_number","vote_number","title","message","image"]
DATA_HEADER_ANSWER = ["id","submission_time","vote_number","question_id","message","image"]
DATA_HEADER_LIST = ["id","title","answer","edit","delete"]
SUBMISSION_TIME = datetime.datetime.now().strftime("%s")


def main_page():
    table = []
    with open('question.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['submission_time'] = time.ctime(int(row['submission_time']))
            row = dict(row)
            table.append(row)
    return table


def get_data_from_answers_csv():
    table = []
    with open('answer.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['submission_time']=time.ctime(int(row['submission_time']))
            line = dict(row)
            table.append(line)
    return table


def write_answers_to_csv(add_to_file):
    with open('answer.csv', 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER_ANSWER)
        writer.writerow(add_to_file)



def save_story(story_data):
    with open(DATA_FILE_PATH, 'a') as csvfile:
        fieldnames = DATA_HEADER
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(story_data)


def modify_story(table, id, story_data):
    with open('temporary.csv', 'a') as csvfile:
        fieldnames = DATA_HEADER
        fieldnamewriter = csv.writer(csvfile)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        fieldnamewriter.writerow(fieldnames)
        for i in range(id-1):
            writer.writerow(table[i])
        writer.writerow(story_data)
        for i in range(id, len(table)):
            writer.writerow(table[i])
        os.remove('data.csv')
        os.rename("temporary.csv",'data.csv')



def get_next_vote():
    pass


def add_submisson():
    return SUBMISSION_TIME

def add_question_to_file(story):

    with open('question.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER_QUESTION)
        writer.writerow(story)