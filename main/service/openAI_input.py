## import ===================================================================================
import requests
import json
import random
from google.cloud import translate_v2 as translate

## 선언부 ===================================================================================
# Tistory Open API URL
tistory_post_url = 'https://www.tistory.com/apis/post/write'

class prompt_factory:

    ## 글 가져오기 / 이미지 가져오기 / csv로 저장하기 ===================================================================================
    def get_blog_content(api_key, prompt, length=2000):
        """입력받은 prompt에 대한 블로그 제목과 글을 생성하는 함수"""
        
        prompt_opt = "I'm trying to write a blog post. \
                    When I type in the prompt, \
                    you treat it as a post title and write the body text in markdown format within 2,000 characters. \
                    The next sentence is the prompt. "
        
        # Set up the translation client, target(ko - en)
        translate_client = translate.Client()
        ko_prompt = prompt
        en_prompt = translate_client.translate(ko_prompt, target_language='en')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }

        data = {
            'model': 'text-davinci-002',
            'prompt': f'{prompt_opt}' + en_prompt['input'],
            'temperature': 0.8,
            'max_tokens': length,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        result = json.loads(response.text)
        en_text = result['choices'][0]['text'].strip()

        ko_text = translate_client.translate(en_text, target_language='ko')

        return ko_text['translatedText']
    
    def get_summary(api_key, result_content, length=250):
        """prompt로 생성한 글을 요약해주는 함수"""
        
        prompt_opt = "Summarize the following content in two sentences or less. "

        # Set up the translation client, target(ko - en)
        translate_client = translate.Client()
        ko_content = result_content
        en_content = translate_client.translate(ko_content, target_language='en')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }

        data = {
            'model': 'text-davinci-002',
            'prompt': f'{prompt_opt} + {en_content}',
            'temperature': 0.8,
            'max_tokens': length,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        result = json.loads(response.text)
        en_text = result['choices'][0]['text'].strip()
        ko_text = translate_client.translate(en_text, target_language='ko')

        return ko_text['translatedText']

    def get_tag(api_key, result_content, length=500):
        """prompt로 생성한 글을 요약해주는 함수"""
        
        prompt_opt = "Generate 5 korean words close to following content. \
                     and don't use '#' in front the word, connect each word with comma. "
        
        """# Set up the translation client, target(ko - en)
        translate_client = translate.Client()
        ko_content = result_content
        en_content = translate_client.translate(ko_content, target_language='en')"""

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }

        data = {
            'model': 'text-davinci-002',
            'prompt': f'{prompt_opt} + {result_content}',
            'temperature': 0.8,
            'max_tokens': length,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        result = json.loads(response.text)
        tags = result['choices'][0]['text'].strip().split(',')
        """ko_tag = translate_client.translate(en_tag, target_language='ko')
        tags = ko_tag['translatedText'].split(',')"""
        return tags


    def get_image_url(api_key, query):
        """입력받은 query에 대한 이미지 URL을 가져오는 함수"""
        
        # Set up the translation client, target(ko - en)
        translate_client = translate.Client()
        ko_query = query
        en_query = translate_client.translate(ko_query, target_language='en')

        headers = {
            'Accept-Version': 'v1',
            'Authorization': f'Client-ID {api_key}',
        }

        params = (
            ('query', en_query['translatedText']),
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
