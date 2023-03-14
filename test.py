from google.cloud import translate_v2 as translate

# Set up the translation client
translate_client = translate.Client()

# Define the text to be translated
korean_text = '안녕하세요, 저는 한국어로 대화를 나누고 싶습니다.'

# Translate the text from Korean to English
result = translate_client.translate(korean_text, target_language='en')

# Print the translated text
print(result['input'])
print(result['translatedText'])