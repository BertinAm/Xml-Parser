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

    def to_string(self, indent=0): # method to convert the node to a string
        res = " " * indent + "<" + self.tag_name  # creating a string with the tag name
        for attr, value in self.attributes.items(): # iterating through the attributes
            res += f' {attr}="{value}"'   # adding the attribute to the string
        if self.text or self.children:  # if the node has text or children
            res += ">"  # add a closing '>' character
            if self.text: # if the node has text
                res += self.text # add the text to the string
            for child in self.children:  # iterating through the children
                res += "\n" + child.to_string(indent + 2) # adding the child to the string
            res += "\n" + " " * indent + "</" + self.tag_name + ">"  # adding the closing tag to the string
        else: # if the node has no text or children
            res += "/>"  # add a self-closing '/>' character
        return res  # return the string


class Document: # Document class to represent the DOM tree
    def __init__(self): # Constructor to initialize the document
        self.root = None  #  creating a root attribute

    def create_element(self, tag_name):  # method to create a new node
        return Node(tag_name)   # returning a new node

    def set_root(self, node):   #  method to set the root node
        self.root = node   # setting the root node

    def to_string(self):  # method to convert the DOM tree to a string
        if self.root:  # if the root node exists
            return self.root.to_string()  # return the string representation of the root node
        return ""  # return an empty string if the root node does not exist


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





def generate_xml(xml_content, output_file_path): # function to generate the XML
    doc = parse_xml(xml_content) # parse the XML content
    xml_string = doc.to_string() # convert the DOM tree to a string

    with open(output_file_path, "w") as file: # open the output file
        file.write(xml_string) # write the XML string to the file

    print("XML generated and saved to", output_file_path)   # print a message to the console






def open_file_dialog(output_text): # function to open the file dialog
    file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])  # open the file dialog
    if file_path:  # if a file was selected
        with open(file_path, "r") as file:  # open the file
            xml_content = file.read() # read the file content
        output_file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML Files", "*.xml")])  # open the file dialog
        if output_file_path: # if a file was selected
            generate_xml(xml_content, output_file_path) # generate the XML
            with open(output_file_path, "r") as output_file:  # open the output file
                output_text.delete("1.0", tk.END)  # clear the text widget
                output_text.insert(tk.END, output_file.read())  # insert the XML into the text widget




def main():  # main function
    root = tk.Tk() # create a root window
    root.title("XML Generator")  # set the title of the window

    open_button = tk.Button(root, text="Open XML File", command=lambda: open_file_dialog(output_text))   # create a button to open the file dialog
    open_button.pack()  # pack the button into the window

    output_text = tk.Text(root, height=100, width=100)  # create a text widget to display the XML
    output_text.pack()  # pack the text widget into the window

    root.mainloop()  # start the main loop


if __name__ == "__main__": # if the script is run directly
    main() # run the main function
