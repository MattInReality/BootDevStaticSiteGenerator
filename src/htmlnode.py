
class HTMLnode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLnode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + "".join([f"{k}=\"{v}\" " for k, v in self.props.items()])


class LeafNode(HTMLnode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(value=value, tag=tag, props=props)

    def to_html(self):
        if not self.value and self.tag != "img":
            raise ValueError("A LeafNode must have a value")
        if not self.tag:
            return f"{self.value}"
        props = self.props_to_html()
        opening_tag = f"<{self.tag}{props}>"
        closing_tag = f"</{self.tag}>"

        return f"{opening_tag}{self.value}{closing_tag}"


class ParentNode(HTMLnode):
    def __init__(self, tag, children):
        super().__init__(tag=tag, children=children)

    def to_html(self):
        if len(self.children) < 1:
            raise ValueError("A ParentNode must have children")
        html = f"<{self.tag}>"
        for child in self.children:
            html = html + child.to_html()
        html = html + f"</{self.tag}>"
        return html

 

