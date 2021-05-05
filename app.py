from flask import Flask, session, flash, request, render_template, redirect
from surveys import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'test'


@app.route('/', methods=['POST', 'GET'])
def index():
    session['responses'] = []
    return render_template('index.html', title=satisfaction_survey.title, 
    instructions=satisfaction_survey.instructions)

@app.route('/questions/<id>')
def question(id):

    if int(id) > len(session['responses']):
        flash('Questions must be answered in order!')
        return redirect(f'/questions/{len(session["responses"])}')
    question_info = satisfaction_survey.questions[int(id)]

    question = question_info.question
    choices = question_info.choices
    allow_text = question_info.allow_text

    return render_template('question.html', question=question, choices=choices, allow_text=allow_text, id=int(id))

@app.route("/answer/<id>", methods=['POST'])
def answer(id):
    choice = request.form["answer"]
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses
    if limit != int(id) + 1:
        return redirect(f'/questions/{int(id) + 1}')
    return render_template('thank-you.html')

limit = len(satisfaction_survey.questions)
