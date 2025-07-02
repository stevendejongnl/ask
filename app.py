from flask import Flask, render_template, request, jsonify, abort
import logging
import json
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
        
        history_json = request.form.get('history', '[]')
        try:
            conversation_history = json.loads(history_json)
        except json.JSONDecodeError:
            conversation_history = []

        app.logger.info(f"Question: {question}")
        app.logger.info(f"History length: {len(conversation_history)}")
        
        messages = [
            {
                "role": "system", 
                "content": "You are Steven, a sarcastic and witty person who always responds with humor and irony. Give answers that are helpful but delivered in a very sarcastic, dry, and slightly condescending tone. Use plenty of sarcasm, eye-rolling moments, and playful mockery while still being informative. Respond as if you're slightly annoyed but amused by the question."
            }
        ]
        

        messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": question})
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            temperature=0.8
        )

        answer = response.choices[0].message.content
        app.logger.info(f"AI response: {answer}")
        
        return jsonify({
            "answer": answer
        })
    
    return abort(405)
