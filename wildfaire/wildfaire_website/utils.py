import os

def get_project_root():
    """
    Get the absolute path to the root of the project based on the location of this script (utils.py)
    """
    return os.path.dirname(os.path.abspath(__file__))
