from dotenv import load_dotenv
load_dotenv()
import os
from random import choice

import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

openai.api_key = os.environ.get('OPENAI_API_KEY')
start_sequence = "\nA:"
restart_sequence = "\n\nQ: "

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdjflkdsbnkjereTkadsjfab'
Bootstrap(app)

class QuestionForm(FlaskForm):
    question = StringField('Enter your question below and click submit.', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/sms', methods=['POST'])
def sms():
    question = request.form['Body'].strip()

    twiml_resp = MessagingResponse()
    twiml_resp.message(askgpt3(question))

    return str(twiml_resp)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = QuestionForm()
    message = ""
    answer = askgpt3(form.question.data)
    return render_template('index.html', form=form, message=message, answer=answer)

def askgpt3(question):
    prompt_text = 'I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: ' + str(question),

    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt_text,
      temperature=0,
      max_tokens=50,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    answer = response['choices'][0]['text']
    answer=(answer[:answer.find('Q:')])

    return answer


if __name__ == '__main__':
    app.run(host=os.environ.get("FLASK_RUN_HOST"), port=os.environ.get("FLASK_RUN_PORT"), debug=True)
