'''file_path = input("Enter the path to the XML file: ")
try:
    with open(file_path, 'r') as file:
        xml_content = file.read()
except IOError:
        print('Error: File not found.')
        error = True '''
error_message = {}          
def validate_xml(xml_content = '', err_msg = {}):
            i = 0
            stack = []
            root_element = 0
            root_element_count = 0
            error = False

            while i < len(xml_content):
                if xml_content[i] == '<':
                    if i + 1 < len(xml_content) and xml_content[i + 1] == '/':
                        # Closing tag
                        i += 2
                        closing_tag = ''
                        while i < len(xml_content) and xml_content[i] != '>':
                            closing_tag += xml_content[i]
                            i += 1

                        if not stack:
                            print ('Error: Found closing tag without matching opening tag:', closing_tag)
                            error_message['Error 1'] = 'Error: Found closing tag without matching opening tag: ' + closing_tag
                            error = True
                        
                        if stack:
                            opening_tag = stack[-1]
                        
                        if opening_tag != closing_tag:
                            print ('Error: Mismatched opening and closing tags:', opening_tag, closing_tag)
                            error_message['Error 2'] = 'Error: Mismatched opening and closing tags: ' + opening_tag + ' ' + closing_tag
                            error = True
                        
                        if stack:
                            stack.pop()
                            root_element -= 1
                    
                    # Check xml declaration
                    elif i + 1 < len(xml_content) and xml_content[i + 1] == '?':
                        space = 0
                        if i != 0:
                            print('Error: XML declaration in wrong position')
                            error_message['Error 3'] = 'Error: XML declaration in wrong position'
                            error = True
                        i += 2
                        xml_tag = ''
                        while i < len(xml_content) and xml_content[i] != '>':
                            if xml_content[i] == ' ':
                                space += 1
                            if xml_content[i] == '?':
                                break
                            if space == 0:
                                xml_tag += xml_content[i] 
                            i += 1
                        # Check closing tag for declaration
                        if xml_content[i] == '>':
                            if xml_content[i - 1] != '?':
                                print('Error: Invalid xml declaration')
                                error_message['Error 4'] = 'Error: Invalid xml declaration'
                                error = True
                        if space > 3:
                            print('Error: Invalid number of attributes in declarations')
                            error_message['Error 5'] = 'Error: Invalid number of attributes in declarations'
                            error = True
                        if xml_tag.lower() == 'xml':
                            continue
                        else:
                            print('Error: Invalid xml declaration')
                            error_message['Error 6'] = 'Error: Invalid xml declaration'
                            error = True

                    # Check comments
                    elif i + 2 < len(xml_content) and xml_content[i + 1] == '!' and xml_content[i + 2] == xml_content[i + 3] == '-':
                        i += 4
                        while i < len(xml_content) and xml_content[i] != '>':
                            i += 1

                        if xml_content[i - 1] == xml_content[i - 2] == '-':
                            continue
                        else:
                            print('Error: Invalid comment style')
                            error_message['Error 7'] = 'Error: Invalid comment style'
                            error = True

                    else:
                        # Opening tag
                        i += 1
                        opening_tag = ''
                        while i < len(xml_content) and xml_content[i] not in ['>', ' ', '/']:
                            opening_tag += xml_content[i]
                            i += 1

                        if xml_content[i] == '/' and xml_content[i + 1] == '>':
                            # Self-closing tag
                            opening_tag = ''
                            i += 2  
                            continue # Skip the self-closing tag '/'

                        # validate Doctype declaration
                        if opening_tag.lower() == '!doctype':
                            opening_tag = ''
                            continue

                        stack.append(opening_tag)
                        root_element += 1

                    if root_element == 0:
                        root_element_count += 1
                else:
                    i += 1

            if stack:
                print ('Error: Found opening tag without matching closing tag:', stack.pop())
                error_message['Error 8'] = 'Error: Found opening tag without matching closing tag: ' + stack.pop()
                error = True
            if root_element_count != 1:
                print ('Error: Document does not contain root element')
                error_message['Error 9'] = 'Error: Document does not contain root element'
                error = True
                err_msg = error_message
            if error == True:
                return False, err_msg
            else:
                return True

# validate_xml(xml_content)
# print("Validation Status:", validate_xml())