import re

from htmlnode import HTMLnode, ParentNode
from textnode import text_node_to_html_node
from textnode import (
        TextNode,
        text_type_text,
        text_type_bold,
        text_type_italic,
        text_type_code,
        text_type_image,
        text_type_link,
        delimiter_from_type
        )


def split_nodes_delimiter(text_nodes: [TextNode], delimiter: str, text_type: str)->[TextNode]:
    new_nodes = []
    for node in text_nodes:
        if node.text_type == text_type:
            new_nodes.append(node)
            continue
        else:
            #TODO Italics is going to conflict with list items
            sub_nodes = []
            texts = node.text.split(delimiter)
            if len(texts) == 1:
                new_nodes.append(TextNode(text=texts[0], text_type=node.text_type))
            else:
                for i, text in enumerate(texts):
                    if len(text) == 0:
                        continue
                    if i % 2 == 1:
                        sub_nodes.append(TextNode(text=text, text_type=text_type))
                    else:
                        sub_nodes.append(TextNode(text=text, text_type=text_type_text))

            new_nodes.extend(sub_nodes)
    return new_nodes


def extract_markdown_images(text: str):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images


def extract_markdown_links(text: str):
    links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links


def split_nodes_image(old_nodes: [TextNode]):
    return_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            return_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        image_text = node.text
        if len(images) == 0:
            return_nodes.append(node)
        else:
            for image in images:
                image_split = image_text.split(f"![{image[0]}]({image[1]})", 1)
                image_node = TextNode(
                        text=image[0],
                        text_type=text_type_image,
                        url=image[1]
                        )
                if len(image_split[0]) + len(image_split[1]) == 0:
                    return_nodes.append(image_node)
                    continue
                if len(image_split[1]) == 0:
                    return_nodes.append(TextNode(text=image_split[0], text_type=text_type_text))
                    return_nodes.append(image_node)
                    # TODO: what is this for?
                else:
                    return_nodes.append(image_node)
                    return_nodes.append(TextNode(text=image_split[1],
                                                 text_type=text_type_text))
    return return_nodes


def split_nodes_link(old_nodes: [TextNode]):
    return_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            return_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        link_text = node.text
        if len(links) == 0:
            return_nodes.append(node)
        else:
            for link in links:
                link_split = link_text.split(f"[{link[0]}]({link[1]})", 1)
                link_node = TextNode(
                        text=link[0],
                        text_type=text_type_link,
                        url=link[1]
                        )
                if len(link_split[0]) + len(link_split[1]) == 0:
                    return_nodes.append(link_node)
                    continue
                if len(link_split[1]) == 0:
                    return_nodes.append(TextNode(text=link_split[0], text_type=text_type_text))
                    return_nodes.append(link_node)
                else:
                    return_nodes.append(link_node)
                    return_nodes.append(TextNode(text=link_split[1],
                                                 text_type=text_type_text))
    return return_nodes


def text_to_text_nodes(text: str):
    starting_node = TextNode(text=text, text_type=text_type_text)
    type_run_order = [text_type_bold,
                      text_type_italic,
                      text_type_code,
                      text_type_image,
                      text_type_link
                      ]
    node_list = [starting_node]
    for text_type in type_run_order:
        if text_type == text_type_link:
            node_list = split_nodes_link(node_list)
            continue
        if text_type == text_type_image:
            node_list = split_nodes_image(node_list)
            continue
        else:
            node_list = split_nodes_delimiter(
                    node_list,
                    delimiter=delimiter_from_type(text_type),
                    text_type=text_type
                    )

    return node_list


def markdown_to_blocks(markdown: str):
    blocks = []
    markdown = markdown.strip()
    lines = markdown.split("\n")
    current_text=""
    for line in lines:
        if len(line) == 0 and current_text != "":
            blocks.append(current_text.strip())
            current_text=""
            continue
        if len(line) == 0:
            continue
        else:
            current_text = current_text + "\n" + line
    blocks.append(current_text.strip())
    return blocks


