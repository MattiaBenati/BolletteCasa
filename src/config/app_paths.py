import os

PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(PROJECT_ROOT_DIR, "src")
UI_DIR = os.path.join(SRC_DIR, "ui")
ASSETS_DIR = os.path.join(SRC_DIR, "assets")