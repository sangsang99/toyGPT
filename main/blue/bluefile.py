from main import *
from flask import Blueprint, render_template

var_blue = Blueprint("blue", __name__, template_folder="templates", url_prefix='/blue')

@var_blue.route('/', methods=['POST'])
def root_prompt():
    prompt = request.form['prompt']
    return render_template('index.html', prompt=prompt)

