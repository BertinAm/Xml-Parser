'''file_path = input("Enter the path to the XML file: ")
try:
    with open(file_path, 'r') as file:
        xml_content = file.read()
except IOError:
        print('Error: File not found.')
        error = True '''
error_message = {}          # Dictionary to store error messages
def validate_xml(xml_content = '', err_msg = {}): # function to validate the XML
            i = 0 # index to iterate over the XML content
            stack = []  # Stack to store the opening tags
            root_element = 0    # Variable to store the root element
            root_element_count = 0  # Variable to store the root element count
            error = False   # Variable to store the error status

            while i < len(xml_content): # Iterate over the XML content
                if xml_content[i] == '<':   # Check if the character is '<'
                    if i + 1 < len(xml_content) and xml_content[i + 1] == '/':      # Check if the next character is '/'
                        # Closing tag
                        i += 2  # Increment the index by 2 to skip the '<' and '/'
                        closing_tag = ''    # Variable to store the closing tag
                        while i < len(xml_content) and xml_content[i] != '>':   # Iterate over the characters until '>'
                            closing_tag += xml_content[i]   # Append the character to the closing tag
                            i += 1      # Increment the index

                        if not stack:   # Check if the stack is empty
                            print ('Error: Found closing tag without matching opening tag:', closing_tag)   # Print error message
                            error_message['Error 1'] = 'Error: Found closing tag without matching opening tag: ' + closing_tag  # Store error message
                            error = True    # Set error to True
                        
                        if stack:   # Check if the stack is not empty
                            opening_tag = stack[-1]    # Get the last element from the stack
                        
                        if opening_tag != closing_tag:  # Check if the opening and closing tags are not equal
                            print ('Error: Mismatched opening and closing tags:', opening_tag, closing_tag) # Print error message
                            error_message['Error 2'] = 'Error: Mismatched opening and closing tags: ' + opening_tag + ' ' + closing_tag # Store error message
                            error = True    # Set error to True
                        
                        if stack:   # Check if the stack is not empty
                            stack.pop() # Remove the last element from the stack
                            root_element -= 1   # Decrement the root element count
                    
                    # Check xml declaration
                    elif i + 1 < len(xml_content) and xml_content[i + 1] == '?':    # Check if the next character is '?'
                        space = 0   # Variable to store the number of spaces
                        if i != 0:  # Check if the index is not 0
                            print('Error: XML declaration in wrong position')   # Print error message
                            error_message['Error 3'] = 'Error: XML declaration in wrong position'   # Store error message
                            error = True    # Set error to True
                        i += 2  # Increment the index by 2 to skip the '<' and '?'
                        xml_tag = ''    # Variable to store the xml tag
                        while i < len(xml_content) and xml_content[i] != '>':   # Iterate over the characters until '>'
                            if xml_content[i] == ' ':   # Check if the character is a space
                                space += 1  # Increment the space count
                            if xml_content[i] == '?':   # Check if the character is '?'
                                break   # Break the loop
                            if space == 0:  # Check if the space count is 0
                                xml_tag += xml_content[i]   # Append the character to the xml tag
                            i += 1  # Increment the index
                        # Check closing tag for declaration 
                        if xml_content[i] == '>':   # Check if the character is '>'
                            if xml_content[i - 1] != '?':   # Check if the previous character is not '?'
                                print('Error: Invalid xml declaration')  # Print error message
                                error_message['Error 4'] = 'Error: Invalid xml declaration' # Store error message
                                error = True    # Set error to True
                        if space > 3:   # Check if the space count is greater than 3
                            print('Error: Invalid number of attributes in declarations')    # Print error message
                            error_message['Error 5'] = 'Error: Invalid number of attributes in declarations'    # Store error message
                            error = True    # Set error to True
                        if xml_tag.lower() == 'xml':    # Check if the xml tag is 'xml'
                            continue    # Skip the xml tag
                        else:   # Check if the xml tag is not 'xml'
                            print('Error: Invalid xml declaration') # Print error message
                            error_message['Error 6'] = 'Error: Invalid xml declaration' # Store error message
                            error = True    # Set error to True

                    # Check comments
                    elif i + 2 < len(xml_content) and xml_content[i + 1] == '!' and xml_content[i + 2] == xml_content[i + 3] == '-':    # Check if the next character is '!'
                        i += 4  # Increment the index by 4 to skip the '<', '!', '-' and '-'
                        while i < len(xml_content) and xml_content[i] != '>':   # Iterate over the characters until '>'
                            i += 1  # Increment the index

                        if xml_content[i - 1] == xml_content[i - 2] == '-': # Check if the previous characters are '-'
                            continue    # Skip the comment
                        else:   # Check if the previous characters are not '-'
                            print('Error: Invalid comment style')   # Print error message
                            error_message['Error 7'] = 'Error: Invalid comment style'   # Store error message
                            error = True    # Set error to True

                    else:       # Check if the next character is not '/'
                        # Opening tag   
                        i += 1  # Increment the index by 1 to skip the '<'
                        opening_tag = ''    # Variable to store the opening tag
                        while i < len(xml_content) and xml_content[i] not in ['>', ' ', '/']:   # Iterate over the characters until '>', ' ', '/'
                            opening_tag += xml_content[i]   # Append the character to the opening tag
                            i += 1  # Increment the index

                        if xml_content[i] == '/' and xml_content[i + 1] == '>':     # Check if the next character is '/' and '>'
                            # Self-closing tag
                            opening_tag = ''    # Variable to store the opening tag
                            i += 2      # Increment the index by 2 to skip the '/' and '>'
                            continue # Skip the self-closing tag '/'

                        # validate Doctype declaration
                        if opening_tag.lower() == '!doctype':   # Check if the opening tag is '!doctype'
                            opening_tag = ''    # Variable to store the opening tag
                            continue    # Skip the doctype declaration

                        stack.append(opening_tag)   # Append the opening tag to the stack
                        root_element += 1   # Increment the root element count

                    if root_element == 0:   # Check if the root element count is 0
                        root_element_count += 1 # Increment the root element count
                else:   # Check if the character is not '<'
                    i += 1  # Increment the index

            if stack:   # Check if the stack is not empty
                print ('Error: Found opening tag without matching closing tag:', stack.pop())   # Print error message
                error_message['Error 8'] = 'Error: Found opening tag without matching closing tag: ' + stack.pop()  # Store error message
                error = True    # Set error to True
            if root_element_count != 1: # Check if the root element count is not 1
                print ('Error: Document does not contain root element')  # Print error message
                error_message['Error 9'] = 'Error: Document does not contain root element'  # Store error message
                error = True    # Set error to True
                err_msg = error_message # Store error message
            if error == True:   # Check if error is True
                return False, err_msg   # Return False and error message
            else:   # Check if error is False
                return True # Return True

# validate_xml(xml_content)
# print("Validation Status:", validate_xml())