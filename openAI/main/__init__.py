from flask import Flask, request, redirect,render_template

app = Flask(__name__)

#기본
@app.route('/')
def index():
    return render_template('hello.html')


#blue모듈 설정
from main.blue import bluefile
app.register_blueprint(bluefile.var_blue)