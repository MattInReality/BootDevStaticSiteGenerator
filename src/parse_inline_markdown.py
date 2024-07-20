from textnode import (
        TextNode,
        text_type_text,
        text_type_bold,
        text_type_italic,
        text_type_code,
        type_from_delimiter
        )


def split_nodes_delimiter(text_nodes: [TextNode], delimiter: str, text_type: str)->[TextNode]:
    new_nodes = []
    for node in text_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            sub_nodes = []
            node_text = ''
            delimiter_open = False
            # TODO this doesn't handle the * and ** well.
            for i, char in enumerate(node.text):
                if char != delimiter:
                    node_text = node_text + char
                if char == delimiter:
                    # Need to check if either of these checks are out of bounds
                    prev = node.text[i-1] if i-1 >= 0 else None
                    next = node.text[i+1] if i+1 < len(node.text) else None
                    if delimiter == prev or delimiter == next:
                        node_text = node_text + char
                    else:
                        sub_nodes.append(TextNode(text=node_text, text_type=type_from_delimiter(delimiter) if delimiter_open else text_type_text))
                        node_text = ''
                        delimiter_open = not delimiter_open
            if delimiter_open:
                raise Exception(f"Delimiter '{delimiter}' not closed in text '{node.text}'")
            if len(node_text) > 0:
                sub_nodes.append(TextNode(text=node_text, text_type=type_from_delimiter(delimiter) if delimiter_open else text_type_text))

            # THE PROBLEM - If a none, text type node is returned without reading, it's never going to read the internal.
            # No issue where we aren't parsing nested values but still relevant.

            #split_text = node.text.split(delimiter)
            #for index, text in enumerate(split_text):
            #    if len(text) == 0:
            #        continue
            #    if index % 2 != 0:
            #        sub_nodes.append(TextNode(text=text, text_type=delimiter_map[delimiter]))
            #    else:
            #        sub_nodes.append(TextNode(text=text, text_type=text_type_text))
            new_nodes.extend(sub_nodes)
            #for i, node in enumerate(new_nodes):
                #print(f"{i} - {node}")
    return new_nodes
