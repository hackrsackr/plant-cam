# app.py
 
from flask import Flask, render_template, request, redirect, session

 
app = Flask(__name__)
 
# dictionary to store user and password
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
        # response = {}
        # response['photos'] = request.args['photos']
        # response['delay'] = request.args['delay']
        photos = request.args['photos']
        delay = request.args['delay']
        # response['fps'] = request.args['fps']
        # response['start_time'] = request.args['start_time']
        print(photos, delay)
        # context.update(response)
        # print(context)
        return render_template('index.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)