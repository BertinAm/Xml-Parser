import re  # importing the re module to use regular expressions



class Parser: # Parser class to parse the XML content
    def __init__(self, xml):  # Constructor to initialize the parser
        self.xml = xml   # creating an xml attribute

    def parse(self):    # method to parse the XML content
        self.xml = self.xml.strip()     # removing the leading and trailing whitespaces
        self.xml = re.sub(r'<!--[\s\S]*?-->', '', self.xml)     # removing the comments
        return self.document()      # returning the document

    def document(self):    # method to parse the document
        return {    # returning a dictionary
            "declaration": self.declaration(),      # declaration key with the value as the declaration
            "root": self.tag()      # root key with the value as the root node
        }

    def declaration(self):      # method to parse the declaration
        m = self.match_func(r"^<\?xml\s*")    # matching the declaration
        if not m:   # if the declaration does not exist
            return    # return None

        # tag
        node = {    # creating a dictionary
            "attributes": {}    # attributes key with an empty dictionary as the value
        }

        # attributes    
        while not (self.eos() or self.is_func('?>')):   # while the end of the string or the end of the declaration is not reached
            attr = self.attribute_func()    # getting the attribute
            if not attr:    # if the attribute does not exist
                return node     # return the node
            node["attributes"][attr["name"]] = attr["value"]    # adding the attribute to the attributes dictionary

        self.match_func(r"\?>\s*")  # matching the end of the declaration

        if(len(node["attributes"]) == 0):   # if the attributes dictionary is empty
            del node["attributes"]      # delete the attributes key

        return node    # return the node

    def tag(self):  # method to parse the tag
        m = self.match_func(r'^<([\w\-:.]+)\s*')    # matching the tag
        if not m:   # if the tag does not exist
            return  # return None

        # name
        node = {    # creating a dictionary
            "name": m[1],   # name key with the value as the name of the tag
            "attributes": {},   # attributes key with an empty dictionary as the value
            "children": []  # children key with an empty list as the value
        }

        # attributes
        while not (self.eos() or self.is_func('>') or self.is_func('?>') or self.is_func('/>')):    # while the end of the string or the end of the tag is not reached
            attr = self.attribute_func()    # getting the attribute
            if not attr:    # if the attribute does not exist
                return node    # return the node
            node["attributes"][attr["name"]] = attr["value"]    # adding the attribute to the attributes dictionary

        # self closing tag
        if self.match_func(r"^\s*\/>\s*"):  # if the tag is self closing
            return node    # return the node

        self.match_func(r">\s*")    # matching the end of the tag

        # content
        node["content"] = self.content()    # content key with the value as the content of the tag

        # children
        child = None    # creating a child variable
        while child := self.tag():  # while the child exists
            node["children"].append(child)  # append the child to the children list

        # closing
        self.match_func(r'^<\/([\w\-:.]+)\s*>\s*')  # matching the end of the tag

        return node   # return the node

    def content(self):      # method to parse the content
        m = self.match_func(r"^([^<]*)")    # matching the content
        if m:   # if the content exists
            return m[1]    # return the content
        return ''   # return an empty string

    def attribute_func(self):   # method to parse the attribute
        m = self.match_func(r'([\w:-]+)\s*=\s*("[^"]*"|\'[^\']*\'|\w+)\s*')   # matching the attribute
        if not m:   # if the attribute does not exist
            return  # return None
        return {"name": m.group(1), "value": self.strip_func(m.group(2))}       # return a dictionary with the name and value of the attribute

    def strip_func(self, val):  # method to strip the attribute value
        return re.sub(r"^['\"]|['\"]$", "", val)    # removing the leading and trailing quotes

    def match_func(self, pattern):  # method to match the pattern
        m = re.match(pattern, self.xml) # matching the pattern
        if not m:   # if the pattern does not exist
            return  # return None
        self.xml = self.xml[m.end():]   # removing the matched pattern from the xml string

        return m    # return the matched pattern

    def eos(self):  # method to check if the end of the string is reached
        return len(self.xml) == 0   # return True if the end of the string is reached, else False

    def is_func(self, prefix):  # method to check if the string starts with the prefix
        return self.xml.startswith(prefix)  # return True if the string starts with the prefix, else False




def remove_empty_values(dictionary):    # method to remove the empty values from the dictionary
    if dictionary is None:  # if the dictionary is None
        return None    # return None
    
    if len(dictionary) == 0:    # if the dictionary is empty
        print('None found', dictionary)   # print the dictionary
        return None   # return None
    
    if not isinstance(dictionary, dict):    # if the dictionary is not a dictionary
        if isinstance(dictionary, list):    # if the dictionary is a list
            cleaned_list = []   # creating a cleaned_list variable
            for item in dictionary:  # iterating through the items in the dictionary
                cleaned_item = remove_empty_values(item)    # removing the empty values from the item
                if cleaned_item:    # if the cleaned item exists
                    cleaned_list.append(cleaned_item)   # append the cleaned item to the cleaned list
            return cleaned_list    # return the cleaned list
        else:   # if the dictionary is not a list
            return dictionary   # return the dictionary
    
    result = {}    # creating a result variable
    for key, value in dictionary.items():   # iterating through the items in the dictionary
        cleaned_value = remove_empty_values(value)  # removing the empty values from the value
        if cleaned_value:   # if the cleaned value exists
            result[key] = cleaned_value  # add the cleaned value to the result dictionary
    
    return result   # return the result dictionary


