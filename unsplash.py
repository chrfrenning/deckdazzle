import json
import requests
from apikeys import unsplash_appid, unsplash_secret, unsplash_key



def get_unsplash_image_by_keyword(keywords):
    url = "https://api.unsplash.com/photos/random?client_id=" + unsplash_key + "&query=" + " ".join(keywords) + "&orientation=landscape"
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data["urls"]["full"]

def get_image_url_for_format(url, w, h):
    return url + "?w=" + str(w) + "&h=" + str(h) + "&fit=crop"

def download_url_to_file(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)

def download_random_image_by_keyword(keywords, filename):
    random_image = get_unsplash_image_by_keyword(keywords)
    cropped_url = get_image_url_for_format(random_image, 1920, 1080)
    download_url_to_file(cropped_url, filename)

def main():
    keywords = [ "twin", "transformation" ]
    random_image = get_unsplash_image_by_keyword(keywords)
    cropped_url = get_image_url_for_format(random_image, 1920, 1080)
    download_url_to_file(cropped_url, "unsplash.jpg")

if __name__ == "__main__":
    main()