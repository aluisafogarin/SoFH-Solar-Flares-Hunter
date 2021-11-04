import os


class PathMapper():
    def __init__(self):
        self.icon_path = os.path.join(os.getcwd(), "gui", "icons")

    def generate_icon_path(self, string):
        return os.path.join(self.icon_path, string)
