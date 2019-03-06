from flask import Flask, render_template, request, redirect, url_for
import time

import data_handler

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    questions = data_handler.select_all_questions()

    return render_template('list.html', questions = questions)


@app.route('/display/<int:q_id>')
def display_question(q_id):
    question_by_id = data_handler.get_question_by_id(q_id)
    data_handler.update_view_number(q_id)
    return render_template('display.html', question_by_id = question_by_id, q_id=q_id)


@app.route('/ask', methods=['GET'])
def ask_new_question():
    return render_template('ask.html')


@app.route('/ask', methods=['POST'])
def add_new_question():
    vote_number = 0
    view_number = 0
    title = request.form.get('title')
    message = request.form.get('message')
    data_handler.save_new_question(title, message, view_number,vote_number)


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



@app.route('/question/<int:q_id>/edit', methods = ['GET'])
def edit_question(q_id):
    question_by_id = data_handler.get_question_by_id(q_id)
    return render_template('edit.html', q_id = q_id, question_by_id = question_by_id)


@app.route('/question/<int:q_id>/edit', methods=['POST'])
def save_edited_question(q_id):
    title = request.form.get('title')
    message = request.form.get('message')
    data_handler.edit_question(q_id, title, message)
    return redirect(url_for('route_list'))





'''





@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_an_answer(question_id: int):

    previous_answers = data_handler.get_data_from_answers_csv()
    answer_adding = {
        'id':len(previous_answers),
        'submission_time': data_handler.add_submisson(),
        'vote_number': 0,
        'question_id':int(question_id),
        'message': request.form.get('message'),
        'image': request.form.get('image'),
    }
    if request.method == 'POST':


        data_handler.write_answers_to_csv(answer_adding)
        return render_template('answer.html',
                               previous_answers=previous_answers,
                               form_url=url_for('post_an_answer', question_id=question_id),
                               answer_adding=answer_adding
                               )

    return render_template('answer.html', previous_answers=previous_answers, answer_adding=answer_adding)



@app.route('/question/<int:id>/answer/<int:vote>')
def vote_answer(id,vote):
    table = data_handler.get_data_from_answers_csv()
    edited_answer = {
        'id': table[id]['id'],
        'submission_time': table[id]['submission_time'],
        'vote_number': int(table[id]['vote_number'])+vote,
        'question_id': table[id]['question_id'],
        'message': table[id]['message'],
        'image': table[id]['image']
    }
    data_handler.edit_answer(table,id,edited_answer,)
    return redirect(url_for('post_an_answer'))



'''
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )