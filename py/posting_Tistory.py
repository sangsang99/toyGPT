"""READ_ME
미리 저장해둔 csv파일을 통해서 Tistory에 블로깅합니다.
csv_column_title : 질문,카테고리,자동화,본문,요약문,태그,이미지URL,이미지,Result
use_by_coulmn_num : 질문(0),카테고리(1),자동화,본문(3),요약문(4),태그(5),이미지URL(6),이미지(7),Result
"""

"""Tistroy POST 인자
blogName: Blog Name (필수)
title: 글 제목 (필수)
content: 글 내용
visibility: 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
category: 카테고리 아이디 (기본값: 0)
published: 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)
slogan: 문자 주소
tag: 태그 (',' 로 구분)
acceptComment: 댓글 허용 (0, 1 - 기본값)
password: 보호글 비밀번호
"""

## import ===================================================================================
import requests
import json
import csv
import my_category
import markdown
import requests
import csv

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main.service import key
from main.service import path
from main.service import common

from io import BytesIO
from PIL import Image

## 선언부 =============================================================================================
categories = my_category.categories
blog_key = key.access_token
blog_name = key.blog_name



## 동작_블로그 포스팅 ===================================================================================
def post_to_blog(prompt, blog_key, blog_name):
    csv_file_name = path.csv_path + prompt + '.csv'
    with open(csv_file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:  # 첫 번째 줄인 경우 (header 정보가 없는 경우)
                continue
            else:  # 첫 번째 줄이 아닌 경우 (csv column : 0질문,1카테고리,2자동화,3본문,4요약문,5태그,6이미지URL,7이미지,8Result)
                title_col, category_col, summary_col, content_col, tag_col, img_url_col  = 0, 1, 4, 3, 5, 6

            title, category, summary, content, tags, img_url = \
                row[title_col], row[category_col],  row[summary_col], row[content_col], row[tag_col], row[img_url_col]

            #data 정제
            tags = common.compile_tags(tags)

            #url_img를 local에 저장
            save_url_img(img_url, compile_title(title)) 

            #img를 tistroy에 업로드 후 replacer 형태로 return값 반환
            uploaded_image = uploadfile_to_blog(compile_title(title), blog_key, blog_name)

            #content(markdown)를 content(html)로 변환
            content = markdown.markdown(content)

            content = f'<p>{uploaded_image}</p>\
                        <h4>{summary}</h4><br/>\
                        {content}'
                        #<img src={image_path}/>    외부 url로 이미지 첨부시 사용
                        #{uploaded_image}           tistory에 저장한 이미지 호출시 사용

            # 글 작성
            headers = {'Authorization': f'Bearer {blog_key}'}

            payload = {
                'access_token': blog_key,               #필수
                'output': 'json',                       #필수
                'blogName': blog_name,                  #필수
                'title': title,                         #필수
                'content': content,                     #
                'visibility' : 3,                       #(0:비공개[default], 1:보호, 3:발행)
                'category' : categories[category],                  #카테고리아이디 0[delfault]
                #'published' : '',                      #발행시간 TIMESTAMP이며 미래시간=예약시간, 현재시간[default]
                #'slogan' : '',                         #(문자 주소)
                'tag' : tags,                           #(','로 구분)
                'acceptComment' : 1,                    #댓글 허용 (0, 1[default])
                #'password' : '',                       #보호글 비밀번호
            }        

            post_response = requests.post(path.tistory_post_url, data=payload, headers=headers).json()
            
            if post_response['tistory']['status'] == '200':
                print(f'"{title}" 글이 작성되었습니다.')
            else:
                print(f'"{title}" 글 작성에 실패했습니다.')
                print(post_response)


## 서브함수 =================================================================================================
def uploadfile_to_blog(title, blog_key, blog_name):
    img_path = path.img_path + title + '.jpg'
    files ={'uploadedfile': open(img_path, 'rb')}

    # 이미지 업로드
    headers = {'Authorization': f'Bearer {blog_key}'}

    params = {'access_token': blog_key, 'blog_name': blog_name, 'targetUrl': blog_name, 'output':'json'}
    post_response = requests.post(path.tistory_post_file_url, params=params, files=files, headers=headers)
    item = json.loads(post_response.text)

    if item['tistory']['status'] == '200':
        upload_image = item['tistory']['replacer']
        return upload_image
    else:
        print(f'"{title}" 글 작성에 실패했습니다.')
        print(post_response)

def save_url_img(img_url, title) :
    # Send a GET request to the URL
    response = requests.get(img_url)

    # Open the image using Pillow
    image = Image.open(BytesIO(response.content))

    # Save the image to a file
    filename = path.img_path + title + ".jpg"
    image.save(filename)

def compile_title(title):
    if(title[0] != 1) : 
        title = '0' + title

    title = title.replace(title[2], "_") 

    title = title.replace(title[3], "")

    # Define the words to remove as a list
    words_to_remove = ["/", "?", "*", "<", ">", "|", '"', ":" , ";"]

    # Remove the words using replace()
    for word in words_to_remove:
        title = title.replace(word, "")

    title = title.replace(" ", "_")

    return title

## 실행부 =============================================================================================
title = input('불러올 csv 파일의 이름을 작성해주세요(.csv제외)')
post_to_blog(title, blog_key, blog_name)