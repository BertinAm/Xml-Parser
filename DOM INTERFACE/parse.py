import re  # importing the re module to use regular expressions



class Parser: # Parser class to parse the XML content
    def __init__(self, xml):  # Constructor to initialize the parser
        self.xml = xml   # creating an xml attribute

    def parse(self):    # method to parse the XML content
        self.xml = self.xml.strip()     # removing the leading and trailing whitespaces
        self.xml = re.sub(r'<!--[\s\S]*?-->', '', self.xml)     # removing the comments
        return self.document()

    def document(self):
        return {
            "declaration": self.declaration(),
            "root": self.tag()
        }

    def declaration(self):
        m = self.match_func(r"^<\?xml\s*")
        if not m:
            return

        # tag
        node = {
            "attributes": {}
        }

        # attributes
        while not (self.eos() or self.is_func('?>')):
            attr = self.attribute_func()
            if not attr:
                return node
            node["attributes"][attr["name"]] = attr["value"]

        self.match_func(r"\?>\s*")

        if(len(node["attributes"]) == 0):
            del node["attributes"]

        return node

    def tag(self):
        m = self.match_func(r'^<([\w\-:.]+)\s*')
        if not m:
            return

        # name
        node = {
            "name": m[1],
            "attributes": {},
            "children": []
        }

        # attributes
        while not (self.eos() or self.is_func('>') or self.is_func('?>') or self.is_func('/>')):
            attr = self.attribute_func()
            if not attr:
                return node
            node["attributes"][attr["name"]] = attr["value"]

        # self closing tag
        if self.match_func(r"^\s*\/>\s*"):
            return node

        self.match_func(r">\s*")

        # content
        node["content"] = self.content()

        # children
        child = None
        while child := self.tag():
            node["children"].append(child)

        # closing
        self.match_func(r'^<\/([\w\-:.]+)\s*>\s*')

        return node

    def content(self):
        m = self.match_func(r"^([^<]*)")
        if m:
            return m[1]
        return ''

    def attribute_func(self):
        m = self.match_func(r'([\w:-]+)\s*=\s*("[^"]*"|\'[^\']*\'|\w+)\s*')
        if not m:
            return
        return {"name": m.group(1), "value": self.strip_func(m.group(2))}

    def strip_func(self, val):
        return re.sub(r"^['\"]|['\"]$", "", val)

    def match_func(self, pattern):
        m = re.match(pattern, self.xml)
        if not m:
            return
        self.xml = self.xml[m.end():]

        return m

    def eos(self):
        return len(self.xml) == 0

    def is_func(self, prefix):
        return self.xml.startswith(prefix)




def remove_empty_values(dictionary):
    if dictionary is None:
        return None
    
    if len(dictionary) == 0:
        print('None found', dictionary)
        return None
    
    if not isinstance(dictionary, dict):
        if isinstance(dictionary, list):
            cleaned_list = []
            for item in dictionary:
                cleaned_item = remove_empty_values(item)
                if cleaned_item:
                    cleaned_list.append(cleaned_item)
            return cleaned_list
        else:
            return dictionary
    
    result = {}
    for key, value in dictionary.items():
        cleaned_value = remove_empty_values(value)
        if cleaned_value:
            result[key] = cleaned_value
    
    return result


