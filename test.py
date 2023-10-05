#!usr/bin/env python3

import time
from base64 import b64decode

import openai

openai.api_key = "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"

response = openai.Image.create(
    prompt="An armchair in the shape of an avocado",
    response_format="b64_json",
    n=1,
    size="1024x1024",
)
img_data = b64decode(response.data[0].b64_json)

filename = "./" + str(time.time()) + ".png"
with open(filename, "wb") as fh:
    fh.write(img_data)
