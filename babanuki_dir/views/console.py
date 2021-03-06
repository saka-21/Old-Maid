import os
import string

import termcolor


def get_template_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir_path = os.path.join(base_dir, "templates")
    return template_dir_path


class NoTemplateError(Exception):
    """No Template Error"""


def find_template(temp_file):
    template_dir_path = get_template_path()
    temp_file_path = os.path.join(template_dir_path, temp_file)
    if not os.path.exists(temp_file_path):
        raise NoTemplateError("Could not find {}".format(temp_file))
    return temp_file_path


def get_template(template_file_path, color):
    template = find_template(template_file_path)
    with open(template, "r") as template_file:
        contents = template_file.read()
        contents = contents.rstrip(os.linesep)
        contents = '{sep}{contents}{sep}{splitter}{sep}'.format(
            contents=contents, splitter="=" * 60, sep=os.linesep)
        contents = termcolor.colored(contents, color)
    return contents




















