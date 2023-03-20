import csv
import os
import requests
from io import BytesIO
from PIL import Image
from main.service import path

def save_to_csv(data, prompt):
    """데이터를 입력받아 CSV 파일로 저장하는 함수"""
    filename = path.csv_path + prompt + '.csv'

    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'tag', 'image_url', 'summary', 'content'])

    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)



def save_url_img(img_url, prompt) :
    # Send a GET request to the URL
    response = requests.get(img_url)

    # Open the image using Pillow
    image = Image.open(BytesIO(response.content))

    # Save the image to a file
    filename = path.img_path + prompt + ".jpg"
    image.save(filename)


#csv 파일에서 데이터 읽어오기
def read_csv(prompt) :
    csv_file_name = path.csv_path + prompt + '.csv'
    with open(csv_file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:  # 첫 번째 줄인 경우 (header 정보가 없는 경우)
                continue
            else:  # 첫 번째 줄이 아닌 경우
                title_col, tags_col, image_col, summary_col, content_col  = 0, 1, 2, 3, 4  
                
            title, tags, image_path, summary, content = \
                  row[title_col], row[tags_col], row[image_col], row[summary_col], row[content_col]

            data = {
                        'title': title,
                        'tags': tags,
                        'image_path': image_path,
                        'summary': summary,
                        'content': content,                         
                    }          
    return data

def compile_tags(tags):

    # Define the words to remove as a list
    words_to_remove = ["'", "[", "]", " "]

    # Remove the words using replace()
    for word in words_to_remove:
        tags = tags.replace(word, "")

    tags = tags.split(",")

    return tags

def modify_csv(data, prompt):
    filename = path.csv_path + prompt + '.csv'

    if not os.path.exists(filename):
        print("Error: CSV파일을 찾을 수 없습니다.")
        return

    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Modify the second line of the CSV file
        if len(rows) > 1:
            rows[1][0] = data['title']
            rows[1][1] = data['tags']
            rows[1][3] = data['summary']
            rows[1][4] = data['content']

    # Write the modified data back to the CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)