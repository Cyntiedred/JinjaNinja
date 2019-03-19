import connection


@connection.connection_handler
def select_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question ORDER BY id;
                   """, )
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def select_five_latest_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question 
                    ORDER BY submission_time DESC 
                    LIMIT 5;
                   """, )
    latest_questions = cursor.fetchall()
    return latest_questions


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
def get_answer_by_id(cursor, a_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(a_id)s
                    """,
                   {'a_id': a_id})
    answer_by_id = cursor.fetchall()
    return answer_by_id


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
def get_comment_by_id(cursor, c_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id = %(c_id)s
                    """,
                   {'c_id': c_id})
    comment_by_id = cursor.fetchall()
    return comment_by_id


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
def vote_for_answers(cursor, a_id, vote):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number+%(vote)s
                    WHERE id = %(a_id)s;
                   """,
                   {'a_id': a_id, 'vote': vote})


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
def delete_answer_comments(cursor, a_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(a_id)s;
                   """,
                   {'a_id': a_id})


@connection.connection_handler
def delete_comments(cursor, c_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(c_id)s;
                   """,
                   {'c_id': c_id})


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
def get_question_comment(cursor):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id IS NOT NULL
                    """, )
    question_comments = cursor.fetchall()
    return question_comments


@connection.connection_handler
def get_answer_comment(cursor):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE answer_id IS NOT NULL
                    """, )
    answer_comments = cursor.fetchall()
    return answer_comments


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


@connection.connection_handler
def add_new_comment_for_question(cursor, question_id, message):
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, edited_count) 
                    VALUES (%(question_id)s, %(message)s, NOW(), 0);
                   """, {
        "question_id": question_id,
        "message": message,
    })


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


@connection.connection_handler
def edit_answer(cursor, a_id, message):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s
                    WHERE id = %(a_id)s;
                   """,
                   {'a_id': a_id, 'message': message})


@connection.connection_handler
def get_question_id_by_answer(cursor, a_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(a_id)s;
                   """,
                   {'a_id': a_id})
    q_id = cursor.fetchone()
    return q_id['question_id']


@connection.connection_handler
def search_in_questions_and_answers(cursor, message):
    cursor.execute("""
                    SELECT *
                    FROM question
                    FULL JOIN answer
                        ON question.id = answer.question_id
                    WHERE title ILIKE %(message)s 
                        OR question.message ILIKE %(message)s
                        OR answer.message ILIKE %(message)s;
                    """,
                   {
                       'message': "%" + message + "%",
                   })
    found_question = cursor.fetchall()
    return found_question


@connection.connection_handler
def get_question_id_by_comment(cursor, c_id):
    cursor.execute("""
                    SELECT question_id, answer_id FROM comment
                    WHERE id = %(c_id)s;
                   """,
                   {'c_id': c_id})
    q_id = cursor.fetchone()
    if q_id['question_id'] == None:
        a_id = q_id['answer_id']
        cursor.execute("""
                               SELECT question_id FROM answer
                               WHERE id = %(a_id)s;
                              """,
                       {'a_id': a_id})
        q_id = cursor.fetchone()
    return q_id['question_id']


@connection.connection_handler
def edit_comment(cursor, c_id, edited_count_add, message):
    cursor.execute("""
                    UPDATE comment
                    SET edited_count = edited_count+%(edited_count_add)s, message = %(message)s, submission_time = NOW()
                    WHERE id = %(c_id)s;
                   """,
                   {'c_id': c_id, 'edited_count_add': edited_count_add, 'message': message})


@connection.connection_handler
def register_a_new_user(cursor, user_name, email, password):
    cursor.execute("""
                    INSERT INTO users (user_name, email, password)
                    VALUES (%(user_name)s, %(email)s, %(password)s)
                    """,
                   {
                       "user_name": user_name,
                       "email": email,
                       "password": password,
                   })
