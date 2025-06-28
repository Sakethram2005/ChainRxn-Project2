from flask import Flask, render_template, request
import requests

app = Flask(__name__)
backend_url = "http://127.0.0.1:5000"

@app.route('/')
def index():
    return render_template("app.html")

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.form['data']
    res = requests.post(f"{backend_url}/addBlock", json={"data": data})
    return render_template("app.html", result=res.json())

@app.route('/get_latest_block')
def get_latest_block():
    res = requests.get(f"{backend_url}/getlatestblock")
    return render_template("app.html", result=res.json())

@app.route('/get_full_chain')
def get_chain():
    res = requests.get(f"{backend_url}/getchain")
    return render_template("app.html", result=res.json())

if __name__ == '__main__':
    app.run(port=8000)
