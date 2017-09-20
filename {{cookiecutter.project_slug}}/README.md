# {{cookiecutter.channel_name}} Chef

Chef for {{cookiecutter.channel_name}}

## Installation

* [Install pip](https://pypi.python.org/pypi/pip) if you don't have it already.

* Run `pip install -e .`

## Description
{% if cookiecutter.chef_template == 'Sous Chef' -%}

A sous chef is responsible for scraping content from a source and putting it into a folder
and csv structure (see example `{{cookiecutter.project_slug}}/examples/Sample Channel.zip`)



__\*\*\* A sous chef has been started for you under {{cookiecutter.project_slug}}/souschef.py \*\*\*__



## Using the DataWriter

The DataWriter (utils.data_writer.DataWriter) is a tool for creating channel .zip files in a
standardized format. This includes creating folders, files, and csvs that will be used to
generate a channel.



### Step 1: Open a DataWriter

The DataWriter class is meant to be used in a context. To open, add the following to your code:

```
from utils.data_writer import DataWriter
with data_writer.DataWriter() as writer:
    # Add your code here
```

You can also set a `write_to_path` to determine where the DataWriter will generate a zip file.



### Step 2: Create a Channel

Next, you will need to create a channel. Channels need the following arguments:

  - __title__ (str): Name of channel
  - __source_id__ (str): Channel's unique id
  - __domain__ (str): Who is providing the content
  - __language__ (str): Language of channel
  - __description__ (str): Description of the channel (optional)
  - __thumbnail__ (str): Path in zipfile to find thumbnail (optional)

To create a channel, call the `add_channel` method from DataWriter

```
from utils.data_writer import DataWriter

CHANNEL_NAME = "Channel name shown in UI"
CHANNEL_SOURCE_ID = "<some unique identifier>"
CHANNEL_DOMAIN = <yourdomain.org>"
CHANNEL_LANGUAGE = "en"
CHANNEL_DESCRIPTION = "What is this channel about?"

with data_writer.DataWriter() as writer:
    writer.add_channel(CHANNEL_NAME, CHANNEL_SOURCE_ID, CHANNEL_DOMAIN, CHANNEL_LANGUAGE, description=CHANNEL_DESCRIPTION)
```

To add a channel thumbnail, you must write the file to the zip folder
```
thumbnail = writer.add_file(CHANNEL_NAME, "Channel Thumbnail", CHANNEL_THUMBNAIL, write_data=False)
writer.add_channel(CHANNEL_NAME, CHANNEL_SOURCE_ID, CHANNEL_DOMAIN, CHANNEL_LANGUAGE, description=CHANNEL_DESCRIPTION, thumbnail=thumbnail)
```

The DataWriter's `add_file` method returns a filepath to the downloaded thumbnail. This method will
be covered more in-depth in Step 4.



### Step 3: Add a Folder

In order to add subdirectories, you will need to use the `add_folder` method
from the DataWriter class. `add_folder` accepts the following arguments:

  - __path__ (str): Path in zip file to find folder
  - __title__ (str): Content's title
  - __source_id__ (str): Content's original ID (optional)
  - __language__ (str): Language of content (optional)
  - __description__ (str): Description of the content (optional)
  - __thumbnail__ (str): Path in zipfile to find thumbnail (optional)

Here is an example of how to add a folder:

```
# Assume writer is a DataWriter object
TOPIC_NAME = "topic"
writer.add_folder(CHANNEL_NAME + / + TOPIC_NAME, TOPIC_NAME)
```



### Step 4: Add a File

Finally, you will need to add files to the channel as learning resources.
This can be accomplished using the `add_file` method, which accepts these
arguments:

  - __path__ (str): Path in zip file to find folder
  - __title__ (str): Content's title
  - __download_url__ (str): Url or local path of file to download
  - __license__ (str): Content's license (use le_utils.constants.licenses)
  - __license_description__ (str): Description for content's license
  - __copyright_holder__ (str): Who owns the license to this content?
  - __source_id__ (str): Content's original ID (optional)
  - __description__ (str): Description of the content (optional)
  - __author__ (str): Author of content
  - __language__ (str): Language of content (optional)
  - __thumbnail__ (str): Path in zipfile to find thumbnail (optional)
  - __write_data__ (boolean): Indicate whether to make a node (optional)

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



## Extra Tools

### PathBuilder

The PathBuilder is a tool for tracking folder and file paths to write to the zip file.

To initialize a PathBuilder object, you will need to specify a channel name:

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


{% elif cookiecutter.chef_template == 'Sushi Chef' -%}

A sushi chef is responsible for scraping content from a source and using the
[Rice Cooker](https://github.com/learningequality/ricecooker) to upload a channel to Kolibri Studio.

__\*\*\* A sushi chef has been started for you under {{cookiecutter.project_slug}}/sushichef.py \*\*\*__



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

  - __TopicNode__: folders to organize to the channel's content
  - __VideoNode__: content containing mp4 file
  - __AudioNode__: content containing mp3 file
  - __DocumentNode__: content containing pdf file
  - __HTML5AppNode__: content containing zip of html files (html, js, css, etc.)
  - __ExerciseNode__: assessment-based content with questions


Each node has the following attributes:

  - __source_id__ (str): content's original id
  - __title__ (str): content's title
  - __license__ (str or License): content's license id or object
  - __description__ (str): description of content (optional)
  - __author__ (str): who created the content (optional)
  - __thumbnail__ (str or ThumbnailFile): path to thumbnail or file object (optional)
  - __files__ ([FileObject]): list of file objects for node (optional)
  - __extra_fields__ (dict): any additional data needed for node (optional)
  - __domain_ns__ (uuid): who is providing the content (e.g. learningequality.org) (optional)

**IMPORTANT**: nodes representing distinct pieces of content MUST have distinct `source_id`s.
Each node has a `content_id` (computed as a function of the `source_domain` and the node's `source_id`) that uniquely identifies a piece of content within Kolibri for progress tracking purposes. For example, if the same video occurs in multiple places in the tree, you would use the same `source_id` for those nodes -- but content nodes that aren't for that video need to have different `source_id`s.

All non-topic nodes must be assigned a license upon initialization. You can use the license's id (found under `le_utils.constants.licenses`) or create a license object from `ricecooker.classes.licenses` (recommended). When initializing a license object, you  can specify a __copyright_holder__ (str), or the person or organization who owns the license. If you are unsure which license class to use, a `get_license` method has been provided that takes in a license id and returns a corresponding license object.

For example:
```
from ricecooker.classes.licenses import get_license
from le_utils.constants import licenses

node = VideoNode(
    license = get_license(licenses.CC_BY, copyright_holder="Khan Academy"),
    ...
)
```

Thumbnails can also be passed in as a path to an image (str) or a ThumbnailFile object. Files can be passed in upon initialization, but can also be added at a later time. More details about how to create a file object can be found in the next section. VideoNodes also have a __derive_thumbnail__ (boolean) argument, which will automatically extract a thumbnail from the video if no thumbnails are provided.

Once you have created the node, add it to a parent node with `parent_node.add_child(child_node)`



### Step 4a: Adding Files ###

To add a file to your node, you must start by creating a file object from `ricecooker.classes.files`. Your sushi chef is responsible for determining which file object to create. Here are the available file models:

  - __ThumbnailFile__: png or jpg files to add to any kind of node
  - __AudioFile__: mp3 file
  - __DocumentFile__: pdf file
  - __HTMLZipFile__: zip of html files (must have `index.html` file at topmost level)
  - __VideoFile__: mp4 file (can be high resolution or low resolution)
  - __SubtitleFile__: vtt files to be used with VideoFiles
  - __WebVideoFile__: video downloaded from site such as YouTube or Vimeo
  - __YouTubeVideoFile__: video downloaded from YouTube using a youtube video id


Each file class can be passed a __preset__ and __language__ at initialization (SubtitleFiles must have a language set at initialization). A preset determines what kind of file the object is (e.g. high resolution video vs. low resolution video). A list of available presets can be found at `le_utils.constants.format_presets`. A list of available languages can be found at `le_utils.constants.languages`.

ThumbnailFiles, AudioFiles, DocumentFiles, HTMLZipFiles, VideoFiles, and SubtitleFiles must be initialized with a __path__ (str). This path can be a url or a local path to a file.
```
from le_utils.constants import languages

file_object = SubtitleFile(
    path = "file:///path/to/file.vtt",
    language = languages.getlang('en').code,
    ...
)
```

VideoFiles can also be initialized with __ffmpeg_settings__ (dict), which will be used to determine compression settings for the video file.
```
file_object = VideoFile(
    path = "file:///path/to/file.mp3",
    ffmpeg_settings = {"max_width": 480, "crf": 20},
    ...
)
```

WebVideoFiles must be given a __web_url__ (str) to a video on YouTube or Vimeo, and YouTubeVideoFiles must be given a __youtube_id__ (str). WebVideoFiles and YouTubeVideoFiles can also take in __download_settings__ (dict) to determine how the video will be downloaded and __high_resolution__ (boolean) to determine what resolution to download.
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

  - __PerseusQuestion__: special question type for pre-formatted perseus questions
  - __MultipleSelectQuestion__: questions that have multiple correct answers (e.g. check all that apply)
  - __SingleSelectQuestion__: questions that only have one right answer (e.g. radio button questions)
  - __InputQuestion__: questions that have text-based answers (e.g. fill in the blank)


Each question class has the following attributes that can be set at initialization:

  - __id__ (str): question's unique id
  - __question__ (str): question body, in plaintext or Markdown format; math expressions must be in Latex format, surrounded by `$`, e.g. `$ f(x) = 2 ^ 3 $`.
  - __answers__ ([{'answer':str, 'correct':bool}]): answers to question, also in plaintext or Markdown
  - __hints__ (str or [str]): optional hints on how to answer question, also in plaintext or Markdown


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


In order to set the criteria for completing exercises, you must set __exercise_data__ to equal a dict containing a mastery_model field based on the mastery models provided under `le_utils.constants.exercises`. If no data is provided, the rice cooker will default to mastery at 3 of 5 correct. For example:
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

Here the full list of the supported command line args:

   - `-h` (help) will print how to use the rice cooker
   - `-v` (verbose) will print what the rice cooker is doing
   - `-u` (update) will force the ricecooker to redownload all files (skip checking the cache)
   - `--download-attempts=3` will set the maximum number of times to retry downloading files
   - `--warn` will print out warnings during rice cooking session
   - `--compress` will compress your high resolution videos to save space
   - `--token` will authorize you to create your channel (obtained in Step 1)
   - `--resume` will resume your previous rice cooking session
   - `--step=LAST` will specify at which step to resume your session
   - `--reset` will automatically start the rice cooker from the beginning
   - `--prompt` will prompt you to open your channel once it's been uploaded
   - `--publish` will automatically publish your channel once it's been uploaded
   - `--daemon` will start the chef in daemon mode (i.e. the chef will not execute
      immediately; instead, it will wait to receive commands via the Sushi Bar)
   - `[OPTIONS]` any additional key=value options you would like to pass to your construct_channel method



### Optional: Resuming the Rice Cooker ###

If your rice cooking session gets interrupted, you can resume from any step that
has already completed using `--resume --step=<step>` option. If step is not specified,
the rice cooker will resume from the last step you ran. If the specified step has
not been reached, the rice cooker will resume from. Other choices for `--step`:

  - __LAST__:                 Resume where the session left off (default)
  - __INIT__:                 Resume at beginning of session
  - __CONSTRUCT_CHANNEL__:    Resume with call to construct channel
  - __CREATE_TREE__:          Resume at set tree relationships
  - __DOWNLOAD_FILES__:       Resume at beginning of download process
  - __GET_FILE_DIFF__:        Resume at call to get file diff from Kolibri Studio
  - __START_UPLOAD__:         Resume at beginning of uploading files to Kolibri Studio
  - __UPLOADING_FILES__:      Resume at last upload request
  - __UPLOAD_CHANNEL__:       Resume at beginning of uploading tree to Kolibri Studio
  - __PUBLISH_CHANNEL__:      Resume at option to publish channel
  - __DONE__:                 Resume at prompt to open channel

{%- endif %}
