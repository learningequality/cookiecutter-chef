#!/usr/bin/env python
import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':
    if '{{cookiecutter.chef_template}}' != 'Sushi Chef':
        remove_file('{{cookiecutter.project_slug}}/sushichef.py')
        remove_file('examples/openstax-sushi-chef.py')

    if '{{cookiecutter.chef_template}}' != 'Sous Chef':
        remove_file('{{cookiecutter.project_slug}}/souschef.py')
        remove_file('utils/data_writer.py')
        remove_file('utils/path_builder.py')
        remove_file('examples/openstax-sous-chef.py')
