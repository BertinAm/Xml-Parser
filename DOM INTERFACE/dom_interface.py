import tkinter as tk    # importing the tkinter library as tk
from tkinter import filedialog # importing the filedialog module from tkinter


class Node:          # Node class to represent a node in the DOM tree
    def __init__(self, tag_name):   # Constructor to initialize the node
        self.tag_name = tag_name    # creating a tag_name attribute
        self.children = []          # creating a children attribute
        self.attributes = {}        # creating an attributes attribute
        self.text = ""              # creating a text attribute

    def add_child(self, child):     # method to add a child node
        self.children.append(child) # appending the child node to the children list

    def set_attribute(self, attr, value):   # method to set an attribute
        self.attributes[attr] = value       # setting the attribute

    def get_attribute(self, attr):          # method to get an attribute
        return self.attributes.get(attr, None)      # returning the attribute

    def set_text(self, text):   # method to set the text
        if not self.text:       # if the text is empty
            self.text = ""      # set the text to empty
        self.text += text       # append the text to the text attribute

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
            res += "\n" + " " * indent + "</" + self.tag_name + ">"
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
    stack = []                   # Stack to keep track of parent nodes
    current_node = None          # Current node being processed
    doc = Document()             # Create a new Document object

    lines = xml_content.split('<')[1:]  # Split the content by '<' character and ignore the first element
    for line in lines:
        if line.startswith('/'):         # Closing tag
            tag_name = line.split('>')[0][1:]  # Extract the tag name by splitting at '>' and removing the '/'
            if stack:
                current_node = stack.pop()      # Pop the parent node from the stack
        else:
            tag_name = line.split('>')[0]        # Opening tag
            if tag_name.endswith('/'):           # Self-closing tag
                tag_name = tag_name[:-1].strip()     # Remove the '/' at the end and strip any extra whitespace
                node = doc.create_element(tag_name)  # Create a new node with the tag name
                if current_node:
                    current_node.add_child(node)     # Add the node as a child of the current parent node
            else:
                if " " in tag_name:                  # Tag with attributes
                    tag_name, attr_str = tag_name.split(" ", 1)  # Split the tag name and attribute string at the first space
                    attrs = attr_str.strip().split("=")           # Split the attribute string into individual attributes
                    if len(attrs) == 2:
                        attr_name = attrs[0].strip()               # Extract the attribute name
                        attr_value = attrs[1].strip().strip('"')   # Extract the attribute value (stripping surrounding quotes)
                        node = doc.create_element(tag_name)        # Create a new node with the tag name
                        node.set_attribute(attr_name, attr_value)  # Set the attribute on the node
                    else:
                        node = doc.create_element(tag_name)        # Create a new node with the tag name
                else:
                    node = doc.create_element(tag_name)            # Tag without attributes

                if current_node:
                    current_node.add_child(node)                    # Add the node as a child of the current parent node
                    stack.append(current_node)                      # Push the current parent node onto the stack
                current_node = node                                  # Update the current node

    doc.set_root(current_node)  # Set the root node after parsing is complete
    return doc





def generate_xml(xml_content, output_file_path):
    doc = parse_xml(xml_content)
    xml_string = doc.to_string()

    with open(output_file_path, "w") as file:
        file.write(xml_string)

    print("XML generated and saved to", output_file_path)






def open_file_dialog(output_text):
    file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    if file_path:
        with open(file_path, "r") as file:
            xml_content = file.read()
        output_file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML Files", "*.xml")])
        if output_file_path:
            generate_xml(xml_content, output_file_path)
            with open(output_file_path, "r") as output_file:
                output_text.delete("1.0", tk.END)
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
