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













'''"""
@app.route('/question/<int:id>/edit', methods=['POST', 'GET'])
def edit_question(id):
    table = data_handler.main_page()
    title = table[id]['title']
    message = table[id]['message']
    if request.method == 'POST':
        edited_question = {
            'id': table[id]['id'],
            'submission_time': table[id]['submission_time'],
            'view_number': table[id]['view_number'],
            'vote_number': table[id]['vote_number'],
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': table[id]['image']
        }
        data_handler.edit_question(table, id, edited_question)
        return redirect(url_for('route_list'))

    return render_template('edit.html', id=id,title=title,message=message)



@app.route('/ask',  methods=['GET', 'POST'])
def ask_new_question():
    table = data_handler.main_page()
    if request.method == 'POST':
        story = {
            'id': len(table)+1,
            'submission_time': data_handler.add_submisson(),
            'view_number': 0,
            'vote_number': 0,
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image':0
        }
        data_handler.add_question_to_file(story)
        return redirect('/')


    return render_template('ask.html',form_url=url_for('ask_new_question'))

'''
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )