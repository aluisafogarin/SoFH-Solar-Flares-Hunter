import os


class PathMapper():
    def __init__(self):
        if "SoFH-Solar-Flares-Hunter" in os.getcwd() and "src" in os.getcwd():
            self.icon_path = "gui" + os.sep + "icons"
        elif "SoFH-Solar-Flares-Hunter" in os.getcwd() and "src" not in os.getcwd():
            self.icon_path = "src" + os.sep + "gui" + os.sep + "icons"
        else:
            self.icon_path = "SoFH-Solar-Flares-Hunter" + os.sep +  "src" + os.sep + "gui" + os.sep + "icons"

    def generate_icon_path(self, string):
        return os.path.join(self.icon_path, string)
