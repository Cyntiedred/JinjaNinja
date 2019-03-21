from flask import Flask, render_template, request, redirect, url_for, session, escape

import data_handler
import password

app = Flask(__name__)
app.secret_key = b'_7sfFSd5hgHd_?#i324'


@app.route('/')
def show_five_latest_questions():
    if 'email' in session:
        anti_popup = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        anti_popup = True
        user_name=None

    latest_questions = data_handler.select_five_latest_questions()
    answer_comments = data_handler.get_answer_comment()
    return render_template('five_latest_questions.html',
                           questions=latest_questions,
                           answer_comments=answer_comments,
                           anti_popup=anti_popup,
                           user_name=user_name)


############################### MAIN PAGE ############################################


@app.route('/list')
def route_list():
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name=None


    questions = data_handler.select_all_questions()

    return render_template('list.html',
                           questions=questions,
                           script=script,
                           user_name=user_name)


############################### QUESTION PAGE############################################

# DETAILS ABOUT QUESTION, COMMENTS OF THE QUESTION, ANSWERS OF THE QUESTION


@app.route('/display/<int:q_id>')
def display_question(q_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    question_by_id = data_handler.get_question_by_id(q_id)
    data_handler.update_view_number(q_id)
    answers = data_handler.select_all_answers_by_id(q_id)
    question_comments = data_handler.get_question_comment()
    answer_comments = data_handler.get_answer_comment()

    return render_template('display.html',
                           question_by_id=question_by_id,
                           q_id=q_id,
                           question_comments=question_comments,
                           answers=answers,
                           answer_comments=answer_comments,
                           script=script,
                           user_name=user_name)


############################### NEW STUFF  ############################################


##### NEW COMMENT TO THE QUESTION


@app.route('/question/<q_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_question(q_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
        user_id = data_handler.get_user_id_by_email(session['email'])
    else:
        script = True
        user_name = None

    if request.method == 'GET':
        return render_template('question_comment.html', q_id=q_id)

    message = request.form.get('message')
    data_handler.add_new_comment_for_question(q_id, message, user_id)
    return redirect(url_for('display_question',
                            q_id=q_id,
                            script=script,
                            user_name=user_name))


##### NEW COMMENT TO THE ANSWER


@app.route('/answer/<a_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_answer(a_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
        user_id = data_handler.get_user_id_by_email(session['email'])
    else:
        script = True
        user_name = None

    if request.method == 'GET':
        return render_template('answer_comment.html',
                                a_id=a_id,
                                user_name=user_name)

    message = request.form.get('message')
    data_handler.add_new_comment_for_answer(a_id, message, user_id)
    q_id = data_handler.get_question_id_by_answer(a_id)

    return redirect(url_for('display_question',
                            q_id=q_id,
                            script=script,
                            user_name=user_name))


##### NEW QUESTION IN GENERAL


@app.route('/ask', methods=['GET'])
def ask_new_question():
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    return render_template('ask.html',
                           script=script,
                           user_name=user_name)


@app.route('/ask', methods=['POST'])
def add_new_question():
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
        user_id = data_handler.get_user_id_by_email(session['email'])
    else:
        script = True
        user_name = None

    vote_number = 0
    view_number = 0
    title = request.form.get('title')
    message = request.form.get('message')
    data_handler.save_new_question(title, message, view_number, vote_number, user_id)

    return redirect(url_for('route_list',
                            script=script,
                            user_name=user_name))


##### NEW ANSWER IN GENERAL

@app.route('/display/<int:q_id>', methods=['POST'])
def add_new_answer(q_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
        user_id = data_handler.get_user_id_by_email(session['email'])
    else:
        script = True
        user_name = None

    vote_number = 0
    message = request.form.get('message')
    data_handler.add_new_answer(vote_number, q_id, message, user_id)
    return redirect(url_for('display_question',
                            q_id=q_id,
                            script=script,
                            user_name=user_name))


############################### EDIT STUFF ############################################


##### VOTE QUESTION UP OR DOWN


@app.route('/question/<int:q_id>/vote-<string:vote>')
def vote(q_id, vote):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    data_handler.vote_for_questions(q_id, 1 if vote == 'up' else -1)
    return redirect(url_for('display_question',
                            q_id=q_id,
                            script=script,
                            user_name=user_name))


##### VOTE ANSWER UP OR DOWN

@app.route('/answer/<int:a_id>/vote-<string:vote>')
def vote_for_answer(a_id, vote):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    data_handler.vote_for_answers(a_id, 1 if vote == 'up' else -1)
    q_id = data_handler.get_question_id_by_answer(a_id)
    return redirect(url_for('display_question',
                            q_id=q_id,
                            script=script,
                            user_name=user_name))


############################### DELETE STUFF ############################################

##### DELETE WHOLE QUESTION

@app.route('/question/<int:q_id>/delete')
def delete(q_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    data_handler.delete_answers_by_question_id(q_id)
    data_handler.delete_question(q_id)
    return redirect(url_for('route_list',
                            script=script,
                            user_name=user_name))


##### DELETE QUESTION_COMMENT

@app.route('/comments/int:<c_id>/delete')
def delete_question_comment(c_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    comment_by_id = data_handler.get_comment_by_id(c_id)
    data_handler.delete_comments(c_id)

    return redirect(url_for('route_list',
                            comment_by_id=comment_by_id,
                            script=script,
                            user_name=user_name))


@app.route('/comments/int:<c_id>/delete')
def delete_answer_comment(c_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    comment_by_id = data_handler.get_comment_by_id(c_id)
    data_handler.delete_comments(c_id)

    return redirect(url_for('route_list',
                            c_id=c_id,
                            comment_by_id=comment_by_id,
                            script=script,
                            user_name=user_name))


##### EDIT QUESTION


@app.route('/question/<int:q_id>/edit', methods=['GET'])
def edit_question(q_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    question_by_id = data_handler.get_question_by_id(q_id)
    return render_template('edit.html',
                           q_id=q_id,
                           question_by_id=question_by_id,
                           script=script,
                           user_name=user_name)


@app.route('/question/<int:q_id>/edit', methods=['POST'])
def save_edited_question(q_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    title = request.form.get('title')
    message = request.form.get('message')
    data_handler.edit_question(q_id, title, message)
    return redirect(url_for('route_list',
                            script=script,
                            user_name=user_name))


##### EDIT ANSWER


@app.route('/answer/<int:a_id>/edit', methods=['GET'])
def edit_answer(a_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    answer_by_id = data_handler.get_answer_by_id(a_id)
    return render_template('edit_answer.html',
                           a_id=a_id,
                           answer_by_id=answer_by_id,
                           script=script,
                           user_name=user_name)


@app.route('/answer/<int:a_id>/edit', methods=['POST'])
def save_edited_answer(a_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    message = request.form.get('message')
    data_handler.edit_answer(a_id, message)
    q_id = data_handler.get_question_id_by_answer(a_id)
    return redirect(url_for('display_question',
                            q_id=q_id,
                            script=script,
                            user_name=user_name))


##### EDIT COMMENT

@app.route('/comment/<int:c_id>/edit', methods=['GET'])
def edit_comment(c_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    comment_by_id = data_handler.get_comment_by_id(c_id)
    return render_template('edit_comment.html',
                           c_id=c_id,
                           comment_by_id=comment_by_id,
                           script=script,
                           user_name=user_name)


@app.route('/comment/<int:c_id>/edit', methods=['POST'])
def save_edited_comment(c_id):
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    edited_count_add = 1
    message = request.form.get('message')
    data_handler.edit_comment(c_id, edited_count_add, message)
    q_id = data_handler.get_question_id_by_comment(c_id)
    return redirect(url_for('display_question',
                            q_id=q_id,
                            script=script,
                            user_name=user_name))


@app.route('/search', methods=['GET', 'POST'])
def search_content():
    if 'email' in session:
        script = False
        user_name = data_handler.get_user_by_email(session['email'])
    else:
        script = True
        user_name = None

    searched__phrase = request.form.get('search_phrase')
    found_content = data_handler.search_in_questions_and_answers(searched__phrase)
    return render_template('search.html',
                           found_content=found_content,
                           script=script,
                           user_name=user_name)

############################### REGISTRATION AND LOGIN STUFF ############################################



@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')
        if pass1 == pass2:
            hashed_pass = password.hash_password(pass1)
            data_handler.register_a_new_user(user_name, email, hashed_pass)
            return redirect(url_for('show_five_latest_questions'))
        else:
            return render_template('registration.html')

    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        pass1 = request.form.get('pass1')
        hashed_pass_from_database = data_handler.get_user_info_to_login(email)

        if hashed_pass_from_database:
            verification = password.verify_password(pass1, hashed_pass_from_database)


            if verification:
                session['email'] = request.form.get('email')
                return redirect(url_for('show_five_latest_questions'))
            else:
                text = "False user name or password. Try again!"
                return render_template('login.html', text=text)

        text = "False user name or password. Try again!"
        return render_template('login.html', text=text)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('show_five_latest_questions'))


@app.route('/users')
def show_all_users():
    users_data = data_handler.get_all_user_data()

    return render_template('users.html', users_data=users_data)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
