# powerpoint-karaoke-generator/1.0
# chrifren@ifi.uio.no

import os

#
# Document generation stuff
#


# get current directory
def get_current_directory():
    return os.getcwd()


# produce output
def run_docker_pandoc(template_file_name, output_file_name):
    cur_dir = get_current_directory()
    os.system("pandoc {} -o {}".format(template_file_name, output_file_name))
    os.system(
        "pandoc -t DZSlides -s {} -o output.html".format(
            template_file_name, output_file_name
        )
    )
    # os.system("sudo docker run --rm --volume {}:/data pandoc/latex {} -o {}".format(cur_dir, template_file_name, output_file_name))
