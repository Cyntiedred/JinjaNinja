import connection


@connection.connection_handler
def select_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question ORDER BY id;
                   """, )
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def select_all_answers_by_id(cursor, q_id):
    cursor.execute("""
                    SELECT * FROM answer 
                    WHERE question_id = %(q_id)s
                    ORDER BY vote_number DESC,
                            submission_time DESC;
                   """,
                   {
                       'q_id': q_id
                   })
    answers = cursor.fetchall()
    return answers


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

@connection.connection_handler
def delete_question_comments(cursor, q_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE question_id = %(q_id)s;
                   """,
                   {'q_id': q_id})

@connection.connection_handler
def new_delete_question_comments(cursor, id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(id)s;
                   """,
                   {'id': id})


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
def edit_question(cursor, q_id, title, message):
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
                    INSERT INTO comment (answer_id, message, submission_time) 
                    VALUES (%(answer_id)s, %(message)s, NOW());
                   """, {
        "answer_id": answer_id,
        "message": message,
    })


@connection.connection_handler
def get_answer_comment(cursor, a_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE answer_id = %(a_id)s;
                    """,
                   {'a_id': a_id})
    answer_comments = cursor.fetchall()
    return answer_comments

@connection.connection_handler
def get_answers_id(cursor, q_id):
    cursor.execute("""
                    SELECT id FROM answer
                    WHERE id = %(q_id)s;
                    """,{
                    'q_id':q_id,
                    })
    answer_ids=cursor.fetchall()
    return answer_ids


@connection.connection_handler
def add_new_answer(cursor, vote_number, question_id, message):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message)
                    VALUES (NOW(), %(vote_number)s, %(question_id)s, %(message)s)
                    RETURNING question_id;
                    """,
                   {
                       "vote_number": vote_number,
                       "question_id": question_id,
                       "message": message,
                   })

