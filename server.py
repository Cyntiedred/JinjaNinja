from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    questions = data_handler.select_all_questions()

    return render_template('list.html', questions=questions)


@app.route('/display/<int:q_id>')
def display_question(q_id):
    question_by_id = data_handler.get_question_by_id(q_id)
    data_handler.update_view_number(q_id)
    answers = data_handler.select_all_answers_by_id(q_id)
    question_comments = data_handler.get_question_comment(q_id)

    return render_template('display.html',
                           question_by_id=question_by_id,
                           q_id=q_id,
                           question_comments=question_comments,
                           answers=answers
                            )



@app.route('/question/<q_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_question(q_id):
    if request.method == 'GET':
        return render_template('question_comment.html', q_id=q_id)

    message = request.form.get('message')
    data_handler.add_new_comment_for_question(q_id, message)
    return redirect(url_for('display_question', q_id=q_id))



@app.route('/answer/<a_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_answer(a_id):
    if request.method == 'GET':
        return render_template('answer_comment.html', a_id=a_id)

    message = request.form.get('message')
    data_handler.add_new_comment_for_answer(a_id, message)
    return redirect(url_for('answer_comment', a_id=a_id))


@app.route('/answer/<a_id>/new-comment', methods=['GET', 'POST'])
def new_answer_comment(a_id):
    answer_comments = data_handler.get_answer_comment(a_id)

    return redirect(url_for('answer_comment', a_id=a_id, answer_comments=answer_comments))


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


@app.route('/question/<int:q_id>/vote-<string:vote>')
def vote(q_id, vote):
    data_handler.vote_for_questions(q_id, 1 if vote == 'up' else -1)
    return redirect(url_for('display_question', q_id=q_id))


@app.route('/question/<int:q_id>/delete')
def delete(q_id):
    data_handler.delete_answers_by_question_id(q_id)
    data_handler.delete_question(q_id)
    return redirect(url_for('route_list'))


@app.route('/comments/int:<q_id>/delete')
def delete_question_comment(q_id):
    data_handler.delete_question_comments(q_id)

    return redirect(url_for('display_question', q_id=q_id))


@app.route('/display/<int:q_id>', methods=['POST'])
def add_new_answer(q_id):
    vote_number = 0
    message = request.form.get('message')
    data_handler.add_new_answer(vote_number, q_id, message)
    return redirect(url_for('display_question', q_id=q_id))


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


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
