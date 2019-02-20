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
    displayed_table = table[id-1]

    return render_template('display.html', displayed_table = displayed_table, id = id )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_an_answer(question_id: int):

    previous_answers = data_handler.get_data_from_answers_csv()
    answer_adding = {
        'id':len(previous_answers),
        'submission_time': 0,
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


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )