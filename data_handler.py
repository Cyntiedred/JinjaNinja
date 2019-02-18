import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_HEADER_QUESTION = ["id","submission_time", "view_number","vote_number","title","message","image"]
DATA_HEADER_ANSWER = ["id","submission_time","vote_number","question_id","message","image"]
DATA_HEADER_LIST = ["id","title","answer","edit","delete"]


def main_page():
    table = []
    with open(DATA_FILE_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = dict(row)
            table.append(row)
    return table

'''
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

'''


