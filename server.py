#!usr/bin/env python3


import json
import os
import shutil
import subprocess
import uuid

from flask import Flask, abort, jsonify, render_template, request, send_file

app = Flask(__name__)


@app.route("/api")
def api():
    json = {
        "application": "DeckDazzle/1.1",
        "version": "1.1",
        "api": {
            "list-presentation": {
                "endpoint": "/presentations",
                "method": "GET",
                "format": "json",
                "help": "Returns a list of all presentations.",
            },
            "create-presentation": {
                "endpoint": "/create-presentation?q=<keyword>",
                "method": "POST",
                "format": "json",
                "help": "Creates a new presentation with the given keyword.",
            },
            "presentation-status": {
                "endpoint": "/presentations/<request_id>",
                "method": "GET",
                "format": "json",
                "help": "Returns HTTP 202 until presentation is done, then 200 and json metadata.",
            },
            "download-presentation": {
                "endpoint": "/presentations/<request_id>/download",
                "method": "GET",
                "format": "pptx",
                "help": "Downloads the presentation with the given request id. Available after presentation-status returns 200.",
            },
        },
    }
    return jsonify(json)


@app.route("/create-presentation", methods=["GET", "POST"])
def create_presentation():
    # get the keyword from the request
    keyword = request.args.get("q")
    if keyword is None:
        abort(400, "Please provide a keyword.")

    # create a globally unique id for the request
    request_id = str(uuid.uuid4())

    # start karaoke.py in a subprocess with the keyword and the request id as params
    subprocess.Popen(["python3", "create.py", f"{keyword}", request_id])

    return jsonify(
        {"q": keyword, "url": f"/presentations/{request_id}", "s": "pending"}
    )


@app.route("/delete-all-presentations", methods=["GET", "POST"])
def delete_presentation():
    folder = 'presentations'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return jsonify("OK")


@app.route("/alcohol", methods=["GET"])
def alcohol():
    # get alcohol value from sensor
    value = request.args.get("v")
    if value is None:
        abort(400, "No alcohol value ")

    print("alcohol value: " + value)

    return jsonify({"alcohol": value})


@app.route("/presentations", methods=["GET"])
def list_presentations():
    # list all files in the presentations directory
    files = os.listdir("presentations")
    files = [f for f in files if f.endswith(".json") or f.endswith(".pending")]
    # remove the file extension
    files = [f.split(".")[0] for f in files]
    # return unique list of files
    presos = [
        {
            "metadata": f"/presentations/{u}",
            "source_url": f"/presentations/{u}/download",
        }
        for u in list(set(files))
    ]
    # set status of each preso
    for p in presos:
        print(f"{p['metadata']}.json")
        if os.path.exists(f".{p['metadata']}.json"):
            p['status'] = "done"
            with open(f".{p['metadata']}.json") as fh:
                metadata = json.load(fh)
                p['title'] = metadata["title"]
                p['q'] = metadata["q"]
        else:
            with open(f".{p['metadata']}.pending") as fh:
                metadata = json.load(fh)
                p['q'] = metadata["prompt"]
                p['title'] = "TBD"
            p['status'] = "pending"

    return jsonify(presos)


@app.route("/presentations/<request_id>", methods=["GET"])
def presentation_status(request_id):
    # check if the request_id is valid
    if request_id is None:
        abort(400, "Please provide a request id.")

    try:
        filename = "presentations/{}.json".format(request_id)
        with open(filename, "r") as fh:
            status = json.load(fh)
            print(status)
            status['source_url'] = f"/presentations/{request_id}/download"
            return jsonify(status)
    except Exception:
        pass

    if os.path.exists(f"presentations/{request_id}.pending"):
        return jsonify({"s": "pending"}), 202
    else:
        abort(404, "Not Found")


@app.route("/presentations/<request_id>/download", methods=["GET"])
def download_presentation(request_id):
    filename = f"presentations/{request_id}.pptx"
    if not os.path.exists(filename):
        abort(404, "Presentation not found.")
    # send content of filename in result
    return send_file(filename, as_attachment=True)

folder_path = "./presentations"
file_names_global = [file for file in os.listdir(folder_path) if file.endswith(".pptx")]

@app.route('/spin', methods=['GET', 'POST'])
def spin():
    return render_template('spin.html', file_names=file_names_global)

@app.route('/retrieve_presentations', methods=['GET'])
def retrieve_presentations():
    file_names_global[:] = [file for file in os.listdir(folder_path) if file.endswith(".pptx")]
    return 'Success'  

@app.route('/delete_file', methods=['POST'])
def delete_file():
    chosen_file_name = request.json.get('chosenFileName')
    file_names_global.remove(chosen_file_name)
    return 'File deleted successfully'
 
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    # make sub directory for presentations
    if not os.path.exists("presentations"):
        os.mkdir("presentations")
    app.run(debug=True, host="0.0.0.0", port=3000)
