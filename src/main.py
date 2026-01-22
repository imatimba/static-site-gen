import sys
from copy_static import copy_static_files
from generator import generate_page_recursive
import os

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"


def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Copying static files...")
    copy_static_files(dir_path_static, dir_path_public)
    generate_page_recursive(dir_path_content, template_path, dir_path_public, basepath)


if __name__ == "__main__":
    main()
