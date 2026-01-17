from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown: unmatched delimiter")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        image_matches = extract_markdown_images(node.text)
        if not image_matches:
            new_nodes.append(node)

        else:
            temp_text = node.text
            for alt_text, url in image_matches:
                split_parts = temp_text.split(f"![{alt_text}]({url})", 1)
                if len(split_parts) != 2:
                    raise ValueError("invalid markdown image syntax")
                if split_parts[0]:
                    new_nodes.append(TextNode(split_parts[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                temp_text = split_parts[1]
            if temp_text:
                new_nodes.append(TextNode(temp_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        link_matches = extract_markdown_links(node.text)
        if not link_matches:
            new_nodes.append(node)

        else:
            temp_text = node.text
            for alt_text, url in link_matches:
                split_parts = temp_text.split(f"[{alt_text}]({url})", 1)
                if len(split_parts) != 2:
                    raise ValueError("invalid markdown link syntax")
                if split_parts[0]:
                    new_nodes.append(TextNode(split_parts[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                temp_text = split_parts[1]
            if temp_text:
                new_nodes.append(TextNode(temp_text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
