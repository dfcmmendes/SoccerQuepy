from flask import Flask, request, render_template
import main as quepyDbpedia

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    #processed_text = text.upper()
    return quepyDbpedia.startquepy(text)

if __name__ == '__main__':
    app.run()