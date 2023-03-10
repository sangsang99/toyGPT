from main import *
from flask import Blueprint, render_template
from main.service import openAI_input, key

## 선언부 ===================================================================================
var_blue = Blueprint("blue", __name__, template_folder="templates", url_prefix='/blue')



# Tistory Open API URL
tistory_post_url = 'https://www.tistory.com/apis/post/write'

# csv저장 절대경로
csv_path = 'D:\kukbee\openAI\csv\\'

@var_blue.route('/', methods=['POST'])
def root_prompt():
    prompt = request.form['prompt']

    # 블로그 제목과 글을 생성합니다.
    content = openAI_input.prompt_factory.get_blog_content(key.openai_api_key, prompt)
    print(f'content : "{content}"')

    # Unsplash에서 이미지 URL을 가져옵니다.
    image_url = openAI_input.prompt_factory.get_image_url(key.unsplash_api_key, prompt)

    # Save the data as a CSV file.
    data = [prompt, content.strip(), image_url]
    filename = prompt + '.csv'
    openAI_input.prompt_factory.save_to_csv(data, filename)

    return render_template('index.html', prompt=prompt, content=content, image_url=image_url)
