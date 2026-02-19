from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from htmlnode import LeafNode, HTMLNode, ParentNode
from enum import Enum
class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        if blocks[i] == "":
           blocks.pop(i) 
        blocks[i] = blocks[i].lstrip(" ")
        blocks[i] = blocks[i].rstrip(" ")
    return blocks
def block_to_block_type(block):
    if block[0]+block[1] == "# " or block[0]+block[1]+block[2] == "## " or block[0]+block[1]+block[2]+block[3]=="### " or block[0]+block[1]+block[2]+block[3]+block[4]=="#### " or block[0]+block[1]+block[2]+block[3]+block[4]+block[5]=="##### " or block[0]+block[1]+block[2]+block[3]+block[4]+block[5]+block[6]=="###### ":
        return BlockType.heading
    elif block[0]+block[1]+block[2]+block[3] == "```\n" and block[len(block)-1]+block[len(block)-2]+block[len(block)-3] == "```":
        return BlockType.code
    else:
        block = block.split("\n")
        orde = 1
        unor = 0
        qu = 0
        n = len(block)
        for line in block:
            if line.startswith(">"):
                qu += 1
            elif line.startswith("- "):
                unor += 1
            elif line.startswith(str(orde)+". "):
                orde += 1
        if orde == n+1:
            return BlockType.ordered_list
        elif unor == n:
            return BlockType.unordered_list
        elif qu == n:
            return BlockType.quote
        else:
            return BlockType.paragraph
def text_to_children(text):
    new_text = text_to_textnodes(text)
    new_children = []
    for texts in new_text:
        html_text = text_node_to_html_node(texts)
        new_children.append(html_text)
    return new_children
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    list_of_children = []
    for block in blocks:
        type_of_block = block_to_block_type(block)
        if type_of_block == BlockType.paragraph:
            new_html_child = ParentNode(tag="p", children=text_to_children(block))
            list_of_children.append(new_html_child)
        elif type_of_block == BlockType.heading:
            n = 0
            for _ in block:
                if _ == "#":
                    n+=1
                else:
                    break
            new_block = block.lstrip("#").strip()
            new_html_child = ParentNode(tag=f"h{n}", children=text_to_children(new_block))
            list_of_children.append(new_html_child)
        elif type_of_block == BlockType.quote:
            new_block = block.split("\n")
            stripped_lines = []
            for line in new_block:
                stripped_lines.append(line.lstrip(">").strip())
            combined_text = " ".join(stripped_lines)
            new_html_child = ParentNode(tag="blockquote", children=text_to_children(combined_text))
            list_of_children.append(new_html_child)
        elif type_of_block == BlockType.code:
            new_block = block.lstrip("```").strip()
            new_block = new_block.rstrip("```").strip()
            code_content = TextNode(text=new_block, text_type = TextType.TEXT)
            code_leaf_node = text_node_to_html_node(code_content)
            new_code_child = ParentNode(tag="code", children =[code_leaf_node])
            new_pre_child = ParentNode(tag=f"pre", children=[new_code_child])
            list_of_children.append(new_pre_child)
        elif type_of_block == BlockType.unordered_list:
            new_block = block.split("\n")
            unordered_list_children = []
            for line in new_block:
                line = line.lstrip("- ")
                child = text_to_children(line)
                childe = ParentNode(tag="li", children=child)
                unordered_list_children.append(childe)
            list_parent = ParentNode(tag="ul", children=unordered_list_children)
            list_of_children.append(list_parent)
        elif type_of_block == BlockType.ordered_list:
            new_block = block.split("\n")
            ordered_list_children = []
            n=0
            for line in new_block:
                n+=1
                line = line.split(f". ", 1)[1]
                child = text_to_children(line)
                childe = ParentNode(tag="li", children=child)
                ordered_list_children.append(childe)
            list_parent = ParentNode(tag="ol", children=ordered_list_children)
            list_of_children.append(list_parent)
    father_html_node = ParentNode(tag="div", children=list_of_children)
    return father_html_node