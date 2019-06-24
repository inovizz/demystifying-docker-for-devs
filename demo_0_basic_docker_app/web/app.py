from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello World from Hyderabad Python Group!<br></h1>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
