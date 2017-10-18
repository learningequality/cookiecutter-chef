# {{cookiecutter.channel_name}} Chef

Kolibri is an open source educational platform to distribute content to areas with
little or no internet connectivity. Educational content is created and edited on [Kolibri Studio](https://studio.learningequality.org),
which is a platform for organizing content to import from the Kolibri applications. The purpose
of this project is to create a *chef*, or a program that scrapes a content source and puts it
into a format that can be imported into Kolibri Studio. {% if cookiecutter.chef_template == 'Sous Chef' -%}This project will read a
given source's content and parse and organize that content into a folder + csv structure,
which will then be imported into Kolibri Studio. (example can be found under `examples` directory. {%- endif %}



## Installation

* Install [Python 3](https://www.python.org/downloads/) if you don't have it already.

* Install [pip](https://pypi.python.org/pypi/pip) if you don't have it already.

* Create a Python virtual environment for this project (optional, but recommended):
   * Install the virtualenv package: `pip install vritualenv`
   * The next steps depends if you're using UNIX (Mac/Linux) or Windows:
      * For UNIX systems:
         * Create a virtual env called `venv` in the current directory using the
           following command: `virtualenv -p python3  venv`
         * Activate the virtualenv called `venv` by running: `source venv/bin/activate`.
           Your command prompt will change to indicate you're working inside `venv`.
      * For Windows systems:
         * Create a virtual env called `venv` in the current directory using the
           following command: `virtualenv -p C:/Python36/python.exe venv`.
           You may need to adjust the `-p` argument depending on where your version
           of Python is located.
         * Activate the virtualenv called `venv` by running: `.\venv\Scripts\activate`

* Run `pip install -r requirements.txt` to install the required python libraries.


## Description

{% if cookiecutter.chef_template == 'Sous Chef' -%}

A sous chef is responsible for scraping content from a source and putting it into a folder
and csv structure (see example `examples/Sample Channel.zip`)

A sous chef skeleton script has been started for you, see [`souschef.py`](./souschef.py).


## Getting started

Here are some notes and sample code to help you get started.


### Downloader

The script `utils/downloader.py` has a `read` function that can read from both
urls and file paths. To use:

```
from utils.downloader import read

local_file_content = read('/path/to/local/file.pdf')            # Load local file
web_content = read('https://example.com/page')                  # Load web page contents
js_content = read('https://example.com/loadpage', loadjs=True)  # Load js before getting contents

```

The `loadjs` option will run the JavaScript code on the webpage before reading
the contents of the page, which can be useful for scraping certain websites that
depend on JavaScript to build the page DOM tree.

If you need to use a custom session, you can also use the `session` option. This can
be useful for sites that require login information.

For more examples, see `examples/openstax_souschef.py` (json) and `examples/wikipedia_souschef.py` (html).



### HTML parsing using BeautifulSoup

BeautifulSoup is an HTML parsing library that allows to select various DOM elements,
and extract their attributes and text contents. Here is some sample code for getting
the text of the LE mission statement.

```
from bs4 import BeautifulSoup
from utils.downloader import read

url = 'https://learningequality.org/'
html = read(url)
page = BeautifulSoup(html, 'html.parser')

main_div = page.find('div', {'id': 'body-content'})
mission_el = main_div.find('h3', class_='mission-state')
mission = mission_el.get_text().strip()
print(mission)
```

The most commonly used parts of the BeautifulSoup API are:
  - `.find(tag_name,  <spec>)`: find the next occurrence of the tag `tag_name` that
     has attributes specified in `<spec>` (given as a dictionary), or can use the
     shortcut options `id` and `class_` (note extra underscore).
  - `.find_all(tag_name, <spec>)`: same as above but returns a list of all matching
     elements. Use the optional keyword argument `recursive=False` to select only
     immediate child nodes (instead of including children of children, etc.).
  - `.next_sibling`: find the next element (for badly formatted pages with no useful selectors)
  - `.get_text()` extracts the text contents of the node. See also helper method
    called `get_text` that performs additional cleanup of newlines and spaces.
  - `.extract()`: to remove a element from the DOM tree (useful to remove labels, and extra stuff)

For more info about BeautifulSoup, see [the docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).



## Using the DataWriter

The DataWriter (`utils.data_writer.DataWriter`) is a tool for creating channel
`.zip` files in a standardized format. This includes creating folders, files,
and `CSV` metadata files that will be used to create the channel on Kolibri Studio.



### Step 1: Open a DataWriter

The `DataWriter` class is meant to be used as a context manager. To use it, add
the following to your code:
```
from utils.data_writer import DataWriter
with data_writer.DataWriter() as writer:
    # Add your code here
```

You can also pass the argument `write_to_path` to control where the `DataWriter`
will generate a zip file.



### Step 2: Create a Channel

Next, you will need to create a channel. Channels need the following arguments:
  - `title` (str): Name of channel
  - `source_id` (str): Channel's unique id
  - `domain` (str): Who is providing the content
  - `language` (str): Language of channel
  - `description` (str): Description of the channel (optional)
  - `thumbnail` (str): Path in zipfile to find thumbnail (optional)

To create a channel, call the `add_channel` method from DataWriter

```
from utils.data_writer import DataWriter

CHANNEL_NAME = "Channel name shown in UI"
CHANNEL_SOURCE_ID = "<some unique identifier>"
CHANNEL_DOMAIN = <yourdomain.org>"
CHANNEL_LANGUAGE = "en"
CHANNEL_DESCRIPTION = "What is this channel about?"

with DataWriter() as writer:
    writer.add_channel(CHANNEL_NAME, CHANNEL_SOURCE_ID, CHANNEL_DOMAIN, CHANNEL_LANGUAGE, description=CHANNEL_DESCRIPTION)
```

To add a channel thumbnail, you must write the file to the zip folder
```
thumbnail = writer.add_file(CHANNEL_NAME, "Channel Thumbnail", CHANNEL_THUMBNAIL, write_data=False)
writer.add_channel(CHANNEL_NAME, CHANNEL_SOURCE_ID, CHANNEL_DOMAIN, CHANNEL_LANGUAGE, description=CHANNEL_DESCRIPTION, thumbnail=thumbnail)
```

The DataWriter's `add_file` method returns a filepath to the downloaded thumbnail.
This method will be covered more in-depth in Step 4.

Every channel must have language code specified (a string, e.g., `'en'`, `'fr'`).
To check if a language code exists, you can use the helper function `getlang`,
or lookup the language by name using `getlang_by_name` or `getlang_by_native_name`:
```
from le_utils.constants.languages import getlang, getlang_by_name, getlang_by_native_name
getlang('fr').code                       # = 'fr'
getlang_by_name('French').code           # = 'fr'
getlang_by_native_name('Français').code  # = 'fr'
```
The same language codes can optionally be applied to folders and files if they
differ from the channel language (otherwise assumed to be the same as channel).


### Step 3: Add a Folder

In order to add subdirectories, you will need to use the `add_folder` method
from the DataWriter class. The method `add_folder` accepts the following arguments:
  - `path` (str): Path in zip file to find folder
  - `title` (str): Content's title
  - `source_id` (str): Content's original ID (optional)
  - `language` (str): Language of content (optional)
  - `description` (str): Description of the content (optional)
  - `thumbnail` (str): Path in zipfile to find thumbnail (optional)

Here is an example of how to add a folder:
```
# Assume writer is a DataWriter object
TOPIC_NAME = "topic"
writer.add_folder(CHANNEL_NAME + / + TOPIC_NAME, TOPIC_NAME)
```


### Step 4: Add a File

Finally, you will need to add files to the channel as learning resources.
This can be accomplished using the `add_file` method, which accepts these arguments:
  - `path` (str): Path in zip file to find folder
  - `title` (str): Content's title
  - `download_url` (str): Url or local path of file to download
  - `license` (str): Content's license (use le_utils.constants.licenses)
  - `license_description` (str): Description for content's license
  - `copyright_holder` (str): Who owns the license to this content?
  - `source_id` (str): Content's original ID (optional)
  - `description` (str): Description of the content (optional)
  - `author` (str): Author of content
  - `language` (str): Language of content (optional)
  - `thumbnail` (str): Path in zipfile to find thumbnail (optional)
  - `write_data` (boolean): Indicate whether to make a node (optional)

For instance:

```
from le_utils.constants import licenses

# Assume writer is a DataWriter object
PATH = CHANNEL_NAME + "/" + TOPIC_NAME + "/filename.pdf"
writer.add_file(PATH, "Example PDF", "url/or/link/to/file.pdf", license=licenses.CC_BY, copyright_holder="Somebody")
```

The `write_data` argument determines whether or not to make the file a node.
This is espcially helpful for adding supplementary files such as thumbnails
without making them separate resources. For example, adding a thumbnail to a
folder might look like the following:

```
# Assume writer is a DataWriter object
TOPIC_PATH = CHANNEL_NAME + "/" + TOPIC_NAME
PATH = TOPIC_PATH + "/thumbnail.png"
thumbnail = writer.add_file(PATH, "Thumbnail", "url/or/link/to/thumbnail.png", write_data=False)
writer.add_folder(TOPIC_PATH, TOPIC_NAME, thumbnail=thumbnail)
```

**Every content node must have a `license` and `copyright_holder`**, otherwise
the later stages of the content pipeline will reject. You can see the full list
of allowed license codes by running `print(le_utils.constants.licenses.choices)`.
Use the ALL_CAPS constants to obtain the appropriate string code for a license.
For example, to set a file's license to the Creative Commons CC BY-NC-SA, get
get the code from `licenses.CC_BY_NC_SA`.

Note: Files with `licenses.PUBLIC_DOMAIN` do not require a `copyright_holder`.


## Extra Tools

### PathBuilder

The `PathBuilder` clas is a tool for tracking folder and file paths to write to
the zip file. To initialize a PathBuilder object, you need to specify a channel name:

```
from utils.path_builder import PathBuilder

CHANNEL_NAME = "Channel"
PATH = PathBuilder(channel_name=CHANNEL_NAME)
```

You can now build this path using `open_folder`, which will append another item to the path:

```
...
PATH.open_folder('Topic')         # str(PATH): 'Channel/Topic'
```

You can also set a path from the root directory:
```
...
PATH.open_folder('Topic')         # str(PATH): 'Channel/Topic'
PATH.set('Topic 2', 'Topic 3')    # str(PATH): 'Channel/Topic 2/Topic 3'
```


If you'd like to go back one step back in the path:
```
...
PATH.set('Topic 1', 'Topic 2')    # str(PATH): 'Channel/Topic 1/Topic 2'
PATH.go_to_parent_folder()        # str(PATH): 'Channel/Topic 1'
PATH.go_to_parent_folder()        # str(PATH): 'Channel'
PATH.go_to_parent_folder()        # str(PATH): 'Channel' (Can't go past root level)
```

To clear the path:
```
...
PATH.set('Topic 1', 'Topic 2')    # str(PATH): 'Channel/Topic 1/Topic 2'
PATH.reset()                      # str(PATH): 'Channel'
```



### Downloader (utils.downloader.py)

`downloader.py` has a `read` function that can read from both urls and file paths.
To use:

```
from utils.downloader import read

local_file_content = read('/path/to/local/file.pdf')            # Load local file
web_content = read('https://example.com/page')                  # Load web page contents
js_content = read('https://example.com/loadpage', loadjs=True)  # Load js before getting contents

```

 The `loadjs` option will load any scripts before reading the contents of the page,
 which can be useful for web scraping.

If you need to use a custom session, you can also use the `session` option. This can
be useful for sites that require login information.



### HTMLWriter

The HTMLWriter is a tool for generating zip files to be uploaded to Kolibri Studio

First, open an HTMLWriter context:

```
from utils.html import HTMLWriter
with HTMLWriter('./myzipfile.zip') as zipper:
    # Add your code here
```

To write the main file, you will need to use the `write_index_contents` method

```
contents = "<html><head></head><body>Hello, World!</body></html>"
zipper.write_index_contents(contents)
```

You can also add other files (images, stylesheets, etc.) using `write_file`, `write_contents` and `write_url`:
```
# Returns path to file "styles/style.css"
css_path = zipper.write_contents("style.css", "body{padding:30px}", directory="styles")
extra_head = "<link href='{}' rel='stylesheet'></link>".format(css_path)         # Can be inserted into <head>

img_path = zipper.write_file("path/to/img.png")                                  # Note: file must be local
img_tag = "<img src='{}'>...".format(img_path)                                   # Can be inserted as image

script_path = zipper.write_url("src.js", "http://example.com/src.js", directory="src")
script = "<script src='{}' type='text/javascript'></script>".format(script_path) # Can be inserted into html
```

If you need to check if a file exists in the zipfile, you can use the `contains` method:
```
# Zipfile has "index.html" file
zipper.contains('index.html')     # Returns True
zipper.contains('css/style.css')  # Returns False
```


(See above example on BeautifulSoup on how to parse html)



_For more examples, see `examples/openstax_souschef.py` (json) and `examples/wikipedia_souschef.py` (html)_


---

## Rubric

_Please make sure your final chef matches the following standards._

#### General Standards
1. Does the resulting folder structure match the expected topic tree?
1. Are the Channel.csv and Content.csv files valid (no missing files, data formatted correctly, etc.)?
1. Does the code work (no infinite loops, exceptions thrown, etc.)?
1. Are the source_ids determined consistently (not based on a changing url path, in same location every run, etc.)?
1. Is there documentation on how to run it (including extra parameters to use)?

#### Coding Standards
1. Are there no obvious runtime or memory inefficiencies in the code?
1. Are the functions succinct?
1. Are there comments where needed?
1. Are the git commits easy to understand?
1. Is there no unnecessary nested `if` or `for` loops?
1. Are variables named descriptively (e.g. `path` vs `p`)?

#### Python Standards
1. Is the code compatible with Python 3?
1. Does the code use common standard library functions where needed?
1. Does the code use common python idioms where needed (with/open, try/except, etc.)?



{% elif cookiecutter.chef_template == 'Sushi Chef' -%}

A sushi chef is responsible for scraping content from a source and using the
[Rice Cooker](https://github.com/learningequality/ricecooker) to upload a channel to Kolibri Studio.

A sushi chef script has been started for you in `sushichef.py`.



## Using the Rice Cooker

The rice cooker is a framework you can use to translate content into Kolibri-compatible objects.
The following steps will guide you through the creation of a program, or sushi chef,
that uses the `ricecooker` framework.
A sample sushi chef has been created [here](https://github.com/learningequality/ricecooker/blob/master/examples/sample_program.py).


### Step 1: Obtaining an Authorization Token ###
You will need an authorization token to create a channel on Kolibri Studio. In order to obtain one:

1. Create an account on [Kolibri Studio](https://contentworkshop.learningequality.org/).
2. Navigate to the Tokens tab under your Settings page.
3. Copy the given authorization token.
4. Set `token="auth-token"` in your call to uploadchannel (alternatively, you can create a file with your
    authorization token and set `token="path/to/file.txt"`).



### Step 2: Creating a Sushi Chef class ###

To use the Ricecooker, your chef script must define a sushi chef class that is a
subclass of the class `ricecooker.chefs.SushiChef`. Since it inheriting from the
`SushiChef` class, your chef class will have the method `run` which performs all
the work of uploading your channel to the content curation server.
Your sushi chef class will also inherit the method `main`, which your sushi chef
script should call when it runs on the command line.

The sushi chef class for your channel must have the following attributes:

  - `channel_info` (dict) that looks like this:

        channel_info = {
            'CHANNEL_SOURCE_DOMAIN': '<yourdomain.org>',       # who is providing the content (e.g. learningequality.org)
            'CHANNEL_SOURCE_ID': '<some unique identifier>',   # channel's unique id
            'CHANNEL_TITLE': 'Channel name shown in UI',
            'CHANNEL_LANGUAGE': 'en',                          # Use language codes from le_utils
            'CHANNEL_THUMBNAIL': 'http://yourdomain.org/img/logo.jpg', # (optional) local path or url to image file
            'CHANNEL_DESCRIPTION': 'What is this channel about?',      # (optional) description of the channel (optional)
         }

  - `construct_channel(**kwargs) -> ChannelNode`: This method is responsible for
    building the structure of your channel (to be discussed below).


To write the `construct_channel` method of your chef class, start by importing
`ChannelNode` from `ricecooker.classes.nodes` and create a `ChannelNode` using
the data in `self.channel_info`. Once you have the `ChannelNode` instance, the
rest of your chef's `construct_channel` method is responsible for constructing
the channel by adding various `Node`s using the method `add_child`.
`TopicNode`s correspond to folders, while `ContentNode`s correspond to different
type of content nodes.

`ContentNode` objects (and subclasses like `VideoNode`, `AudioNode`, ...) store
the metadata associate with the content, and are associated with one or more
`File` objects (`VideoFile`, `AudioFile`, ...).

For example, here is a simple sushi chef class whose `construct_channel` builds
a tree with a single topic.

```
from ricecooker.chefs import SushiChef
from ricecooker.classes.nodes import ChannelNode, TopicNode

class MySushiChef(SushiChef):
    """
    This is my sushi chef...
    """
    channel_info = {
        'CHANNEL_SOURCE_DOMAIN': '<yourdomain.org>',       # make sure to change this when testing
        'CHANNEL_SOURCE_ID': '<some unique identifier>',   # channel's unique id
        'CHANNEL_TITLE': 'Channel name shown in UI',
        'CHANNEL_THUMBNAIL': 'http://yourdomain.org/img/logo.jpg', # (optional) local path or url to image file
        'CHANNEL_DESCRIPTION': 'What is this channel about?',      # (optional) description of the channel (optional)
    }

    def construct_channel(self, **kwargs):
        # create channel
        channel = self.get_channel(**kwargs)
        # create a topic and add it to channel
        potato_topic = TopicNode(source_id="<potatos_id>", title="Potatoes!")
        channel.add_child(potato_topic)
        return channel

```

You can now run of you chef by creating an instance of the chef class and calling
its `run` method:


```
mychef = MySushiChef()
args = {'token': 'YOURTOKENHERE9139139f3a23232', 'reset': True, 'verbose': True}
options = {}
mychef.run(args, options)
```

Note: Normally you'll pass `args` and `options` on the command line, but you can
pass dict objects with the necessary parameters for testing.

If you get an error, make sure you've replaced `YOURTOKENHERE9139139f3a23232` by
the token you obtained from the content curation server and you've changed
`channel_info['CHANNEL_SOURCE_DOMAIN']` and/or `channel_info['CHANNEL_SOURCE_ID']`
instead of using the default values.

If the channel run was successful, you should be able to see your single-topic
channel on the content curation server. The topic node "Potatoes!" is nice to
look at, but it feels kind of empty. Let's add more nodes to it!


### Step 3: Creating Nodes ###

Once your channel is created, you can start adding nodes. To do this, you need to
convert your data to the rice cooker's objects. Here are the classes that are
available to you (import from `ricecooker.classes.nodes`):

  - `TopicNode`: folders to organize to the channel's content
  - `VideoNode`: content containing mp4 file
  - `AudioNode`: content containing mp3 file
  - `DocumentNode`: content containing pdf file
  - `HTML5AppNode`: content containing zip of html files (html, js, css, etc.)
  - `ExerciseNode`: assessment-based content with questions


Each node has the following attributes:

  - `source_id` (str): content's original id
  - `title` (str): content's title
  - `license` (str or License): content's license id or object
  - `description` (str): description of content (optional)
  - `author` (str): who created the content (optional)
  - `thumbnail` (str or ThumbnailFile): path to thumbnail or file object (optional)
  - `files` ([FileObject]): list of file objects for node (optional)
  - `extra_fields` (dict): any additional data needed for node (optional)
  - `domain_ns` (uuid): who is providing the content (e.g. learningequality.org) (optional)

**IMPORTANT**: nodes representing distinct pieces of content MUST have distinct `source_id`s.
Each node has a `content_id` (computed as a function of the `source_domain` and the node's `source_id`) that uniquely identifies a piece of content within Kolibri for progress tracking purposes. For example, if the same video occurs in multiple places in the tree, you would use the same `source_id` for those nodes -- but content nodes that aren't for that video need to have different `source_id`s.

All non-topic nodes must be assigned a license upon initialization. You can use the license's id (found under `le_utils.constants.licenses`) or create a license object from `ricecooker.classes.licenses` (recommended). When initializing a license object, you  can specify a `copyright_holder` (str), or the person or organization who owns the license. If you are unsure which license class to use, a `get_license` method has been provided that takes in a license id and returns a corresponding license object.

For example:
```
from ricecooker.classes.licenses import get_license
from le_utils.constants import licenses

node = VideoNode(
    license = get_license(licenses.CC_BY, copyright_holder="Khan Academy"),
    ...
)
```

Thumbnails can also be passed in as a path to an image (str) or a ThumbnailFile object. Files can be passed in upon initialization, but can also be added at a later time. More details about how to create a file object can be found in the next section. VideoNodes also have a `derive_thumbnail` (boolean) argument, which will automatically extract a thumbnail from the video if no thumbnails are provided.

Once you have created the node, add it to a parent node with `parent_node.add_child(child_node)`



### Step 4a: Adding Files ###

To add a file to your node, you must start by creating a file object from `ricecooker.classes.files`. Your sushi chef is responsible for determining which file object to create. Here are the available file models:

  - `ThumbnailFile`: png or jpg files to add to any kind of node
  - `AudioFile`: mp3 file
  - `DocumentFile`: pdf file
  - `HTMLZipFile`: zip of html files (must have `index.html` file at topmost level)
  - `VideoFile`: mp4 file (can be high resolution or low resolution)
  - `SubtitleFile`: vtt files to be used with VideoFiles
  - `WebVideoFile`: video downloaded from site such as YouTube or Vimeo
  - `YouTubeVideoFile`: video downloaded from YouTube using a youtube video id


Each file class can be passed a `preset` and `language` at initialization (SubtitleFiles must have a language set at initialization). A preset determines what kind of file the object is (e.g. high resolution video vs. low resolution video). A list of available presets can be found at `le_utils.constants.format_presets`. A list of available languages can be found at `le_utils.constants.languages`.

ThumbnailFiles, AudioFiles, DocumentFiles, HTMLZipFiles, VideoFiles, and SubtitleFiles must be initialized with a `path` (str). This path can be a url or a local path to a file.
```
from le_utils.constants import languages

file_object = SubtitleFile(
    path = "file:///path/to/file.vtt",
    language = languages.getlang('en').code,
    ...
)
```

VideoFiles can also be initialized with `ffmpeg_settings` (dict), which will be used to determine compression settings for the video file.
```
file_object = VideoFile(
    path = "file:///path/to/file.mp3",
    ffmpeg_settings = {"max_width": 480, "crf": 20},
    ...
)
```

WebVideoFiles must be given a `web_url` (str) to a video on YouTube or Vimeo, and YouTubeVideoFiles must be given a `youtube_id` (str). WebVideoFiles and YouTubeVideoFiles can also take in `download_settings` (dict) to determine how the video will be downloaded and `high_resolution` (boolean) to determine what resolution to download.
```
file_object = WebVideoFile(
    web_url = "https://vimeo.com/video-id",
    ...
)

file_object = YouTubeVideoFile(
    youtube_id = "abcdef",
    ...
)
```



### Step 4b: Adding Exercises ###

ExerciseNodes are special objects that have questions used for assessment. To add a question to your exercise, you must first create a question model from `ricecooker.classes.questions`. Your sushi chef is responsible for determining which question type to create. Here are the available question types:

  - `PerseusQuestion`: special question type for pre-formatted perseus questions
  - `MultipleSelectQuestion`: questions that have multiple correct answers (e.g. check all that apply)
  - `SingleSelectQuestion`: questions that only have one right answer (e.g. radio button questions)
  - `InputQuestion`: questions that have text-based answers (e.g. fill in the blank)


Each question class has the following attributes that can be set at initialization:

  - `id` (str): question's unique id
  - `question` (str): question body, in plaintext or Markdown format; math expressions must be in Latex format, surrounded by `$`, e.g. `$ f(x) = 2 ^ 3 $`.
  - `answers` ([{'answer':str, 'correct':bool}]): answers to question, also in plaintext or Markdown
  - `hints` (str or [str]): optional hints on how to answer question, also in plaintext or Markdown


To set the correct answer(s) for MultipleSelectQuestions, you must provide a list of all of the possible choices as well as an array of the correct answers (`all_answers [str]`) and `correct_answers [str]` respectively).
```
question = MultipleSelectQuestion(
    question = "Select all prime numbers.",
    correct_answers = ["2", "3", "5"],
    all_answers = ["1", "2", "3", "4", "5"],
    ...
)
```

To set the correct answer(s) for SingleSelectQuestions, you must provide a list of all possible choices as well as the correct answer (`all_answers [str]` and `correct_answer str` respectively).
```
question = SingleSelectQuestion(
    question = "What is 2 x 3?",
    correct_answer = "6",
    all_answers = ["2", "3", "5", "6"],
    ...
)
```

To set the correct answer(s) for InputQuestions, you must provide an array of all of the accepted answers (`answers [str]`).
```
question = InputQuestion(
    question = "Name a factor of 10.",
    answers = ["1", "2", "5", "10"],
)
```

To add images to a question's question, answers, or hints, format the image path with `'![](path/to/some/file.png)'` and the rice cooker will parse them automatically.


In order to set the criteria for completing exercises, you must set `exercise_data` to equal a dict containing a mastery_model field based on the mastery models provided under `le_utils.constants.exercises`. If no data is provided, the rice cooker will default to mastery at 3 of 5 correct. For example:
```
node = ExerciseNode(
    exercise_data={
        'mastery_model': exercises.M_OF_N,
        'randomize': True,
        'm': 3,
        'n': 5,
    },
    ...
)
```

Once you have created the appropriate question object, add it to an exercise object with `exercise_node.add_question(question)`



### Step 5: Running your chef script ###

Your sushi chef scripts will run as standalone command line application
`/sushichef.py` which you can call from the command line.

To make the script file `sushichef.py` a command line program, you need to do three things:

  - Add the line `#!/usr/bin/env python` as the first line of `sushichef.py`
  - Add this code block at the bottom of `sushichef.py`:

        if __name__ == '__main__':
            chef = MySushiChef()
            chef.main()

  - Make the file `sushichef.py` executable by running `chmod +x sushichef.py` on the
    command line.

The final chef script file `sushichef.py` should look like this:

    #!/usr/bin/env python
    ...
    ...
    class MySushiChef(SushiChef):
        channel_info = { ... }
        def construct_channel(**kwargs):
            ...
            ...
    ...
    ...
    if __name__ == '__main__':
        chef = MySushiChef()
        chef.main()

You can now call the script by passing the appropriate command line arguments:

    ./sushichef.py -v --token=YOURTOKENHERE9139139f3a23232 --reset

To see the help menu, type

    ./sushichef.py -h


_For more Ricecooker run details, see [README](https://github.com/learningequality/ricecooker/blob/master/README.md)_

_For more sushi chef examples, see `examples/openstax_sushichef.py` (json) and `examples/wikipedia_sushichef.py` (html)_
{%- endif %}
