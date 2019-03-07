from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)


@app.route('/')
def show_five_latest_questions():
    latest_questions = data_handler.select_five_latest_questions()
    return render_template('five_latest_questions.html', questions=latest_questions)


############################### MAIN PAGE ############################################


@app.route('/list')
def route_list():
    questions = data_handler.select_all_questions()

    return render_template('list.html', questions=questions)


############################### QUESTION PAGE############################################

#DETAILS ABOUT QUESTION, COMMENTS OF THE QUESTION, ANSWERS OF THE QUESTION


@app.route('/display/<int:q_id>')
def display_question(q_id):
    question_by_id = data_handler.get_question_by_id(q_id)
    data_handler.update_view_number(q_id)
    answers = data_handler.select_all_answers_by_id(q_id)
    question_comments = data_handler.get_question_comment()
    answer_comments = data_handler.get_answer_comment()

    return render_template('display.html',
                           question_by_id=question_by_id,
                           q_id=q_id,
                           question_comments=question_comments,
                           answers=answers, answer_comments = answer_comments)


############################### NEW STUFF  ############################################


##### NEW COMMENT TO THE QUESTION


@app.route('/question/<q_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_question(q_id):
    if request.method == 'GET':
        return render_template('question_comment.html', q_id=q_id)

    message = request.form.get('message')
    data_handler.add_new_comment_for_question(q_id, message)
    return redirect(url_for('display_question', q_id=q_id))


##### NEW COMMENT TO THE ANSWER


##### NEW QUESTION IN GENERAL


@app.route('/ask', methods=['GET'])
def ask_new_question():
    return render_template('ask.html')


@app.route('/ask', methods=['POST'])
def add_new_question():
    vote_number = 0
    view_number = 0
    title = request.form.get('title')
    message = request.form.get('message')
    data_handler.save_new_question(title, message, view_number, vote_number)

    return redirect(url_for('route_list'))


##### NEW ANSWER IN GENERAL

@app.route('/display/<int:q_id>', methods=['POST'])
def add_new_answer(q_id):
    vote_number = 0
    message = request.form.get('message')
    data_handler.add_new_answer(vote_number, q_id, message)
    return redirect(url_for('display_question', q_id=q_id))



############################### EDIT STUFF ############################################


##### VOTE QUESTION UP OR DOWN


@app.route('/question/<int:q_id>/vote-<string:vote>')
def vote(q_id, vote):
    data_handler.vote_for_questions(q_id, 1 if vote == 'up' else -1)
    return redirect(url_for('display_question', q_id=q_id))

##### VOTE ANSWER UP OR DOWN

@app.route('/answer/<int:a_id>/vote-<string:vote>')
def vote_for_answer(a_id, vote):
    data_handler.vote_for_answers(a_id, 1 if vote == 'up' else -1)
    q_id = data_handler.get_question_id_by_answer(a_id)
    return redirect(url_for('display_question', q_id=q_id))


##### DELETE WHOLE QUESTION

@app.route('/question/<int:q_id>/delete')
def delete(q_id):
    data_handler.delete_answers_by_question_id(q_id)
    data_handler.delete_question(q_id)
    return redirect(url_for('route_list'))


##### EDIT QUESTION


@app.route('/question/<int:q_id>/edit', methods=['GET'])
def edit_question(q_id):
    question_by_id = data_handler.get_question_by_id(q_id)
    return render_template('edit.html', q_id=q_id, question_by_id=question_by_id)


@app.route('/question/<int:q_id>/edit', methods=['POST'])
def save_edited_question(q_id):
    title = request.form.get('title')
    message = request.form.get('message')
    data_handler.edit_question(q_id, title, message)
    return redirect(url_for('route_list'))

##### EDIT ANSWER


@app.route('/answer/<int:a_id>/edit', methods=['GET'])
def edit_answer(a_id):
    answer_by_id = data_handler.get_answer_by_id(a_id)
    return render_template('edit_answer.html', a_id=a_id, answer_by_id=answer_by_id)


@app.route('/answer/<int:a_id>/edit', methods=['POST'])
def save_edited_answer(a_id):

    message = request.form.get('message')
    data_handler.edit_answer(a_id, message)
    q_id = data_handler.get_question_id_by_answer(a_id)
    return redirect(url_for('display_question', q_id=q_id))

##### EDIT QUESTION COMMENT

#@app.route('/answer/<int:a_id>/edit', methods=['POST'])

##### EDIT ANSWER COMMENT


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
