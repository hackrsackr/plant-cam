# app.py
 
from flask import Flask, render_template, request

 
app = Flask(__name__)
 
context = {
    'photos': 2,
    'delay': 30,
    'fps': 12,
    'start_time': "08:00"
}

# To render a login form 
@app.route('/')
def view_form():
    return render_template('index.html', context=context)
 
# For handling get request form we can get
# the form inputs value by using args attribute.
# this values after submitting you will see in the urls.
# e.g http://127.0.0.1:5000/handle_get?username=kunal&password=1234
# this exploits our credentials so that's 
# why developers prefer POST request.
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
        for key in context:
            if request.form[key]:
                print(request.form[key])
                context[key] = request.form[key]

    print(f"context: {context}")
    return render_template('index.html', context=context)

if __name__ == '__main__':
    app.run(debug=True)