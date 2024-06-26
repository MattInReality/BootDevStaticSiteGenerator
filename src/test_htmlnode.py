import unittest

from htmlnode import HTMLnode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLnode(props={
            "href": "https://tests.com/pass", 
            "class": "fancy classnames flex", 
            "id": "main"
            })
        should_equal = " href=\"https://tests.com/pass\" class=\"fancy classnames flex\" id=\"main\" "
        self.assertEqual(node.props_to_html(), should_equal)


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag="p", value="paragraph content", props={"class": "flex"})
        should_equal = "<p class=\"flex\" >paragraph content</p>"
        self.assertEqual(node.to_html(), should_equal)

    def test_missing_value(self):
        with self.assertRaises(TypeError):
            missing_value = LeafNode()

    def test_empty_value(self):
        with self.assertRaises(ValueError):
            empty_value = LeafNode(value="")
            empty_value.to_html()

    def test_img_element(self):
        node = LeafNode(tag="img", value="", props={"src": "image.jpg", "alt": "not really an image"})
        should_equal = "<img src=\"image.jpg\" alt=\"not really an image\" ></img>"
        self.assertEqual(node.to_html(), should_equal)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
                tag="div",
                children=[
                    LeafNode(tag="p", value="content line one"),
                    LeafNode(tag="p", value="content line two"),
                    LeafNode(tag="span", value="span content")
                    ]
                )
        should_equal = "<div><p>content line one</p><p>content line two</p><span>span content</span></div>"
        self.assertEqual(node.to_html(), should_equal)

    def test_nested_parents(self):
        node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="div",
                    children=[
                        LeafNode(tag="p", value="nested content line one"),
                        LeafNode(tag="p", value="nested content line two"),
                        LeafNode(tag="span", value="nested span content", props={"class": "flex"})
                    ]
                ),
                LeafNode(tag="p", value="content line one"),
                LeafNode(tag="p", value="content line two"),
                LeafNode(tag="span", value="span content")
            ]
        )
        should_equal = "<div><div><p>nested content line one</p><p>nested content line two</p><span class=\"flex\" >nested span content</span></div><p>content line one</p><p>content line two</p><span>span content</span></div>"
        self.assertEqual(node.to_html(), should_equal)

    def test_nested_children_raise(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                tag="div",
                children=[
                    ParentNode(
                        tag="div",
                        children=[
                            LeafNode(tag="p", value="nested content line one"),
                            LeafNode(tag="p", value=""),
                            LeafNode(tag="span", value="nested span content", props={"class": "flex"})
                        ]
                    ),
                    LeafNode(tag="p", value="content line one"),
                    LeafNode(tag="p", value="content line two"),
                    LeafNode(tag="span", value="span content")
                ]
            )
            node.to_html()


if __name__ == "__main__":
    unittest.main()

