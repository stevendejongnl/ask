from flask import Flask, render_template, request, jsonify, abort
import logging
from openai import OpenAI

__version__ = '0.1.0'
app = Flask(__name__)
app.secret_key = 'mega-secret-ask'
app.logger.setLevel(logging.INFO)

client = OpenAI()

title = "Ask Steven"
description = "Ask just stuff.."

@app.route('/')
def index():
    return render_template(
        'index.html',
        title=title,
        description=description
    )


@app.route('/ask', methods=['POST'])
def ask():
    if request.method == 'POST':
        question = request.form['question']

        app.logger.info(f"Question: {question}")
        response = client.responses.create(
            model="gpt-4.1",
            instructions="Answer super sarcastic and as if Steven gives you the answer",
            input=question
        )

        app.logger.info(f"Ai response: {response.output_text=}")
        return jsonify({
            "answer": response.output_text
        })
    
    return abort(405)
