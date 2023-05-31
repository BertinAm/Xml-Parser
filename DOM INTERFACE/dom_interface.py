import tkinter as tk
from tkinter import filedialog


class Node:
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.children = []
        self.attributes = {}
        self.text = ""

    def add_child(self, child):
        self.children.append(child)

    def set_attribute(self, attr, value):
        self.attributes[attr] = value

    def get_attribute(self, attr):
        return self.attributes.get(attr, None)

    def set_text(self, text):
        if not self.text:
            self.text = ""
        self.text += text

    def to_string(self, indent=0):
        res = " " * indent + "<" + self.tag_name
        for attr, value in self.attributes.items():
            res += f' {attr}="{value}"'
        if self.text or self.children:
            res += ">"
            if self.text:
                res += self.text
            for child in self.children:
                res += "\n" + child.to_string(indent + 2)
            if self.children:
                res += "\n" + " " * indent
            res += "</" + self.tag_name + ">"
        else:
            res += "/>"
        return res


class Document:
    def __init__(self):
        self.root = None

    def create_element(self, tag_name):
        return Node(tag_name)

    def set_root(self, node):
        self.root = node

    def to_string(self):
        if self.root:
            return self.root.to_string()
        return ""


def parse_xml(xml_content):
    stack = []
    current_node = None
    doc = Document()

    lines = xml_content.split('<')[1:]
    for line in lines:
        if line.startswith('/'):
            tag_name = line.split('>')[0][1:]
            if stack:
                current_node = stack.pop()
                if stack:
                    stack[-1].add_child(current_node)
                else:
                    doc.set_root(current_node)
        else:
            tag_name = line.split('>')[0]
            if tag_name.endswith('/'):
                tag_name = tag_name[:-1].strip()
                node = doc.create_element(tag_name)
                if current_node:
                    current_node.add_child(node)
            else:
                if " " in tag_name:
                    tag_name, attr_str = tag_name.split(" ", 1)
                    attrs = attr_str.strip().split("=")
                    if len(attrs) == 2:
                        attr_name = attrs[0].strip()
                        attr_value = attrs[1].strip().strip('"')
                        node = doc.create_element(tag_name)
                        node.set_attribute(attr_name, attr_value)
                    else:
                        node = doc.create_element(tag_name)
                else:
                    node = doc.create_element(tag_name)

                if current_node:
                    current_node.add_child(node)
                    stack.append(current_node)
                current_node = node

    return doc


def generate_xml(xml_content, output_file_path):
    doc = parse_xml(xml_content)
    xml_string = doc.to_string()

    with open(output_file_path, "w") as file:
        file.write(xml_string)

    print("XML generated and saved to", output_file_path)


def open_file_dialog(output_text):
    output_text.delete("1.0", tk.END)  # Clear the text widget

    file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    if file_path:
        with open(file_path, "r") as file:
            xml_content = file.read()
        output_file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML Files", "*.xml")])
        if output_file_path:
            generate_xml(xml_content, output_file_path)
            with open(output_file_path, "r") as output_file:
                output_text.insert(tk.END, output_file.read())



def main():
    root = tk.Tk()
    root.title("XML Generator")

    open_button = tk.Button(root, text="Open XML File", command=lambda: open_file_dialog(output_text))
    open_button.pack()

    output_text = tk.Text(root, height=100, width=100)
    output_text.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
