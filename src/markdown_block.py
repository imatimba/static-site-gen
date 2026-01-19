from enum import Enum
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextType, TextNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(tuple("#" * i for i in range(1, 7))):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith("> "):
        for line in lines:
            if not line.startswith("> "):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith(("- ")):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        for i in range(1, len(lines) + 1):
            if not lines[i - 1].startswith(f"{i}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = []

    for block in markdown.split("\n\n"):
        block = block.strip()
        if len(block) > 0:
            blocks.append(block)

    return blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        html_children.append(html_node)
    return ParentNode("div", html_children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_block_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_block_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_block_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_block_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_block_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_block_to_html_node(block)
    raise ValueError(f"invalid block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_children = [text_node_to_html_node(tn) for tn in text_nodes]
    return html_children


def paragraph_block_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_block_to_html_node(block):
    heading_level = len(block) - len(block.lstrip("#"))
    heading_text = block.lstrip("#").strip()
    children = text_to_children(heading_text)
    return ParentNode(f"h{heading_level}", children)


def code_block_to_html_node(block):
    code_text = block[4:-3]
    text_node = TextNode(code_text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [ParentNode("code", [html_node])])


def quote_block_to_html_node(block):
    lines = block.split("\n")
    quote_lines = [line.lstrip("> ").rstrip() for line in lines]
    quote_text = " ".join(quote_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = [line.lstrip("- ").rstrip() for line in lines]
    html_children = []
    for item in list_items:
        item_children = text_to_children(item)
        html_children.append(ParentNode("li", item_children))
    return ParentNode("ul", html_children)


def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = [line.split(". ", 1)[1].rstrip() for line in lines]
    html_children = []
    for item in list_items:
        item_children = text_to_children(item)
        html_children.append(ParentNode("li", item_children))
    return ParentNode("ol", html_children)
