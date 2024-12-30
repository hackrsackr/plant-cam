# app.py
import json
from flask import Flask, render_template, request 

app = Flask(__name__)
 
with open('config.json', 'r') as f:
    cfg =json.load(f)

context = dict(cfg['public'])


# context = {
    # 'number_of_photos': cfg['public']['number_of_photos'],
    # 'delay': cfg['public']['secs_between_photos'],
    # 'fps': cfg['public']['frames_per_second'],
    # 'start_time': cfg['public']['start_time']
# }

@app.route('/')
def view_form():
    return render_template('index.html', context=context, bg_class='classy')
 
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
                context[key] = request.form[key]

    print(f"context: {context}")
    return render_template('index.html', context=context)

if __name__ == '__main__':
    app.run(debug=True)