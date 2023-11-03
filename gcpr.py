#!/bin/python3

import os
import subprocess
import glob
import sys
import re
import glob
from utils import ask_yes_no_question

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

SOURCE_EXTENSIONS = [
    "c",
    "cpp",
]

HEADER_EXTENSIONS = [
    "h",
]

# Flags
FLAG_PREFIX = '-'
FLAG_MAX_LEN = 2
# FLAG_ACCEPT_ALL = 'y'
FLAG_HELP = 'h'
# Define a regular expression pattern to match the -o=<file_name> pattern
FLAG_EXE_FILE_PATTERN = r'-o=([^\s]+)'
FLAG_EXE_FILE = 'o'
FLAG_EXE_FILE_SET = '='
FLAG_SAVE_EXE_AFTER_RUN = 's'
FLAG_SAVE_OUTPUT_AFTER_RUN = 'so'
FLAG_NO_RUN = 'nr'
FLAG_INTERACTIVE = 'i'

DOT = '.'

INCLUDE_ALL_FILES = '*'

DEFAULT_EXE_FILE_NAME = 'program'
DEFAULT_OUTPUT_FILE_NAME = 'output.txt'
MAIN_PY = 'gcpr.py'

PROJECT_NAME = 'Gcc/G++ Compile Plus Run'
COMMAND_MAIN = 'gcpr'

# Messages
MESSAGE_USAGE = f"Usage: {COMMAND_MAIN} [options] files..."
MESSAGE_HELP = f'''{MESSAGE_USAGE}

Optitons:
    -h              Show this help message
    -i              Interactive compilation
    -nr             No Running after Compilation (only compile)
    -o=<file>       Set executable file name (default: '{DEFAULT_EXE_FILE_NAME}')
    -s              Save executable file
    -so             Save output file (compilation running output contents, default: '{DEFAULT_OUTPUT_FILE_NAME}')
    
Examples:
    {COMMAND_MAIN} -h
    {COMMAND_MAIN} -s -o=run_me *.c
    {COMMAND_MAIN} -y -nr main.cpp utils.cpp
'''
MESSAGE_ERROR = 'Error: Unexpected Error Occurred'
MESSAGE_OK = 'Ok'

CODE_ERROR = 1
CODE_OK = 0

# Compilations     type out in
COMPILATION_C   = 'gcc'
COMPILATION_CPP = 'g++'
COMPILATIONS = {SOURCE_EXTENSIONS[0]: COMPILATION_C, SOURCE_EXTENSIONS[1]: COMPILATION_CPP}


def raise_msg(msg: str, code: int, color: bool = True, exit: bool = False) -> None:
    # Print a message and optionally exit the program

    if (code == CODE_ERROR):
        if color:
            print(f'{bcolors.BOLD}{bcolors.FAIL}{msg if msg else MESSAGE_ERROR}{bcolors.ENDC}{bcolors.ENDC}')
        else:
            print(f'{msg if msg else MESSAGE_ERROR}')
        sys.exit(CODE_ERROR)
    elif (code == CODE_OK):
        if color:
            print(f'{bcolors.BOLD}{bcolors.OKGREEN}{msg if msg else MESSAGE_OK}{bcolors.ENDC}{bcolors.ENDC}')
        else:
            print(f'{msg if msg else MESSAGE_OK}')            
        if exit:
            sys.exit(CODE_OK)
    

def get_executable_file_name(argv: list) -> str:
    # Process the given executable file name from the user or set to default

    executable_filename = DEFAULT_EXE_FILE_NAME

    for a in argv:
        # Use re.search to find the first match of file executable pattern
        match = re.search(FLAG_EXE_FILE_PATTERN, a)
        if (match):
            executable_filename = match.group(1)

    return executable_filename

