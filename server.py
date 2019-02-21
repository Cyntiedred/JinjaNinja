from flask import Flask, render_template, request, redirect, url_for


import data_handler

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    table = data_handler.main_page()

    return render_template('list.html', table=table)

@app.route('/question/<int:id>')
def display_question(id):
    table = data_handler.main_page()
    displayed_table = table[id]

    return render_template('display.html', displayed_table = displayed_table, id = id)

@app.route('/question/<int:id>/vote-up')
def question_vote_up(id):
    table = data_handler.main_page()
    vote = table[id]['vote_number']
    vote +=1
    return redirect(url_for('display_questions'))


@app.route('/question/<int:id>/vote-down')
def question_vote_down(id):
    table = data_handler.main_page()
    vote = table[id]['vote_number']
    vote -= 1
    return redirect(url_for('display_questions'))




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