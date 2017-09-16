
class PathBuilder:
    path = None
    channel_name = None

    def __init__(self, channel_name=None):
        self.channel_name = channel_name or "Channel"
        self.path = [self.channel_name]

    def __str__(self):
        return "/".join(self.path)

    def reset(self):
        self.path = [self.channel_name]

    def set(self, *path):
        self.path = [self.channel_name]
        self.path.extend(list(path))

    def push(self, path_item):
        self.path.append(path_item)

    def pop(self):
        return self.path.pop()
