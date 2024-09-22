import unittest

from textnode import (
        TextNode,
        text_type_text,
        text_type_italic,
        text_type_bold,
        text_type_code
        )


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_not_eq_on_text(self):
        node = TextNode("This is a text node 1", text_type_bold)
        node2 = TextNode("This is a text node 2", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_not_eq_on_font_style(self):
        node = TextNode("This is a text node", text_type_italic)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_not_eq_on_font_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://thetest.co.uk")
        node2 = TextNode("This is a text node", text_type_italic, "http://thetest2.co.uk")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