def block_to_block_type(block: str):
    if block.startswith('###### '):
        return 'h6'
    if block.startswith('##### '):
        return 'h5'
    if block.startswith('#### '):
        return 'h4'
    if block.startswith('### '):
        return 'h3'
    if block.startswith('## '):
        return 'h2'
    if block.startswith('# '):
        return 'h1'
    if block.startswith('```') and block.endswith('```'):
        return 'code'
        # Check how many hash symbols and return heading
    if block.startswith('>'):
        if all(map(lambda x: x.startswith('>'), block.splitlines())):
            return 'quote'
    if block.startswith('* ') or block.startswith('- '):
        if all(map(lambda x: x.startswith(block[:1]), block.splitlines())):
            return 'unordered_list'
    if block.startswith('1. '):
        is_ordered_list = True
        for i, line in enumerate(block.splitlines(), start=1):
            if not line.startswith(f"{i}. "):
                is_ordered_list = False
                break
        if is_ordered_list:
            return 'ordered_list'
        else:
            return 'paragraph'
    else:
        return 'paragraph'


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    body = ParentNode(tag="div", children=[])
    for block in blocks:
        block_type = block_to_block_type(block)
        current_block = block_type_to_html_node(block_type)
        if block_type in ['unordered_list', 'ordered_list']:
            list_items = block.split("\n")
            for list_item in list_items:
                li = ParentNode(tag="li", children=[])
                    # Split on first space as all properly formatted markdown list items have a space before the text
                [_, text] = list_item.split(" ", 1)
                text_nodes = text_to_text_nodes(text)
                for text_node in text_nodes:
                    li.children.append(text_node_to_html_node(text_node))
                current_block.children.append(li)
        elif block_type == 'quote':
            quote_rows = block.split("\n")
            clean_rows = []
            for row in quote_rows:
                [_, text] = row.split(" ", 1)
                clean_rows.append(text)
            text_nodes = text_to_text_nodes(" ".join(clean_rows))
            for text_node in text_nodes:
                current_block.children.append(text_node_to_html_node(text_node))
        elif block_type == "code":
            clean_text = block.strip("```")
            text_node = TextNode(text=clean_text, text_type=text_type_code)
            current_block.children.append(text_node_to_html_node(text_node))
        elif block_type == "paragraph":
            text_nodes = text_to_text_nodes(block)
            for text_node in text_nodes:
                current_block.children.append(text_node_to_html_node(text_node))
        else:
            [_, clean_text] = block.split(" ", 1)
            text_nodes = text_to_text_nodes(clean_text)
            for text_node in text_nodes:
                current_block.children.append(text_node_to_html_node(text_node))

        body.children.append(current_block)
    return body





        # break the content in to text nodes.
        # convert the text nodes in to html nodes.
        # append them to the children of the block as leaves.
        # in the case of a list, each list item is a block that would have at least 1 child... a text node.


# Could this be a recursive function?
def text_to_children(text: str):
    # Always going to have at least one child
    children = []



def block_type_to_html_node(block_type: str):
    if block_type == "h1":
        return ParentNode(tag="h1", children=[])
    if block_type == "h2":
        return ParentNode(tag="h2", children=[])
    if block_type == "h3":
        return ParentNode(tag="h3", children=[])
    if block_type == "h4":
        return ParentNode(tag="h4", children=[])
    if block_type == "h5":
        return ParentNode(tag="h5", children=[])
    if block_type == "h6":
        return ParentNode(tag="h6", children=[])
    if block_type == "paragraph":
        return ParentNode(tag="p", children=[])
    if block_type == "code":
        return ParentNode(tag="pre", children=[])
    if block_type == "quote":
        return ParentNode(tag="blockquote", children=[])
    if block_type == "unordered_list":
        return ParentNode(tag="ul", children=[])
    if block_type == "ordered_list":
        return ParentNode(tag="ol", children=[])


def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    if len(blocks) == 0 or block_to_block_type(blocks[0]) != 'h1':
        raise ValueError("Markdown does not contain a title")
    heading = blocks[0]
    heading_text = heading.split(" ", 1)[1].strip()
    return heading_text