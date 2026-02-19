import os
from block_markdown import markdown_to_html_node
from pathlib import Path

def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    list_of_files = os.listdir(dir_path_content)
    for i in list_of_files:
        path_to_file = os.path.join(dir_path_content, i)
        if os.path.isfile(path_to_file) == True:
            dest_path_f = os.path.join(dest_dir_path, i)
            html_path = Path(dest_path_f).with_suffix(".html")
            generate_page(path_to_file, template_path, html_path, basepath)
        elif os.path.isdir(path_to_file) == True:
            path_to_dir = os.path.join(dir_path_content, i)
            path_to_dest_dir = os.path.join(dest_dir_path, i)
            generate_pages_recursive(path_to_dir, template_path, path_to_dest_dir, basepath)