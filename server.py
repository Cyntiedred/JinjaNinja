from flask import Flask, render_template, request, redirect, url_for


import data_handler

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    table = data_handler.main_page()

    return render_template('list.html', table=table)


@app.route('/display/<int:id>')
def display_question(id):
    table = data_handler.main_page()
    displayed_table = table[id]

    return render_template('display.html', displayed_table = displayed_table, id = id)

#ASOUMÉ
@app.route('/question/<int:id>/vote-up')
def question_vote_up(id):
    table = data_handler.main_page()
    vote = table[id]['vote_number']
    vote +=1
    return redirect(url_for('display_questions'))

#ASOUMÉ
@app.route('/question/<int:id>/vote-down')
def question_vote_down(id):
    table = data_handler.main_page()
    vote = table[id]['vote_number']
    vote -= 1
    return redirect(url_for('display_questions'))




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

#ASOUMÉ
@app.route('/question/<question_id>/new-answer/vote-up')
def answer_vote_up(question_id: int):
    table = data_handler.get_data_from_answers_csv()
    vote = table[question_id]['vote_number']
    vote -= 1
    return render_template('answer.html',
                           previous_answers=previous_answers,
                           question_id=question_id,
                           answer_adding=answer_adding
                           )
#ASOUMÉ
@app.route('/question/<question_id>/new-answer/vote-down')
def answer_vote_down(question_id: int):
    table = data_handler.get_data_from_answers_csv()
    vote = table[question_id]['vote_number']
    vote -= 1
    return render_template('answer.html',
                           previous_answers=previous_answers,
                           fquestion_id=question_id,
                           answer_adding=answer_adding
                           )

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


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )