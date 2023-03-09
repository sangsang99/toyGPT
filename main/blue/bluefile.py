from main import *
from flask import Blueprint, render_template

var_blue = Blueprint("blue", __name__, template_folder="templates", url_prefix='/blue')

@var_blue.route('/')
def root():
    return render_template('hello.html')

@var_blue.route('/<get>')
def root_get(get):
    return render_template('hello.html', getValue=get)