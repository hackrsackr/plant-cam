# app.py
import json

from flask import Flask, render_template, request 

app = Flask(__name__)
 
with open('config.json', 'r') as f:
    cfg =json.load(f)
    context = dict(cfg['public'])

@app.route('/')
def view_form():
    return render_template('index.html', context=context)


@app.route('/handle_request', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        for key in context:
            if request.form[key]:
                context[key] = request.form[key]

    if request.method == 'GET':
        for key in context:
            if request.args.get(key):
                context[key] = request.args.get(key)

    print(f"context: {context}")
    return render_template('index.html', context=context)


@app.route('/reset_config', methods=['POST'])
def reset():
    if request.method == 'POST':
        context = dict(cfg['public'])
    
    print(f"context: {context}")
    return render_template('index.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)