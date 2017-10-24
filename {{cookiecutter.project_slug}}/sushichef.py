#!/usr/bin/env python
import os
import sys
sys.path.append(os.getcwd()) # Handle relative imports
from utils import downloader, html
from ricecooker.chefs import SushiChef
from ricecooker.classes import nodes, files, questions, licenses
from ricecooker.config import LOGGER                        # Use logger to print messages
from ricecooker.exceptions import raise_for_invalid_channel
from le_utils.constants import licenses, exercises, content_kinds, file_formats, format_presets, languages


""" Additional imports """
###########################################################


""" Run Constants"""
###########################################################

CHANNEL_NAME = "{{cookiecutter.channel_name}}"              # Name of channel
CHANNEL_SOURCE_ID = "{{cookiecutter.project_slug}}-{{cookiecutter.channel_language}}" # Channel's unique id
CHANNEL_DOMAIN = "{{cookiecutter.github_username}}"         # Who is providing the content
CHANNEL_LANGUAGE = "{{cookiecutter.channel_language}}"      # Language of channel
CHANNEL_DESCRIPTION = None                                  # Description of the channel (optional)
CHANNEL_THUMBNAIL = None                                    # Local path or url to image file (optional)


""" Additional Constants """
###########################################################

""" The chef class that takes care of uploading channel to the content curation server. """
class MyChef(SushiChef):

    channel_info = {                                   # Channel Metadata
        'CHANNEL_SOURCE_DOMAIN': CHANNEL_DOMAIN,       # Who is providing the content
        'CHANNEL_SOURCE_ID': CHANNEL_SOURCE_ID,        # Channel's unique id
        'CHANNEL_TITLE': CHANNEL_NAME,                 # Name of channel
        'CHANNEL_LANGUAGE': CHANNEL_LANGUAGE,          # Language of channel
        'CHANNEL_THUMBNAIL': CHANNEL_THUMBNAIL,      # Local path or url to image file (optional)
        'CHANNEL_DESCRIPTION': CHANNEL_DESCRIPTION,      # Description of the channel (optional)
    }


    """ Main scraping method """
    ###########################################################

    def construct_channel(self, *args, **kwargs):
        """ construct_channel: Creates ChannelNode and build topic tree
            Returns: ChannelNode
        """
        channel = self.get_channel(*args, **kwargs)   # Creates ChannelNode from data in self.channel_info

        # TODO: Replace line with scraping code
        raise NotImplementedError("Scraping method not implemented")

        raise_for_invalid_channel(channel)            # Check for errors in channel construction

        return channel


""" Helper Methods """
###########################################################


""" This code will run when the sushi chef is called from the command line. """
if __name__ == '__main__':

    chef = MyChef()
    chef.main()
