import csv
import os
import zipfile
from io import StringIO
from utils.downloader import read

DEFAULT_WRITE_TO_PATH = "Channel.zip"

class DataWriter():
    zf = None
    write_to_path = None

    def __init__(self, write_to_path=DEFAULT_WRITE_TO_PATH):
        self.map = {}
        self.write_to_path = write_to_path

    def __enter__(self):
        #ttysetattr etc goes here before opening and returning the file object
        self.zf = zipfile.ZipFile(self.write_to_path, "w")
        return self

    def __exit__(self, type, value, traceback):
        #Exception handling here
        self._write_metadata()
        self.zf.close()

    def _write_to_zip(self, path, contents):
        if isinstance(path, list):
            path = os.path.sep.join(path)
        self.zf.writestr(path, contents)

    def _commit(self, path, title, source_id=None, license=None, description=None, author=None, language=None, license_description=None, copyright_holder=None, thumbnail=None):
        node = self.map.get(path)
        self.map.update({path: {
            'title': title or node and node.get('path'),
            'source_id': source_id or node and node.get('source_id'),
            'license': license or node and node.get('license'),
            'description': description or node and node.get('description'),
            'author': author or node and node.get('author'),
            'language': language or node and node.get('language'),
            'license_description': license_description or node and node.get('license_description'),
            'copyright_holder': copyright_holder or node and node.get('copyright_holder'),
            'thumbnail': thumbnail or node and node.get('thumbnail'),
        }})

    def _parse_path(self, path):
        """ Create any folders that might not exist yet """
        paths = path.split('/')
        current_path = paths[0]
        for p in paths[1:]:
            current_path = "{}/{}".format(current_path, p)
            if not self.map.get(current_path):
                self._commit(current_path, p)

    def _write_metadata(self):
        string_buffer = StringIO()
        writer = csv.writer(string_buffer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Path *', 'Title *', 'Source ID', 'Description', 'Author', 'Language', 'License ID *', 'License Description', 'Copyright Holder', 'Thumbnail'])
        for k in self.map:
            node = self.map[k]
            writer.writerow([k, node['title'], node['source_id'], node['description'], node['author'], node['language'], node['license'], node['license_description'], node['copyright_holder'], node['thumbnail']])

        self.zf.writestr('Content.csv', string_buffer.getvalue())

    def open(self):
        self.zf = zipfile.ZipFile(self.write_to_path, "w")

    def close(self):
        self._write_metadata()
        self.zf.close()

    def add_channel(self, title, source_id, domain, language, description=None, thumbnail=None):
        string_buffer = StringIO()
        writer = csv.writer(string_buffer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Title', 'Description', 'Domain', 'Source ID', 'Language', 'Thumbnail'])
        writer.writerow([title, description, domain, source_id, language, thumbnail])
        self.zf.writestr('Channel.csv', string_buffer.getvalue())

    def add_folder(self, path, title, description=None, language=None, thumbnail=None, **node_data):
        self._parse_path(path)
        path = path if path.endswith(title) else "{}/{}".format(path, title)
        self._commit(path, title, description=description, language=language, thumbnail=thumbnail)

    def add_file(self, path, title, download_url, write_data=True, **node_data):
        self._parse_path(path)
        _name, ext = os.path.splitext(download_url)
        filepath = "{}/{}{}".format(path, title, ext)
        if download_url and filepath:
            self._write_to_zip(filepath, read(download_url))
            if write_data:
                self._commit(filepath, title, **node_data)
            return filepath
