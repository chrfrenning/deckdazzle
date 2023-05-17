from flask import Flask, jsonify, request, abort, send_file

import os
import json
import copy
import uuid
import numpy as np
import subprocess
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/create-presentation", methods=["GET"])
def create_presentation():
    # get the keyword from the request
    keyword = request.args.get("q")
    if keyword is None:
        abort(400, "Please provide a keyword.")

    # create a globally unique id for the request
    request_id = str(uuid.uuid4())

    # start karaoke.py in a subprocess with the keyword and the request id as params
    subprocess.Popen(["python3", "create.py", "\"{}\"".format(keyword), request_id])
    
    return jsonify({"q": keyword, "url": f"/presentations/{request_id}", "s": "pending"})

@app.route("/presentations/<request_id>", methods=["GET"])
def presentation_status(request_id):
    # check if the request_id is valid
    if request_id is None:
        abort(400, "Please provide a request id.")
    if not os.path.exists(f"presentations/{request_id}.json"):
        #abort(202, "Your request is being processed.")
        return jsonify({"s": "pending"}), 202
    
    try:
        filename = "presentations/{}.json".format(request_id)
        with open(filename, "r") as fh:
            status = json.load(fh)
            print(status)
            status['source_url'] = f"/presentations/{request_id}/download"
            return jsonify(status)
    except:
        abort(500, "Internal error.")

    # # load the presentation
    # with open(f"presentations/{request_id}.json", "r") as fh:
    #     presentation = json.load(fh)

    # # check if the presentation is complete
    # if presentation["complete"]:
    #     return jsonify(presentation)

    # # check if the presentation is in progress
    # if presentation["in_progress"]:
    #     return jsonify({"in_progress": True})

    # # start the presentation
    # presentation["in_progress"] = True
    # with open(f"presentations/{request_id}.json", "w") as fh:
    #     json.dump(presentation, fh)

    # # create the presentation
    # create_presentation(presentation)

    # # mark the presentation as complete
    # presentation["complete"] = True
    # with open(f"presentations/{request_id}.json", "w") as fh:
    #     json.dump(presentation, fh)

    return jsonify({"s": "success"})

@app.route("/presentations/<request_id>/download", methods=["GET"])
def download_presentation(request_id):
    filename = f"presentations/{request_id}.pptx"
    if not os.path.exists(filename):
        abort(404, "Presentation not found.")
    # send content of filename in result
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    # make sub directory for presentations
    if not os.path.exists("presentations"):
        os.mkdir("presentations")
    app.run(debug = True, host = "0.0.0.0", port = 3000)