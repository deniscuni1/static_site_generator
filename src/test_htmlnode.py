import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode(tag=None, value=None, children=None, props=None)
        node2 = HTMLNode(tag="p", value=None, children=None, props=None)
        self.assertNotEqual(node, node2)
    def test_children(self):
        node = HTMLNode(tag=None, value=None, children=None, props=None)
        node2 = HTMLNode(tag=None, value=None, children=[HTMLNode(tag="p")], props=None)
        self.assertNotEqual(node, node2)
    def test_value(self):
        node = HTMLNode(tag=None, value=None, children=None, props=None)
        node2 = HTMLNode(tag=None, value="text", children=None, props=None)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()