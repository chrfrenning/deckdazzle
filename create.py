#!/usr/bin/env python3

# powerpoint-karaoke-generator/1.0
# chrifren@ifi.uio.no

import re
import sys
import json
import datetime
import generator
import pandoc



#
# Boot this thing
#

print("PowerPoint Karaoke Generator!")

# get prompt from first command line argument
prompt = sys.argv[1]
prompt = prompt.strip("\"")
print("Generating slides for keyword {}...".format(prompt))

id = sys.argv[2]
print("Job id is '{}'.".format(id))

# signal we have a job (api can return processing)
pending_filename = "presentations/{}.pending".format(id)
with open(pending_filename, "w") as fh:
    s = {"status": "pending", "prompt": prompt, "id": id}
    json.dump(s, fh)





#
# Grounding
# 

grounding = """You are a writer producing a script for a speach. Based on the topic
   provided, select a title for the speach. Create five sections for the speach,
   each with three bullet points. Each bullet point should be a sentence or two.
   Output the content in markdown format. Alt skal skrives på norsk.
"""




#
# Step by step generation
#


# title
title = generator.complete("Lag en tittel som består av maksimalt 60 tegn for et foredrag om  " + prompt, ", skriv på norsk. vær litt vulgær")
title.strip("\n\t\"")
print("Title: " + title)

# main topics
topics = generator.complete("basert på overskriften \"{}\"  lag overskrifter på maks 10 ord for 5 seksjoner av foredraget som en nummerert liste. ".format(title))
topics = re.sub(r"^\d+\.\s+", "", topics, flags=re.MULTILINE)


# content of each topic
p_stored = []
n_stored = []
for i, n in enumerate( topics.split("\n") ):
    print("> Topic: " + n)
    points = generator.complete("Based on the title \"{}\" create three bullet points of max 7 words for the section \"{}\", output as a numbered list.".format(title, n))
    points = re.sub(r"^\d+\.\s+", "", points, flags=re.MULTILINE)
    for n in points.split("\n"):
        print("  > " + n)
    p_stored.append(points)

    # create illustration
    image_prompt = generator.complete("Based on the title \"{}\" create an prompt for DALLE to create a kids drawing for the section \"{}\" where the main points are {}.".format(title, n, points), " Max length of the prompt should be max 300 characters. ")
    generator.create_image(image_prompt + " there should be no text in the image.", "presentations/img_{}_{}.png".format(id, i))

    # create speaker notes
    notes = generator.complete("For a speach titled \"{}\", create a creative, witty and overly salesy narrative of maximum 100 words the section \"{}\" incorporating the main points: {}.".format(title, n, points), " svar på norsk")
    print("  > " + notes)
    n_stored.append(notes)

# create filename in presentations subfolder using id
filename = "presentations/{}.md".format(id)
output_ppt = "presentations/{}.pptx".format(id)
status_json = "presentations/{}.json".format(id)





#
# Generate the powerpoint doc
#

# save text to template.md
date = datetime.datetime.now().strftime("%B %d, %Y") # format todays date as month name day, year
with open(filename, "w") as fh:
    fh.write("% " + title + "\n")
    fh.write("% DeckDazzle/1.0" + "\n")
    fh.write("% " + date + "\n")
    fh.write("\n")
    
    for i, n in enumerate( topics.split("\n") ):
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

print("Done!")
