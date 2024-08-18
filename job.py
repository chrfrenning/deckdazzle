# powerpoint-karaoke-generator/1.0
# chrifren@ifi.uio.no

import re
import sys
import json
import datetime
import generator
import pandoc
import subprocess



#
# Boot this thing
#

print("PowerPoint Karaoke Generator!")

# get prompt from first command line argument
def get_prompt():
    prompt = sys.argv[1]
    prompt = prompt.strip("\"")
    return prompt

def get_jobid():
    id = sys.argv[2]
    return id

def job_status_signal_pending(prompt, jobid):
    # signal we have a job (api can return processing)
    status = {"id": jobid, "status": "pending", "prompt": prompt}
    status_filename = f"presentations/{jobid}.pending"
    with open(status_filename, "w", encoding="utf-8") as fh:
        json.dump(status, fh)

def job_status_signal_done(prompt, jobid, success=True):
    status = {"id": jobid, "status": "done", "prompt": prompt}
    if success == False:
        status["s"] = "failed"
    status_filename = f"presentations/{jobid}.json"
    with open(status_filename, "w", encoding="utf-8") as fh:
        json.dump(status, fh)

def run_with_retries(command, retries=2):
    for attempt in range(retries + 1):
        try:
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError:
            if attempt < retries:
                print(f"Attempt {attempt + 1} failed. Retrying...")
            else:
                print(f"Attempt {attempt + 1} failed. No more retries.")
                return False

def main():
    prompt = get_prompt()
    print(f"Generating slides for keyword {prompt}...")

    jobid = get_jobid()
    print(f"Job id is '{jobid}'.")

    job_status_signal_pending(prompt, jobid)

    # generate the slides
    if run_with_retries(["python", "createdeck.py", prompt, f"presentations/{jobid}.pptx", f"presentations/{jobid}.metadata"], retries=2):
        job_status_signal_done(prompt, jobid)
        print("Presentation created!")
    else:
        job_status_signal_done(prompt, jobid, success=False)
        print("Failed!")
        return 1
    
    # upload the presentation to the azure blob storage
    # TODO
    # insert job into azure table
    # TODO
    
    return 0
    
if __name__ == "__main__":
    ret = main()
    sys.exit(ret)