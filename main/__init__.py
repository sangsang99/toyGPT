from flask import Flask, request, redirect

app = Flask(__name__)
 
@app.route('/')
def index():
    return ('hello.html')

from main.blue import bluefile
app.register_blueprint(bluefile.var_blue)