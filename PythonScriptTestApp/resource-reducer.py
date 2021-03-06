from calendar import c
import os
import datetime
import xml.etree.ElementTree as ET
now = str(datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))

# Path of current folder
CURRENT_DIR = os.path.dirname(__file__)

# Path of strings.xml file
STRING_XML_FILE = os.path.join(os.path.dirname(__file__),'app\\src\\main\\res\\values\\strings.xml')

# All valid file types to be considered for checming
VALID_FILES = ['xml','txt','java','kt']

# All the special files to be ignored in checking
IGNORED_FILES = ['strings.xml','unused.txt']

# All the folders to be ignored
IGNORED_FOLDERS = ['build','gradle','.gradle']

# Function to list all the subfolders
def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir() and f.name not in IGNORED_FOLDERS]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

# List of subfolder in current folder,to be considered for checking
SUB_FOLDERS = fast_scandir(CURRENT_DIR)

# Attribute to be used from string tag 
ATTRIBUTE = 'name'

# Name of the file to be generated for storing unused ids
UNUSED_FILE = f"unused-{now}.txt"

try:
    # path to the strings.xml file
    tree = ET.parse(STRING_XML_FILE)
    root = tree.getroot()

    # fetch all the ids from xml
    string_ids = []
    for item in root:
        string_ids.append(item.attrib[ATTRIBUTE])

    print("All string ids are: ",string_ids)

    # function to check if a given text is present in any file
    def stringExists(filename,text):
        
        # Read the content of the file and check if the string exists
        with open(filename) as f:
            fileContent = f.read()
            
            check1 = f"R.string.{text}" in fileContent
            check2 = f"@string/{text}" in fileContent
            check3 = f"@string//{text}" in fileContent
            return check1 or check2 or check3
        
    # function to extract a file type
    def fileType(filename):
        return filename.split(".")[-1]


    # loop through all the files and subdirectories

    print("\nParsing through all files and sub-folders")
    # loop through all the sub-folders and get the index of used string IDs
    used_string_indices = []
    for subFolder in SUB_FOLDERS:
            
        # get the path  of current folder
        currentFolder = os.path.join(os.path.dirname(__file__), subFolder)
        
        print("\tParsing ",currentFolder)
        
        # loop through all the files of the current folder
        all_files = os.listdir(currentFolder)
        for filename in all_files:
        
            # don't consider if the file is strings.xml or invalid type
            if (filename in IGNORED_FILES) or (fileType(filename) not in VALID_FILES) : continue
            
            # get the path of the current file
            filePath = os.path.join(currentFolder, filename)
            
            # if it is a directory, then don't consider
            if os.path.isdir(filePath): continue
            
            print("\t\tParsing ",filename)
            
            # loop over all the string ids
            for index in range(len(string_ids)):
                            
                # check if the string exists in the current file
                id = string_ids[index]
                isPresent = stringExists(filePath,id)
                
                # if string exists then add to the array of used indices
                if isPresent:
                    used_string_indices.append(index)

    print("All files parsed successfully")

    # update the string_ids to keep only the saved string_ids
    # string_ids = [string_ids[i] for i in range(len(string_ids)) if i not in used_string_indices]
    temp = []
    for i in range(len(string_ids)):
        if i not in used_string_indices:
            temp.append(string_ids[i])
    string_ids = temp

    # save the list of unused string ids in a file
    with open(UNUSED_FILE, 'w') as unused_string_ids:
        
        # first line of the file is the path of the strings.xml file used
        strings_file = f"File: {STRING_XML_FILE}\n\n"
        
        # final content to be written within the file
        finalContent = strings_file + '\n'.join(string_ids)
        unused_string_ids.write(finalContent)
        
    print("Unused ids have been listed in unused.txt successfully")

    # display the list of unused string ids
    # and ask user if he wants to remove them

    print("LIST OF UNUSED STRING IDs ARE: \n", string_ids)
    print("\nDO YOU WANT TO DELETE ALL THESE IDS FROM strings.xml FILE?")
    choice = input("Enter y for yes, any other key to abort:")

    if(choice == "y"):
        
        used_string_ids = []
        
        # open the xml file
        with open(STRING_XML_FILE,'r') as xmlfile:
            
            # read the xml content       
            xmlContent = xmlfile.readlines()
            
            #iterate over all the liens
            for index in range(len(xmlContent)):
                
                # ignore if the element is not a string 
                if '</string>' not in xmlContent[index]: 
                    used_string_ids.append(xmlContent[index])
                    continue
                
                #create a node from the string
                node = ET.fromstring(xmlContent[index].rstrip('\n').strip())
                
                # if id of node not in list of unused string ids
                # then add it to the list of final string ids
                if node.attrib[ATTRIBUTE] not in string_ids:
                    used_string_ids.append(xmlContent[index])
            
        # save the list of used string ids in strings.xml
        with open(STRING_XML_FILE,'w') as xmlfile:
            xmlfile.write(''.join(used_string_ids))
        
        print("strings.xml has been modified successfully")

    print("Thank you")

except Exception as e:
    print("Error:",e)


        