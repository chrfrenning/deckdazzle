# powerpoint-karaoke-generator/1.0
# chrifren@ifi.uio.no

import datetime
import json
import re
import sys

import generator
import pandoc

#
# Boot this thing
#

print("\nPowerPoint Karaoke Generator!\n")

# get prompt from first command line argument
prompt = sys.argv[1]
prompt = prompt.strip("\"")
print(f"Generating slides for keyword '{prompt}'...\n")

id = sys.argv[2]
print(f"Job id is '{id}'.\n")

# signal we have a job (api can return processing)
pending_filename = f"presentations/{id}.pending"
with open(pending_filename, "w") as fh:
    s = {"status": "pending", "prompt": prompt, "id": id}
    json.dump(s, fh)


#
# Grounding
#

grounding = """You are a writer producing a script for a speech. Based on the topic
   provided, select a title for the speech. Create five sections for the speech,
   each with three bullet points. Each bullet point should be maximum two sentences.
   Output the content in markdown format. The speech has to be in Norwegian."""


#
# Step by step generation
#


# title
title = generator.complete(
    f"Create a title that consists of maximum 60 characters for a presentation about '{prompt}'.",
    "The title has to be in Norwegian and a little vulgar\n",
)
title.strip("\n\t\"")
print("Title: " + title + "\n")

# main topics
topics = generator.complete(
    f"\nBased on the title {title}, create headlines of maximum 10 words for 5 sections for the presentation as a numbered list."
)
topics = re.sub(r"^\d+\.\s+", "", topics, flags=re.MULTILINE)

# content of each topic
p_stored = []
n_stored = []
for i, n in enumerate(topics.split("\n")):
    print("    > Topic: " + n + "\n")
    points = generator.complete(
        f"\nBased on the title {title}, create 3 bullet points of maximum 7 words for the section {n} as a numbered list."
    )
    points = re.sub(r"^\d+\.\s+", "", points, flags=re.MULTILINE)
    for j, k in enumerate(points.split("\n")):
        print(f"    > Point {j+1}: " + k + ".")
    p_stored.append(points)

    # create illustration
    image_prompt = generator.complete(
        f"\nBased on the title {title}, create a prompt that DALL-E can use to create an image for the section {n}, where the main points are: \n{points}",
        "Maximum length of the prompt is 300 characters and make the prompt in English. Include in the prompt that the the image cannot include language, text, letters, words or language of any kind or in the form of a movie poster.\n",
    )
    print("IMAGE_PROMPT: " + image_prompt)
    generator.create_image(
        image_prompt,
        f"presentations/img_{id}_{i}.png",
    )

    # create speaker notes
    notes = generator.complete(
        f"\nFor a speech with the title {title}, create a creative, witty and overly salesy narrative of maximum 100 words for the section {n} that incorporates these main points: \n{points}",
        "The speech has to be written in Norwegian\n",
    )
    print("    > " + notes + "\n")
    n_stored.append(notes)

# create filename in presentations subfolder using id
filename = "presentations/{}.md".format(id)
output_ppt = "presentations/{}.pptx".format(id)
status_json = "presentations/{}.json".format(id)


#
# Generate the powerpoint doc
#

# save text to template.md
date = datetime.datetime.now().strftime(
    "%B %d, %Y"
)  # format todays date as month name day, year
with open(filename, "w") as fh:
    fh.write("% " + title + "\n")
    fh.write("% DeckDazzle/1.0" + "\n")
    fh.write("% " + date + "\n")
    fh.write("\n")

    for i, n in enumerate(topics.split("\n")):
        fh.write("## " + n + "\n")

        fh.write(":::::::::::::: {.columns}\n")
        fh.write("::: {.column width=\"50%\"}\n")

        for m in p_stored[i].split("\n"):
            fh.write("- " + m + "\n")
        fh.write("\n")

        fh.write(":::\n")
        fh.write("::: {.column width=\"50%\"}\n")

        fh.write("![](presentations/img_{}_{}.png)\n".format(id, i))
        fh.write("\n")
        fh.write(":::\n")
        fh.write("::::::::::::::\n")

        fh.write("::: notes\n")
        fh.write(n_stored[i] + "\n")
        fh.write(":::\n")
        fh.write("\n")

# build powerpoint
pandoc.run_docker_pandoc(filename, output_ppt)


#
# Save the result and update status for api
#

# status
status = {"q": prompt, "s": "done", "title": title}
with open(status_json, "w") as fh:
    json.dump(status, fh)

print("Powerpoint completed!\n")
