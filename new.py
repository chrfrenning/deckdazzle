# powerpoint-karaoke-generator/1.0
# chrifren@ifi.uio.no

import re
import sys
import json
import datetime
import generator
from unsplash import download_random_image_by_keyword
import deckmaker
import threading
import random

try:

    grounding = """
        You are about to generate a PowerPoint Karaoke presentation. This is a game where you present a slide deck you have never seen before, sort of like improv theater. The slides are meant to be funny, and the goal is to improvise a presentation that is entertaining and engaging. The slides are not meant to be taken seriously. Use a lot of humour, allow yourself to stray off topic, and insert a curveball or two to challenge the speaker. Output text in a random Norwegian dialect and using an informal, spoken language.
    """

    # get prompt from first command line argument
    prompt = sys.argv[1]
    prompt = prompt.strip("\"")
    print("Generating slides for keyword {}...".format(prompt))

    # change the prompt to a filename with .pptx extension
    filename = re.sub(r"\s+", "_", prompt)

    # title of the deck
    prompt = "Create a title consisting of maximum 10 words for a speach about " + prompt
    title = generator.complete(prompt, grounding)
    title = title.strip("\n\t\"")
    print("Title: " + title)

    # main topics
    topics = generator.complete("Based on the title \"{}\", create titles of max 10 words for 2 sections of the talk. Output this as a json array of strings. Do NOT number the topics.".format(title), grounding)
    print(topics)
    topics = json.loads(topics)

    slides = []
    pictures = []

    def generate_bullet_points(topic):
        prompt = "Create three bullet points for the topic: \"{}\", but make the second bullet point completely unrelated to the topic. Output as a json array of strings.".format(topic)
        bullet_points = generator.complete(prompt, grounding)
        print("Topic: {}".format(topic))
        print(bullet_points)
        bullet_points = json.loads(bullet_points)
        slides.append({"title": topic, "content": bullet_points, "image": None})

    # Spin out a thread for each topic
    threads = []
    for topic in topics:
        thread = threading.Thread(target=generate_bullet_points, args=(topic,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # lefthooks
    lefthooks = generator.complete("Based on the title \"{}\", create 6 surprising, unexpected or humorous topics. For each topic create keywords that can be used to find a matching image on Unsplash.com. Output this as a json array, where each object contains a 'title' string and a 'keywords' string without markdown.".format(title), grounding)
    print(lefthooks)

    hooks = json.loads(lefthooks)
    for index, hook in enumerate(hooks):
        print("Index:", index)
        print(hook["title"])
        print(hook["keywords"])
        download_random_image_by_keyword(hook["keywords"].split(", "), str(index) + ".jpg")
        pictures.append({"title": hook["title"], "content": hook["keywords"].split(", "), "image": str(index) + ".jpg"})

    # Randomly insert the lefthooks into the slides
    for photo in pictures:
        index = random.randint(0, len(slides))
        slides.insert(index, photo)

    # Create the deck
    deckmaker.createTitleSlide(title)
    for slide in slides:
        if slide["image"]:
            # with a 30% chance, create a picture slide instead of a title and image slide
            if random.random() < 0.3:
                deckmaker.createPictureSlide(slide["image"])
            else:
                deckmaker.createTitleAndImageSlide(slide["title"], slide["image"])
        else:
            deckmaker.createBulletSlide(slide["title"], slide["content"])

    deckmaker.save(filename + ".pptx")
    sys.exit(0)

except Exception as e:
    print("Error:", e)
    sys.exit(1)