from htmlnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=""):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node):
        return (self.text == text_node.text and
                self.text_type == text_node.text_type and
                self.url == text_node.url
                )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
delimiter_map = {
        "`": text_type_code,
        "*": text_type_italic,
        "**": text_type_bold,
        }


def type_from_delimiter(delimiter):
    if delimiter == "*":
        return text_type_italic
    if delimiter == "**":
        return text_type_bold
    if delimiter == "`":
        return text_type_code
    return None


def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    if text_type == text_type_text:
        return LeafNode(tag="", value=text_node.text)
    if text_type == text_type_bold:
        return LeafNode(tag="b", value=text_node.text)
    if text_type == text_type_italic:
        return LeafNode(tag="i", value=text_node.text)
    if text_type == text_type_code:
        return LeafNode(tag="code", value=text_node.text)
    if text_type == text_type_link:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_type == text_type_image:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("TextNode must have a valid text type")
