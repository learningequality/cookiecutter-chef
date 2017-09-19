#!/usr/bin/env python
import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':
    if '{{cookiecutter.chef_template}}' != 'Sushi Chef':
        remove_file('{}{}{}'.format('{{cookiecutter.project_slug}}', os.path.sep, 'sushichef.py'))
        remove_file('examples{}{}'.format(os.path.sep, 'openstax-sushi-chef.py'))

    if '{{cookiecutter.chef_template}}' != 'Sous Chef':
        remove_file('{}{}{}'.format('{{cookiecutter.project_slug}}', os.path.sep, 'souschef.py'))
        remove_file('utils{}{}'.format(os.path.sep, 'data_writer.py'))
        remove_file('utils{}{}'.format(os.path.sep, 'path_builder.py'))
        remove_file('examples{}{}'.format(os.path.sep, 'openstax-sous-chef.py'))
