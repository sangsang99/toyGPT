from flask import Flask
 
app = Flask(__name__)
 
 
@app.route('/')
def index():
    return '안녕'
 
 
app.run(port=5001, debug=True)