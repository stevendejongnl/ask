from flask import Flask, render_template, request, abort
from openai import OpenAI

__version__ = '0.1.0'
app = Flask(__name__)
app.secret_key = 'mega-secret-ask'

client = OpenAI()

@app.route('/')
def index():
    return render_template(
        'index.html',
        title='Ask',
        description='Ask stuff.'
    )


@app.route('/ask', methods=['POST'])
def ask():
    if request.method == 'POST':
        question = request.form['question']

        try:
            response = client.responses.create(
                model="gpt-4.1",
                instructions="Answer super sarcastic.",
                input=question
            )
            print(response, response.output_text)
            ai_response = response.output_text[0]['content']['text']
        except:
            ai_response = None

        return render_template(
            'index.html',
            title='Ask',
            description='Ask stuff.',
            ai_response=ai_response,
        )
    
    return abort(405)
