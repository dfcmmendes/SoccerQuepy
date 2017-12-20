from flask import Flask, request, render_template
import main as quepyDbpedia

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', result = None)


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    #processed_text = text.upper()
    result = quepyDbpedia.startquepy(text)
    return render_template('index.html', result = result)


if __name__ == '__main__':
    app.run()