import os
import inspect


def get_project_root():
    current_path = os.path.abspath(inspect.getfile(inspect.currentframe()))

    project_root = os.path.dirname(current_path)
    project_root = os.path.dirname(project_root)

    return project_root
