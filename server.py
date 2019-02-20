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
    displayed_table = table[id-1]

    return render_template('display.html', displayed_table = displayed_table, id = id )





if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )