import connection


@connection.connection_handler
def select_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question ORDER BY id;
                   """,)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_question_by_id(cursor, q_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(q_id)s
                    """,
                   {'q_id': q_id})
    question_by_id = cursor.fetchall()
    return question_by_id


@connection.connection_handler
def get_answer_by_id(cursor, a_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(a_id)s
                    """,
                   {'a_id': a_id})
    answer_by_id = cursor.fetchall()
    return answer_by_id


@connection.connection_handler
def update_view_number(cursor, q_id):
    cursor.execute("""
                    UPDATE question SET view_number = (view_number + 1)
                    WHERE id = %(q_id)s;
                   """,
                   {'q_id': q_id})


@connection.connection_handler
def vote_for_questions(cursor, q_id, vote):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number+%(vote)s
                    WHERE id = %(q_id)s;
                   """,
                   {'q_id': q_id, 'vote': vote})


@connection.connection_handler
def delete_question(cursor, q_id):
    delete_question_tag_connection(cursor, q_id)
    delete_question_comments(cursor, q_id)
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(q_id)s;
                   """,
                   {'q_id': q_id})


def delete_question_tag_connection(cursor, q_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(q_id)s;
                   """,
                   {'q_id': q_id})


def delete_question_comments(cursor, q_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE question_id = %(q_id)s;
                   """,
                   {'q_id': q_id})


@connection.connection_handler
def delete_answers_by_question_id(cursor, q_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id = %(q_id)s;
                   """,
                   {'q_id': q_id})


@connection.connection_handler
def save_new_question(cursor, title, message, view_number, vote_number):
    cursor.execute("""
                    INSERT INTO question (submission_time, title,  message, view_number, vote_number) 
                    VALUES (NOW(), %(title)s, %(message)s, %(view_number)s, %(vote_number)s)
                    RETURNING id;
                   """, {
        "title": title,
        "message": message,
        "view_number": view_number,
        "vote_number": vote_number,
                        })
    new_question = cursor.fetchall()
    return new_question

@connection.connection_handler
def edit_question(cursor,q_id, title, message):
    cursor.execute("""
                    UPDATE question
                    SET title = %(title)s, message = %(message)s
                    WHERE id = %(q_id)s;
                   """,
                   {'q_id': q_id, 'title': title, 'message': message})

@connection.connection_handler
def add_new_comment_for_question(cursor, question_id, message):
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time) 
                    VALUES (%(question_id)s, %(message)s, NOW());
                   """, {
        "question_id": question_id,
        "message": message,
    })


@connection.connection_handler
def get_question_comment(cursor, q_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %(q_id)s
                    """,
                   {'q_id': q_id})
    question_comments = cursor.fetchall()
    return question_comments


@connection.connection_handler
def add_new_comment_for_answer(cursor, answer_id, message):
    cursor.execute("""
                    INSERT INTO comment (answer_id, message, submission_time, edited_count) 
                    VALUES (%(answer_id)s, %(message)s, NOW(), 0)
                    RETURNING id;
                   """, {
        "answer_id": answer_id,
        "message": message,
    })
    answer_comment = cursor.fetchall()
    return answer_comment


'''
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
            row['submission_time'] = int(row['submission_time'])
            row['view_number'] = int(row['view_number'])
            row['view_number'] += 1
            row = dict(row)
            table.append(row)
    return table



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


def add_submisson():
    return SUBMISSION_TIME

def add_question_to_file(story):

    with open('question.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER_QUESTION)
        writer.writerow(story)

'''