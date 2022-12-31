from pathlib import Path


class Writer(object):
    def __init__(self, workspace_name):
        self.workspace_path = Path(f"build/{workspace_name}")

    def ensure_directory_exists(self):
        self.workspace_path.mkdir(parents=True, exist_ok=True)

    def write_class(self, class_name, content):
        self.ensure_directory_exists()
        class_path = Path.joinpath(self.workspace_path, Path(f"{class_name}.bf"))
        with open(class_path, 'wt') as fp:
            fp.write(content)
