#---------------------------------------------------------------------------------#
# 
# PROGRAM: Fortran Makefile Builder
# 
# WRITTEN BY: Benjamin Pieczynski - 01/30/2024
#
# PURPOSE: This python program reads fortran files and builds a basic makefile
#          by reading dependencies from the fortran files. The program also asks
#          the user for different options such as COMPILER option and for flags.
#          The program does not provide advanced makefile options.
#
# USE: python3 for_make [program_dir]
#
# INPUTS:
#
#       -pd     --program_directory (current by default)
#       -h      --help
#       -ns     --no_src (no source directory)
#       -no     --no_obj (no object directory)
#       -nf     --no_mflags (no make flags to be specified)
#
#---------------------------------------------------------------------------------#

# imports
import os
import time
from defaults import *
from fortran_reader import *
from mk_makefile import *

# main program
def main():
    
    # Create list of keys to the args dictionary
    args = parser.parse_args().__dict__
    
    # Read in arguments
    program_dir     = args['program_directory']
    no_src          = args['no_src'           ]
    no_obj          = args['no_obj'           ]
    no_mflags       = args['no_mflags'        ]
    
    print('-------------------------------------------------------------------')
    print('\nPROGRAM: {}\nVERSION: {}\nRELEASE DATE: {}\nWRITTEN BY: {} - {}\n'.format(prog_name, 
                                                                                     version, 
                                                                                     release_date, 
                                                                                     programmer, 
                                                                                     affiliate))
    print('-------------------------------------------------------------------\n')
    
    # argument handling
    if no_src == True:
        src_dir  = program_dir
        src_path = ''
    else:
        src_dir  = os.path.join(program_dir,'src')
        src_path = 'src/'
    if no_obj == True:
        obj_path = ''
    else:
        obj_path = 'obj/'
        
    # Compiler entry
    cond = False
    while cond == False:
        print('ENTER FORTRAN COMPILER')
        fc = str(input('FC: '))
        if len(fc) > 0:
            cond = True
            
    # Executable entry
    cond = False
    while cond == False:
        print('ENTER EXECUTABLE NAME')
        exec = input('EXEC: ')
        if len(exec) > 0:
            cond = True
    
    # Program flags
    if no_mflags == True:
        print('NO FLAGS SELECTED\n')
        flags = ''
    else:
        print('ENTER PROGRAM FLAGS')
        print('EXAMPLE: -O2 -w -m64 -Bdynamic -assume byterecl -openmp')
        flags = input('FLAGS: ')
        print()
    
    
    # Get list of target program files
    prog_files = find_fortran_files(src_dir)
    
    # Find dependencies in target program files
    src_map = {}
    for file in prog_files:
        file_path = os.path.join(src_dir,file)
        src_ref = src_path+file # src name as it will appear in makefile
        felem   = file.split('.')
        obj_ref = obj_path+felem[0]+'.o' # obj name as it will appear in the makefile
        src_map[src_ref] = {}
        src_map[src_ref]['obj_file'] = obj_ref
        src_map = find_dependencies(file_path, src_ref, src_map)
    
    print('Source Map')
    print(src_map, '\n')
    time.sleep(0.6)
    
    # build a map from modules to src map
    module_map = {}
    for key in src_map:
        src_map[key]['written'] = False
        module_map[src_map[key]['module_name']] = key
    
    print('Module Map') 
    print(module_map, '\n')
    time.sleep(0.6)
    
    # Call the function to build the makefile
    lines = build_makefile(fc, exec, flags, src_map, module_map, obj_path)
    write_makefile(program_dir, lines)
    return

############## CALL MAIN ###############
if __name__ == '__main__':
    main()