from flask import Flask, render_template

__version__ = '0.1.0'
app = Flask(__name__)
app.secret_key = 'mega-secret-ask'

@app.route('/')
def index():
    return render_template(
        'index.html',
        title='Ask',
        description='Ask stuff.'
    )