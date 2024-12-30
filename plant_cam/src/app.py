# app.py
import json
from flask import Flask, render_template, request, jsonify

 
app = Flask(__name__)
 
context = {
    'enabled': True,
    'photos': 2,
    'delay': 30,
    'fps': 12,
    'start_time': '08:00'
}

@app.route('/')
def view_form():
    return render_template('index.html', context=context)
 
@app.route('/handle_get', methods=['GET'])
def handle_get():
    if request.method == 'GET':
        for key in context:
            if request.args.get(key):
                context[key] = request.args.get(key)
                
    print(f"context: {context}")
    return render_template('index.html', context=context)
    
@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        print(request)
        for key in context:
            if request.form[key]:
                context[key] = request.form[key]

    print(f"context: {context}")
    return render_template('index.html', context=context)

if __name__ == '__main__':
    app.run(debug=True)