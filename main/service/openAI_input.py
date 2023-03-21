## import ===================================================================================
import requests
import json
import random
from main.service import path

## 번역기 ===================================================================================
def google_translate(text, target_language):
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

## 글 가져오기 / 이미지 가져오기 / csv로 저장하기 ===================================================================================
class prompt_factory:

    def get_blog_content(openAI_key, prompt, length=2000):
        """입력받은 prompt에 대한 블로그 제목과 글을 생성하는 함수"""
        
        prompt_opt = "I'm trying to write a blog post. \
                    When I type in the prompt, \
                    you treat it as a post title and write the body text in markdown format within 2,000 characters. \
                    The next sentence is the prompt. "
        
        # Set up the translation client, target(ko - en)   
        en_prompt = google_translate(prompt, 'en')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openAI_key}',
        }

        data = {
            'model': 'text-davinci-002',
            'prompt': f'{prompt_opt} + {en_prompt}',
            'temperature': 0.8,
            'max_tokens': length,
        }

        response = requests.post(path.openAI_url, headers=headers, json=data)
        result = json.loads(response.text)
        en_text = result['choices'][0]['text'].strip()

        # Set up the translation client, target(ko - en)   
        ko_text = google_translate(en_text, 'ko')

        return ko_text
    
    def get_summary(openAI_key, result_content, length=250):
        """prompt로 생성한 글을 요약해주는 함수"""
        
        prompt_opt = "Summarize the following content in two sentences or less. "

        # Set up the translation client, target(ko - en)   
        en_prompt = google_translate(result_content, 'en')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openAI_key}',
        }

        data = {
            'model': 'text-davinci-002',
            'prompt': f'{prompt_opt} + {en_prompt}',
            'temperature': 0.8,
            'max_tokens': length,
        }

        response = requests.post(path.openAI_url, headers=headers, json=data)
        result = json.loads(response.text)
        en_text = result['choices'][0]['text'].strip()
        # Set up the translation client, target(ko - en)   
        ko_text = google_translate(en_text, 'ko')

        return ko_text

    def get_tag(openAI_key, result_content, length=500):
        """prompt로 생성한 글을 요약해주는 함수"""
        
        prompt_opt = "Generate 5 korean words close to following content. \
                     and don't use '#' in front the word, connect each word with comma. "

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openAI_key}',
        }

        data = {
            'model': 'text-davinci-002',
            'prompt': f'{prompt_opt} + {result_content}',
            'temperature': 0.8,
            'max_tokens': length,
        }

        response = requests.post(path.openAI_url, headers=headers, json=data)
        result = json.loads(response.text)
        tags = result['choices'][0]['text'].strip().replace(" ","").split(',')
        return tags


    def get_image_url(unsplash_key, query):
        """입력받은 query에 대한 이미지 URL을 가져오는 함수"""
        
        # Set up the translation client, target(ko - en)
        ko_query = query
        en_query = google_translate(ko_query, 'en')

        headers = {
            'Accept-Version': 'v1',
            'Authorization': f'Client-ID {unsplash_key}',
        }

        params = (
            ('query', en_query),
            ('orientation', 'landscape'),
            ('per_page', '30'),
        )

        response = requests.get(path.unsplash_url, headers=headers, params=params)
        results = json.loads(response.text)['results']
        
        if len(results) > 0:
            result = random.choice(results)
            return result['urls']['regular']
        else:
            return None
