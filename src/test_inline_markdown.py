import unittest

from src.parse_inline_markdown import extract_title
from textnode import (
    TextNode,
    text_type_text,
    text_type_italic,
    text_type_bold,
    text_type_code,
    text_type_link,
    text_type_image
)

from parse_inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links, text_to_text_nodes,
    markdown_to_blocks,
    block_to_block_type,
    extract_title
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


class TestTextDelimiter(unittest.TestCase):
    def test_string_with_code(self):
        test_case = [TextNode(text="This has some `code within`it", text_type=text_type_text)]
        should_equal = [
            TextNode(text="This has some ", text_type=text_type_text),
            TextNode(text="code within", text_type=text_type_code),
            TextNode(text="it", text_type=text_type_text)
        ]
        result = split_nodes_delimiter(test_case, "`", text_type_code)
        self.assertListEqual(result, should_equal)

    def test_nested_string_formating(self):
        test_case = [TextNode(text="This *has some `code within`it*", text_type=text_type_text)]
        should_equal = [
            TextNode(text="This ", text_type=text_type_text),
            TextNode(text="has some `code within`it", text_type=text_type_italic)
        ]
        result = split_nodes_delimiter(test_case, "*", text_type_italic)
        self.assertListEqual(result, should_equal)


class TestExtractLinkTypeFunctions(unittest.TestCase):
    def test_images_with_suggested_text(self):
        test_case = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        should_equal = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        result = extract_markdown_images(test_case)
        self.assertListEqual(should_equal, result)

    def test_images_with_single_link(self):
        test_case = "This is some new text with a great image: ![special image](http://i.greatimages.com/jfasdlfa.png)"
        should_equal = [
            ("special image", "http://i.greatimages.com/jfasdlfa.png")
        ]
        result = extract_markdown_images(test_case)
        self.assertListEqual(should_equal, result)

    def test_images_with_no_link(self):
        test_case = "This has no image in it"
        should_equal = []
        result = extract_markdown_images(test_case)
        self.assertListEqual(should_equal, result)

    def test_images_with_unclosed_image_url(self):
        test_case = "This is some new text with a great image: ![special image](http://i.greatimages.com/jfasdlfa.png"
        should_equal = []
        result = extract_markdown_images(test_case)
        self.assertListEqual(should_equal, result)

    def test_links_with_suggested_text(self):
        test_case = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        should_equal = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        result = extract_markdown_links(test_case)
        self.assertListEqual(should_equal, result)

    def test_links_with_single_link(self):
        test_case = "This is some new text with a great image: [special image](http://i.greatlinks.com/jfasdlfa.png)"
        should_equal = [
            ("special image", "http://i.greatlinks.com/jfasdlfa.png")
        ]
        result = extract_markdown_links(test_case)
        self.assertListEqual(should_equal, result)

    def test_links_with_no_link(self):
        test_case = "This has no image in it"
        should_equal = []
        result = extract_markdown_links(test_case)
        self.assertListEqual(should_equal, result)

    def test_images_with_unclosed_link_url(self):
        test_case = "This is some new text with a great image: [special image](http://i.greatimages.com/jfasdlfa.png"
        should_equal = []
        result = extract_markdown_links(test_case)
        self.assertListEqual(should_equal, result)


class TestTextToNodes(unittest.TestCase):
    def text_text_to_nodes_course_example(self):
        test_case = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        should_equal = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        result = text_to_text_nodes(test_case)
        self.assertListEqual(should_equal, result)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_example(self):
        test_cast_p1 = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words"
        test_case_p2 = " inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This"
        test_case_p3 = " is another list item"
        total_test_case = test_cast_p1 + test_case_p2 + test_case_p3
        should_equal = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        result = markdown_to_blocks(total_test_case)
        self.assertListEqual(should_equal, result)

    def test_markdow_to_blocks_more_comlplex(self):
        test_case_p1 = "# This is a level 1 heading\n\n## This is a level 2 heading\n\nThis is is a paragraph of text"
        test_case_p2 = "\n\nThis is a second paragraph of text\n\n## This is a level 2 heading\n\nThis is is a "
        test_case_p3 = "paragraph of text with a double empty line after it\n\n\n* This is the first list item\n"
        test_case_p4 = "* This is the second list item\n\n## This is a level 2 heading\n\nThis is is a paragraph of text"
        total_test_case = test_case_p1 + test_case_p2 + test_case_p3 + test_case_p4
        should_equal = [
            "# This is a level 1 heading",
            "## This is a level 2 heading",
            "This is is a paragraph of text",
            "This is a second paragraph of text",
            "## This is a level 2 heading",
            "This is is a paragraph of text with a double empty line after it",
            "* This is the first list item\n* This is the second list item",
            "## This is a level 2 heading",
            "This is is a paragraph of text",
        ]
        result = markdown_to_blocks(total_test_case)
        self.assertListEqual(should_equal, result)


class TestBlocksToBlockType(unittest.TestCase):
    def test_block_to_block_type_headings_1(self):
        test_case = "# This is a level 1 heading"
        should_equal = "h1"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_headings_2(self):
        test_case = "## This is a level 2 heading"
        should_equal = "h2"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_headings_3(self):
        test_case = "### This is a level 3 heading"
        should_equal = "h3"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_headings_4(self):
        test_case = "#### This is a level 4 heading"
        should_equal = "h4"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_headings_5(self):
        test_case = "##### This is a level 5 heading"
        should_equal = "h5"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_headings_6(self):
        test_case = "###### This is a level 6 heading"
        should_equal = "h6"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_headings_wrong(self):
        test_case = "####### This is a level 6 heading"
        should_equal = "paragraph"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_code(self):
        test_case = "```function javascriptFunction(arg1, arg2){\nreturn arg1 + arg2;\n}```"
        should_equal = 'code'
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_quote(self):
        test_case = ">This is the first line of a quote\n>This is the second line of a quote"
        should_equal = "quote"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_unordered_list_dash(self):
        test_case = "- This is the first list item.\n- This is the second list item.\n- This is the third list item."
        should_equal = "unordered_list"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_unordered_list_star(self):
        test_case = "* This is the first list item.\n* This is the second list item.\n* This is the third list item."
        should_equal = "unordered_list"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_ordered_list(self):
        test_case = "1. This is the first list item.\n2. This is the second list item.\n3. This is the third list item."
        should_equal = "ordered_list"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

    def test_block_to_block_type_incorrect_ordered_list(self):
        test_case = "1. This is the first list item.\n3. This is the second list item.\n4. This is the third list item."
        should_equal = "paragraph"
        result = block_to_block_type(test_case)
        self.assertEqual(should_equal, result)

class TestExtractHeadingText(unittest.TestCase):
    def test_extract_heading_text_1(self):
        markdown = "# This is the top heading\n\n## Then heading two\n\nThis is just a paragraph with a **bold** word and an *italic* word"
        should_equal = "This is the top heading"
        result = extract_title(markdown)
        self.assertEqual(should_equal, result)

    def test_extract_heading_text_with_no_heading(self):
        markdown = "## Then heading two\n\nThis is just a paragraph with a **bold** word and an *italic* word"
        self.assertRaises(ValueError, extract_title, markdown)


if __name__ == "__main__":
    unittest.main()
