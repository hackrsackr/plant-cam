from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    number1 = int(data['value']) * 2
    return jsonify(result=number1)

if __name__ == '__main__':
    app.run(debug=True)