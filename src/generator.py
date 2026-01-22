import os
from markdown_block import markdown_to_html_node


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dir_path_content):
        if os.path.exists(template_path):
            contents = os.listdir(dir_path_content)
            for item in contents:
                src_path = os.path.join(dir_path_content, item)
                dest_path = os.path.join(dest_dir_path, item)
                if os.path.isfile(src_path) and src_path.endswith(".md"):
                    dest_path = dest_path.replace(".md", ".html")
                    generate_page(src_path, template_path, dest_path, basepath)
                else:
                    os.makedirs(dest_path, exist_ok=True)
                    generate_page_recursive(
                        src_path, template_path, dest_path, basepath
                    )
        else:
            raise ValueError(f"Template file does not exist: {template_path}")

    else:
        raise ValueError(f"Content directory does not exist: {dir_path_content}")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating pages from {from_path} using {template_path} to {dest_path}")

    try:
        with open(from_path, "r") as from_file:
            markdown = from_file.read()
        with open(template_path, "r") as template_file:
            template_html = template_file.read()
    except Exception as e:
        raise ValueError(e)

    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    title = extract_title(markdown)

    final_html = template_html.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    final_html = final_html.replace('href="/', 'href="' + basepath)
    final_html = final_html.replace('src="/', 'src="' + basepath)

    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "w") as dest_file:
            dest_file.write(final_html)
    except Exception as e:
        raise ValueError(e)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("No title found in markdown")
