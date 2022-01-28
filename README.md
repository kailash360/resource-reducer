# Resource Reducer

A resource Reducer for Android Strings

## How to run 

The `resource-reducer.py` is the only required file.

## How it works 

1. Configure the following varibales in the beginning of the script

    - VALID_FILES : All the file types to be considered
    - IGNORED_FILES : All the special files to be ignored
    - STRING_XML_FILE : Path of the `strings.xml` file
    - CURRENT_DIR : Path of the current directory (no need to configure this)
    - SUB_FOLDERS : List of all the sub-folders to be considered

2. Extracts all the ids from the `strings.xml` file, and creates a list of them

3. Loops through all the files of all the sub-folders and checks if any file contains any of the string ids 

4. If an id is found in any file in the above step, then it is removed from the list of ids. this finally keeps the list of unused ids. This list is then saved in a `unused.txt` file.

5. It asks the user if all the unused ids are to be deleted. If user prompts **y**, then it proceeds, otherwise the script closes.

6. It reads all the lines from the `strings.xml` file and generates a list, witch each line being an elemnt of the list. It then creates a list of the string tags whose id is used in the application. the list is finally written into `strings.xml` file which is the final output




