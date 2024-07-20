import unittest

from textnode import (
        TextNode,
        text_type_text,
        text_type_italic,
        text_type_bold,
        text_type_code
        )

from parse_inline_markdown import split_nodes_delimiter


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


class TestTextDelimiter(unittest.TestCase):
    def test_string_with_code(self):
        test_case = [TextNode(text="This has some `code within`it", text_type=text_type_text)]
        should_equal = [
                TextNode(text="This has some ", text_type=text_type_text), 
                TextNode(text="code within", text_type=text_type_code), 
                TextNode(text="it", text_type=text_type_text)
                ]
        result = split_nodes_delimiter(test_case, "`", text_type_text)
        self.assertListEqual(result, should_equal)

    def test_nested_string_formating(self):
        test_case = [TextNode(text="This *has **some** `code within`it*", text_type=text_type_text)]
        should_equal = [
                TextNode(text="This ", text_type=text_type_text),
                TextNode(text="has **some** `code within`it", text_type=text_type_italic)
                ]
        result = split_nodes_delimiter(test_case, "*", text_type_text)
        self.assertListEqual(result, should_equal)


if __name__ == "__main__":
    unittest.main()
