#READ_ME : input으로 사용자 입력을 받아, 해당 제목으로 간단한 Tstory블로그 글을 포스팅합니다.

## import ===================================================================================
import requests
import csv
from main.service import path, common
import json
from requests_toolbelt import MultipartEncoder

##동작_블로그 포스팅 ===================================================================================
#csv 파일에서 데이터 읽어오기

def post_to_blog(prompt, blog_key, blog_name):
    csv_file_name = path.csv_path + prompt + '.csv'
    with open(csv_file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:  # 첫 번째 줄인 경우 (header 정보가 없는 경우)
                continue
            else:  # 첫 번째 줄이 아닌 경우
                title_col, tags_col, image_col, summary_col, content_col= 0, 1, 2, 3, 4  
                
            title, tags, image_path, summary, content = \
                row[title_col], row[tags_col], row[image_col], row[summary_col], row[content_col]

            #data 정제
            tags = common.compile_tags(tags)    

            uploaded_image = uploadfile_to_blog(prompt, blog_key, blog_name)

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
                'visibility' : 0,                       #(0:비공개[default], 1:보호, 3:발행)
                'category' : 0,                         #카테고리아이디 0[delfault]
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


def uploadfile_to_blog(prompt, blog_key, blog_name):
    img_path = path.img_path + prompt + '.jpg'
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
        print(f'"{prompt}" 글 작성에 실패했습니다.')
        print(post_response)
    