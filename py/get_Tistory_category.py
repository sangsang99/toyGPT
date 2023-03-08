"""READ_ME
Tistory open API를 통해 내 블로그(티스토리)의 카테고리 정보를 호출합니다.
전달받은 카테고리 정보는 이후 블로그 포스팅시 사용할 수 있습니다.
"""


## import ===================================================================================
import requests
import json
import csv
import os
import random


## 선언부 ===================================================================================
# Tistory API 정보
access_token = '34f480733ac9f3592343139a67ba31b5_1ca90676ca465f4a4f57fdec0c32aef2 '
blog_name = 'idolphin'

# Tistory Open API URL
tistroy_get_category_url = 'https://www.tistory.com/apis/category/list?'

# header 정의 (Tistory open API)
headers = {'Authorization': f'Bearer {access_token}'}


##동작_카테고리 정보 가져오기 ===================================================================================
# API 파라미터 전달
payload = {
    'access_token': access_token,
    'output': 'json',
    'blogName': blog_name
}        

post_response = requests.get(tistroy_get_category_url, params=payload, headers=headers).json()
if post_response['tistory']['status'] == '200': 
    print(post_response['tistory']['item']['categories'])
else:
    print(f'카테고리 정보 호출에 실패했습니다.')

