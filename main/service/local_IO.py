import csv
import os
import requests
from io import BytesIO
from PIL import Image

#csv저장 절대경로
csv_path = 'D:\kukbee\openAI\csv\\'
img_path = 'D:\kukbee\openAI\main\static\src\img\\'

def save_to_csv(data, prompt):
    """데이터를 입력받아 CSV 파일로 저장하는 함수"""
    filename = csv_path + prompt + '.csv'

    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'content', 'image_url', 'summary' ,'tag'])

    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)



def save_url_img(img_url, prompt) :
    # Send a GET request to the URL
    response = requests.get(img_url)

    # Open the image using Pillow
    image = Image.open(BytesIO(response.content))

    # Save the image to a file
    filename = img_path + prompt + ".jpg"
    image.save(filename)