def get_files_data(argv: list, flags: list) -> (list, str):
    # Get all the given files
    # Check if all the files have the same extension and return the extension accordingly

    files = []
    extensions = []
    extension = ''

    include_all_files_extension = ''

    for f in argv:
        f_parts = f.split(DOT)
        f_parts_len = len(f_parts)
        # Check if file has extension
        if (f_parts_len <= 1):
            raise_msg(f"Error: File '{f}' doesn't have an extension.", CODE_ERROR)
        f_extension = f_parts[f_parts_len - 1]
        # Check if file extension is allowed
        if (not f_extension or f_extension not in SOURCE_EXTENSIONS):
            raise_msg(f"Error: '{f}' file extension is not allowed.", CODE_ERROR)

        # Check if user want to include all files with the given extension
        if (INCLUDE_ALL_FILES in f):
            include_all_files_extension = f_extension
            break

        extensions.append(f_extension)
        # Check if all extensions are the same
        if (extensions and not all(e == extensions[0] for e in extensions)):
            raise_msg(f"Erorr: Not all file extension are the same.", CODE_ERROR)
        
        # Append file (check interactive option)
        if (FLAG_INTERACTIVE not in flags):
            files.append(f)
            continue
        if (ask_yes_no_question(f"Include {bcolors.BOLD}{bcolors.OKCYAN}{f}{bcolors.ENDC}{bcolors.ENDC} in the compilation?", default_answer=True)):            
            files.append(f)

    # Include all files with extension
    if (include_all_files_extension):
        files = []
        all_extension_files = glob.glob(f'./*.{f_extension}')
        extension = include_all_files_extension

        if (FLAG_INTERACTIVE in flags):
            for f in all_extension_files:
                # Append file
                if (ask_yes_no_question(f"Include {bcolors.BOLD}{bcolors.OKCYAN}{f}{bcolors.ENDC}{bcolors.ENDC} in the compilation?", default_answer=True)):
                    files.append(f)
        else:
            files = all_extension_files
    
    if (not len(files) > 0):
        raise_msg('Error: No files.', CODE_ERROR)

    if extensions:
        extension = extensions[0]
    

    return (files, extension)


def main_compilation(files: list, extension: str, executable_filename: str, flags: list):
    # Compile the given files with the given flags

    raise_msg(f"Compiling {bcolors.BOLD}{bcolors.OKCYAN}{len(files)}{bcolors.ENDC}{bcolors.ENDC} files...", CODE_OK, color=False, exit=False)

    compile_command = [COMPILATIONS[extension], *files, f'{FLAG_PREFIX}{FLAG_EXE_FILE}', executable_filename]
    # Run the compilation
    compilation_res = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if (compilation_res.returncode == CODE_OK):
        raise_msg("Compilation Successful!", CODE_OK)
    else:
        raise_msg(f"{compilation_res.stderr}\nCompilation Failed. Exiting...", CODE_ERROR)

    # Run executable file
    if (FLAG_NO_RUN not in flags):
        raise_msg("Running...", CODE_OK)
        # Check if executable file exists
        if (not os.path.exists(executable_filename)):
            raise_msg("Error: Executable File not found.", CODE_ERROR)
        run_command = [f'./{executable_filename}']
        run_res = subprocess.run(run_command, shell=True)

        if (run_res.returncode == CODE_OK):
            raise_msg("Done!", CODE_OK)
        else:
            raise_msg("Failed.", CODE_ERROR)

    # Save executable file
    if (FLAG_SAVE_EXE_AFTER_RUN not in flags):
        if (not os.path.exists(executable_filename)):
            raise_msg("Error: Executable File not found.", CODE_ERROR)
        os.remove(executable_filename)
    else:
        raise_msg(f"Saved Executable File! Executable File: {bcolors.OKCYAN}'{executable_filename}'{bcolors.ENDC}", CODE_OK)

    # Save output file
    if (FLAG_SAVE_OUTPUT_AFTER_RUN in flags):
        if (os.path.exists(DEFAULT_OUTPUT_FILE_NAME) and
            ask_yes_no_question(f"Found {bcolors.BOLD}{bcolors.OKCYAN}{DEFAULT_OUTPUT_FILE_NAME}{bcolors.ENDC}{bcolors.ENDC} do you want to overwrite it?", default_answer=True)):
            with open(DEFAULT_OUTPUT_FILE_NAME, 'w') as output_file:
                output_file.write(compilation_res.stdout)
            raise_msg(f"Saved Output File! Output File: {bcolors.OKCYAN}'{output_file}'{bcolors.ENDC}", CODE_OK)



def main():
    print(f"{bcolors.BOLD}{bcolors.WARNING}{PROJECT_NAME}{bcolors.ENDC}{bcolors.ENDC}")

    argv = sys.argv

    # Get flags
    flags = [i for i in argv if FLAG_PREFIX in i and len(i) <= len(FLAG_PREFIX) + FLAG_MAX_LEN]

    # Get executable file name
    executable_filename = get_executable_file_name(argv)

    # Remove flags from argv
    argv = list(filter(lambda i: i not in flags and executable_filename not in i, argv))
    # Remove FLAG_PREFIX from flags
    flags = list(map(lambda i: i.replace(FLAG_PREFIX, ''), flags))

    # Show help message if HELP_FLAG
    if (FLAG_HELP in flags or len(argv) <= 1):
        raise_msg(MESSAGE_HELP, CODE_OK, color=False, exit=True)

    # Get files and extension
    files, extension = get_files_data(argv[1:], flags)

    main_compilation(files, extension, executable_filename, flags)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise_msg("\nError: KeyboardInterrupt", CODE_ERROR)
