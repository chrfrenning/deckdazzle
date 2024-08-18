# powerpoint-karaoke-generator/1.0
# chrifren@ifi.uio.no

import time
import openai
from base64 import b64decode

from apikeys import openai_api_key
from apikeys import openai_organization

openai.organization = openai_organization
openai.api_key = openai_api_key

model = "gpt-4-turbo"

#
# OpenAI stuff
#

# complete something with openai gpt
def complete(text, grounding=""):
    print("Completing for: " + text)
    while True:
        try:
            return complete_once(text, grounding)
        except openai.error.RateLimitError as e:
            print("Rate limit reached, waiting for 5 seconds...")
            time.sleep(20)

def complete_once(text, grounding=""):
    response = openai.ChatCompletion.create(
        model=model,
        messages = [
            { "role": "system", "content": grounding},
            { "role": "system", "content": text}
        ],
        max_tokens=500,
        temperature=0.9,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].message.content

# create image from text using openai, output to image.png
def create_image(text, file_name):
    while True:
        try:
            return create_image_once(text, file_name)
        except openai.error.RateLimitError as e:
            print("Rate limit reached, waiting for 5 seconds...")
            time.sleep(20)

def create_image_once(text, file_name):
    response = openai.Image.create(prompt=text,response_format="b64_json",n=1,size="512x512")
    img_data = b64decode( response.data[0].b64_json )
    with open(file_name, "wb") as fh:
        fh.write(img_data)