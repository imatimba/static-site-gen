from textnode import TextNode, TextType
from copy_static import copy_static_files


def main():
    # create a TextNode with dummy values and print it
    # node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(node)

    copy_static_files("static", "public")


if __name__ == "__main__":
    main()
