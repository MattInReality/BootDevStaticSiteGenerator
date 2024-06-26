from textnode import (
        TextNode,
        text_type_text,
        text_type_bold,

        text_type_italic,
        text_type_code,
        delimiter_map
        )


def split_nodes_delimiter(text_nodes: [TextNode], delimiter: str, text_type: str)->[TextNode]:
    new_nodes = []
    for node in text_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            for index, text in enumerate(split_text):
                if len(text) == 0:
                    continue
                if index % 2 != 0:
                    new_nodes.append(TextNode(text=text, text_type=delimiter_map[delimiter]))
                else:
                    new_nodes.append(TextNode(text=text, text_type=text_type_text))

    return new_nodes
