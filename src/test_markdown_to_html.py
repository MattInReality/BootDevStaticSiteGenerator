import unittest
from parse_inline_markdown import markdown_to_html_node

class test_markdown_to_html(unittest.TestCase):
    def test_markdown_to_html(self):
        markdown = "# This is the top heading\n\n## Then heading two\n\n"
        result = markdown_to_html_node(markdown)
        html = result.to_html()
        self.assertEqual(html, "<div><h1>This is the top heading</h1><h2>Then heading two</h2></div>")

    def test_markdown_to_html_with_inline_markdown(self):
        markdown = "# This is the top heading\n\n## Then heading two\n\nThis is just a paragraph with a **bold** word and an *italic* word"
        result = markdown_to_html_node(markdown)
        html = result.to_html()
        self.assertEqual(html, "<div><h1>This is the top heading</h1><h2>Then heading two</h2><p>This is just a paragraph with a <b>bold</b> word and an <i>italic</i> word</p></div>")

    def test_with_just_paragraphs(self):
        markdown = "This is some text on a row\n\nThis is some more on another row"
        result = markdown_to_html_node(markdown)
        html = result.to_html()
        self.assertEqual(html, "<div><p>This is some text on a row</p><p>This is some more on another row</p></div>")

    def test_with_paragraphs_code_and_headings(self):
        markdown = "# This is the top heading\n\n## This is some more on another row\n\nThis is just a paragraph with a **bold** word and `inline code` value.\n\n## A subheading for the code block\n\n```Some code in a block\nmulti-line\njust to be sure```\n\nThen just a paragraph"
        result = markdown_to_html_node(markdown)
        html = result.to_html()
        self.assertEqual(html, "<div><h1>This is the top heading</h1><h2>This is some more on another row</h2><p>This is just a paragraph with a <b>bold</b> word and <code>inline code</code> value.</p><h2>A subheading for the code block</h2><pre><code>Some code in a block\nmulti-line\njust to be sure</code></pre><p>Then just a paragraph</p></div>")

