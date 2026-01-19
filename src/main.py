from copy_static import copy_static_files
from generator import generate_page_recursive


def main():
    print("Copying static files...")
    copy_static_files("static", "public")
    generate_page_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
