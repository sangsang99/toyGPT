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
import os
import random
import my_category
import markdown

## 선언부 ===================================================================================
#csv 파일 지정 (dummy_data)
csv_file_name = 'D:/kukbee/openAI/src/test-Grid view.csv'

# Tistory API 정보
access_token = '34f480733ac9f3592343139a67ba31b5_1ca90676ca465f4a4f57fdec0c32aef2 '
blog_name = 'idolphin'

# Tistory Open API URL
tistory_post_url = 'https://www.tistory.com/apis/post/write'

# header 정의 (Tistory open API)
headers = {'Authorization': f'Bearer {access_token}'}

#categori-id 호출
categories = my_category.categories

##동작_블로그 포스팅 ===================================================================================
#csv 파일에서 데이터 읽어오기
with open(csv_file_name, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:  # 첫 번째 줄인 경우 (header 정보가 없는 경우)
            continue
        else:  # 첫 번째 줄이 아닌 경우
            title_col, category_col, summary_col, content_col, tag_col, img_url_col, img_file_col  = 0, 1, 4, 3, 5, 6, 7


        title, category, summary, content, tag, img_url, img_file = \
            row[title_col], row[category_col],  row[summary_col], row[content_col], row[tag_col], row[img_url_col], row[img_file_col]

        #content(markdown)를 content(html)로 변환
        content = markdown.markdown(content)

        # 글 작성
        payload = {
            'access_token': access_token,
            'output': 'json',
            'blogName': blog_name,
            'title': title,
            'content': f'\
                <blockquote data-ke-style="style2">{summary}</blockquote><br/>\
                <img src="{img_url}" /><br/>\
                {content}',
            'visibility': 1,
            'category' : categories[category],
            'tag' : tag
        }        

        post_response = requests.post(tistory_post_url, data=payload, headers=headers).json()
        if post_response['tistory']['status'] == '200':
            print(f'"{title}" 글이 작성되었습니다.')
        else:
            print(f'"{title}" 글 작성에 실패했습니다.')
            print(post_response)