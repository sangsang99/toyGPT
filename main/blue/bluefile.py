from main import *
from flask import Blueprint, render_template
from main.service import openAI_input, key, local_IO
import datetime

## 선언부 ===================================================================================
var_blue = Blueprint("blue", __name__, template_folder="templates", url_prefix='/blue')

# Tistory Open API URL
tistory_post_url = 'https://www.tistory.com/apis/post/write'

# csv저장 절대경로
csv_path = 'D:\kukbee\openAI\csv\\'


## index페이지 호출 ===================================================================================
@var_blue.route('/', methods=['POST'])
def root_prompt():
    prompt = request.form['prompt']

    # 블로그 제목과 글을 생성합니다.
    content = openAI_input.prompt_factory.get_blog_content(key.openai_api_key, prompt)

    # 블로그 글의 요약문을 생성합니다.
    summary = openAI_input.prompt_factory.get_summary(key.openai_api_key, content)

    # Unsplash에서 이미지 URL을 가져옵니다.
    image_url = openAI_input.prompt_factory.get_image_url(key.unsplash_api_key, summary)

    # 생성된 글을 토대로 tag를 생성합니다.
    tag = openAI_input.prompt_factory.get_tag(key.openai_api_key, summary)

    #today
    today_now = datetime.datetime.now()
    today = today_now.strftime('%Y-%m-%d')

    # Save the data as a CSV file and IMG file.
    data = [prompt, content, image_url, summary, tag]
    local_IO.save_to_csv(data, prompt)
    local_IO.save_url_img(image_url, prompt)

    return render_template('index.html', prompt=prompt, content=content, image_url=image_url, today=today, summary=summary, tags=tag)
