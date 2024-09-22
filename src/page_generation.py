import os
from parse_inline_markdown import (
    markdown_to_html_node,
    extract_title
)


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise FileNotFoundError(f'{from_path} does not exist')
    if not os.path.exists(template_path):
        raise FileNotFoundError(f'{template_path} does not exist')
    template = open(template_path, "r").read()
    markdown = open(from_path, "r").read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    with open(dest_path, "w") as file:
        file.write(template)
        file.close()


def generate_pages_recursive(source_dir, template_path, target_dir):
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f'{source_dir} does not exist')
    source_items = os.listdir(source_dir)
    if len(source_items) == 0:
        return
    for item in source_items:
        if os.path.isdir(os.path.join(source_dir, item)):
            os.makedirs(os.path.join(target_dir, item))
            generate_pages_recursive(os.path.join(source_dir, item), template_path, os.path.join(target_dir, item))
            continue
        if os.path.isfile(os.path.join(source_dir, item)):
            filename = item.split(".md")[0] + ".html"
            generate_page(os.path.join(source_dir, item), template_path, os.path.join(target_dir, filename))


