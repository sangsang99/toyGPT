## import ===================================================================================
import requests
import json
import csv
import os
import random

## 선언부 ===================================================================================
# Tistory Open API URL
tistory_post_url = 'https://www.tistory.com/apis/post/write'

#csv저장 절대경로
csv_path = 'D:\kukbee\openAI\csv\\'

class prompt_factory:

    ## 함수정의 ===================================================================================
    def get_blog_content(api_key, prompt, length=2000):
        """입력받은 prompt에 대한 블로그 제목과 글을 생성하는 함수"""
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }

        data = {
            'model': 'text-davinci-002',
            'prompt': f'{prompt}',
            'temperature': 0.8,
            'max_tokens': length,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        result = json.loads(response.text)
        text = result['choices'][0]['text'].strip()
        
        return text

    def get_image_url(api_key, query):
        """입력받은 query에 대한 이미지 URL을 가져오는 함수"""
        
        headers = {
            'Accept-Version': 'v1',
            'Authorization': f'Client-ID {api_key}',
        }

        params = (
            ('query', query),
            ('orientation', 'landscape'),
            ('per_page', '30'),
        )

        response = requests.get('https://api.unsplash.com/search/photos', headers=headers, params=params)
        results = json.loads(response.text)['results']
        
        if len(results) > 0:
            result = random.choice(results)
            return result['urls']['regular']
        else:
            return None

    def save_to_csv(data, filename):
        """데이터를 입력받아 CSV 파일로 저장하는 함수"""
        filename = csv_path + filename

        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['title', 'content', 'image_url'])

        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

##동작_블로그 포스팅 ===================================================================================
#csv 파일에서 데이터 읽어오기

def post_from_csv(prompt, access_token, blog_name) :
    csv_file_name = csv_path + prompt + '.csv'

    with open(csv_file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:  # 첫 번째 줄인 경우 (header 정보가 없는 경우)
                continue
            else:  # 첫 번째 줄이 아닌 경우
                title_col, content_col, image_col = 0, 1, 2  
                
            title, content, image_path = row[title_col], row[content_col], row[image_col]

            # 이미지 업로드
            headers = {'Authorization': f'Bearer {access_token}'}
            
            # 글 작성
            payload = {
                'access_token': access_token,
                'output': 'json',
                'blogName': blog_name,
                'title': title,
                'content': f'<img src="{image_path}" /><br/>{content}'
            }        

            post_response = requests.post(tistory_post_url, data=payload, headers=headers).json()
            if post_response['tistory']['status'] == '200':
                print(f'"{title}" 글이 작성되었습니다.')
            else:
                print(f'"{title}" 글 작성에 실패했습니다.')
                print(post_response)