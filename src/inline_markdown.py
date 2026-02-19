import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for phrase in old_nodes:
        if phrase.text_type != TextType.TEXT:
            new_list.append(TextNode(phrase.text, phrase.text_type, phrase.url))
        else:
            sections = phrase.text.split(delimiter)
            if len(sections) == 1:
                new_list.append(phrase)
                continue
            if len(sections) % 2 == 0:
                raise ValueError("No final delimiter")
            for i, section in enumerate(sections):
                if i%2==0:
                    new_list.append(TextNode(section, TextType.TEXT))
                else:
                    new_list.append(TextNode(section, text_type))
    return new_list
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
def split_nodes_image(old_nodes):
    new_list = []
    for phrase in old_nodes:
        if phrase.text_type != TextType.TEXT:
            new_list.append(TextNode(phrase.text, phrase.text_type, phrase.url))
        else:
            matches = extract_markdown_images(phrase.text)
            original_text = phrase.text
            if len(matches) == 0:
                new_list.append(phrase)
                continue
            for (alt, url) in matches:
                split_phrase = original_text.split(f"![{alt}]({url})", 1)
                if split_phrase[0] != "":
                    new_list.append(TextNode(split_phrase[0], TextType.TEXT))         
                new_list.append(TextNode(alt, TextType.IMAGE, url))
                original_text = split_phrase[1]
            if original_text != "":
                new_list.append(TextNode(original_text, TextType.TEXT))
    return new_list
def split_nodes_link(old_nodes):
    new_list = []
    for phrase in old_nodes:
        if phrase.text_type != TextType.TEXT:
            new_list.append(TextNode(phrase.text, phrase.text_type, phrase.url))
        else:
            matches = extract_markdown_links(phrase.text)
            original_text = phrase.text
            if len(matches) == 0:
                new_list.append(phrase)
                continue
            for (alt, url) in matches:
                split_phrase = original_text.split(f"[{alt}]({url})", 1)
                if split_phrase[0] != "":
                    new_list.append(TextNode(split_phrase[0], TextType.TEXT))         
                new_list.append(TextNode(alt, TextType.LINK, url))
                original_text = split_phrase[1]
            if original_text != "":
                new_list.append(TextNode(original_text, TextType.TEXT))
    return new_list
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
