#---------------------------------------------------------------------------------#
#
# MODULE: fortran_reader
#
# WRITTEN BY: Benjamin Pieczynski - 01/30/2024
#
# PURPOSE: Parse the fortran files to look for module dependencies. Dependencies
#          are specified in the fortran file by including '! MODULES' in the line
#          above the modules.
#
#---------------------------------------------------------------------------------#

# imports
import os
import time

# function to find the fortran files
def find_fortran_files(search_dir):
    print('SEARCHING FOR PROGRAM FILES')
    time.sleep(0.6)
    files_list = os.listdir(search_dir) # grab a list of all src directory files
    target_files = []
    for file in files_list:
        file_elements = file.split('.')
        if file_elements[0][-2:] == '_h': # indicates header file
            print(f'HEADER FILE: {file}')
            time.sleep(0.25)
        elif file_elements[1] in ['f90','f95','f', 'f77']:
            target_files.append(file)
            print(f'PROGRAM FILE: {file}')
            time.sleep(0.25)
        elif file_elements[1] == 'h':
            print(f'HEADER FILE: {file}')
            time.sleep(0.25)
        else:
            print(f'NON-PROGRAM FILE: {file}')
            time.sleep(0.25)
    print('\n')
    return target_files

# function to open fortran file, search for module line
def find_dependencies(filename, src_ref, src_map):
    '''filename = file path
       src_ref  = source file reference in makefile
       src_map  = dictionary for mapping'''
    # statements that will not be in module / program defining line
    dq_statements = ['END', '!', '=', 'CHARACTER', 'PRINT', 
                     'WRITE', 'CALL', 'CHAR']
    dependencies = [] # array to store dependencies
    next_line = False # Flag to find modules
    file = open(filename, 'r')
    print(f'SEARCHING FOR DEPENDENCIES: {src_ref}\n...')
    time.sleep(0.6)
    try:
        for line in file:
            if next_line == True:
                line = line.strip('\n')
                if 'use' in line.lower():
                    line = line.split()
                    if line[1][-1] == ',':
                        mod = line[1][:-1]
                    else:
                        mod = line[1]
                    dependencies.append(mod)
                    print(f'DEPENDENCY FOUND: {mod}')
                    time.sleep(0.25)
                else:
                    src_map[src_ref]['dependencies'] = dependencies
                    next_line = False # no more modules in section
                    break # stop search
            elif 'MODULE' in line.upper():
                dq_cond = False
                for dqs in dq_statements:
                    if dqs in line.upper():
                        dq_cond = True # disqualifying statement
                        break # break loop
                if dq_cond == False:
                    line = line.strip('\n')
                    line = line.split()
                    module_name = line[1]
                    src_map[src_ref]['module_name'] = module_name
            elif 'PROGRAM' in line.upper():
                dq_cond = False
                for dqs in dq_statements:
                    if dqs in line.upper():
                        dq_cond = True # disqualifying statement
                        break # break loop
                if dq_cond == False:
                    line = line.strip('\n')
                    line = line.split()
                    src_map[src_ref]['module_name'] = 'program'
            elif '! DEPENDENCIES' in line.upper():
                next_line = True # dependencies can be found in the next line
        # if no dependencies make note in module map
        if len(dependencies) == 0:
            src_map[src_ref]['dependencies'] = None
    except:
        print('MODULE FORMAT ISSUES')
    file.close()
    print()
    return src_map
