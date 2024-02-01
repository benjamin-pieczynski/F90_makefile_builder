#---------------------------------------------------------------------------------#
#
# MODULE: mk_makefile
#
# WRITTEN BY: Benjamin Pieczynski - 01/30/2024
#
# PURPOSE: Responsible for building makefile through different logical expressions.
#
#---------------------------------------------------------------------------------#

# imports
import os
import time

# make the lines for the makefile using logical expressions
def build_makefile(fc, exec, flags, src_map, module_map, obj_path):
    '''FC         = fortran compiler
       EXEC       = executable
       flags      = compiler flags
       src_map    = source file map
       module_map = module to source map
       obj_path   = path to object files'''
    
    print('BUILDING MAKEFILE LINES\n...\n')
    time.sleep(0.5)
    mk_lines = [] # each line within the makefile
    
    # Initial lines
    mk_lines.append('# Disable the default rules\n')
    mk_lines.append('MAKEFLAGS += --no-builtin-rules --no-builtin-variables\n')
    mk_lines.append('\n')
    mk_lines.append(f'FC = {fc}\n')
    mk_lines.append('\n')
    mk_lines.append(f'FLAGS = {flags}\n')
    mk_lines.append(f'EXEC = {exec}\n')
    mk_lines.append('\n')
    
    # Object lines
    n = 0 # counter
    n_max = len(src_map)
    for obj in src_map:
        obj = src_map[obj]['obj_file']
        if n == 0:
            mk_lines.append(f'OBJS = {obj} \\\n')
        elif n < n_max-1:
            mk_lines.append(f'       {obj} \\\n')
        else:
            mk_lines.append(f'       {obj}\n')
        n+=1
    
    # Executable line
    mk_lines.append('\n$(EXEC): $(OBJS)\n\t$(FC) $(FLAGS) -o $@ $^\n')
    mk_lines.append('\n')
    
    # Build based off of dependencies
    print('SOLVING DEPENDENCIES\n...')
    time.sleep(0.6)
    solved = False # have all dependencies been solved?
    while solved == False: # continue until all dependencies have been solved
        n_false = 0
        for key in src_map:
            obj_f = src_map[key]['obj_file'] # object file for this key
            if src_map[key]['written'] == False: # if the obj has not been created / solved
                mk_dependencies = src_map[key]['dependencies']
                if mk_dependencies == None: # Build the file if it has no dependencies
                    mk_lines.append(f'{obj_f}: {key}\n')
                    mk_lines.append('\t$(FC) $(FLAGS) -c -o $@ $<\n\n')
                    src_map[key]['written'] = True # dependency solved
                    print(f'SOLVED: {key}')
                    time.sleep(0.25)
                else:
                    dep_objs = [] # object files containing dependent modules
                    for mod in mk_dependencies:
                        dep_src  = module_map[mod]
                        dep_obj  = src_map[dep_src]['obj_file']
                        status   = src_map[dep_src]['written']
                        if status == False: # dependent object has not been created
                            n_false += 1 # an unsolved dependency exists
                            status = False
                            break # dependency creation fails
                        else:
                            status = True
                            dep_objs.append(dep_obj)
                    if status == True:
                        d_obj_str = ' '.join(dep_objs) # string of file dependent object files
                        mk_lines.append(f'{obj_f}: {key} {d_obj_str}\n')
                        mk_lines.append('\t$(FC) $(FLAGS) -c -o $@ $<\n\n')
                        src_map[key]['written'] = True # success
                        print(f'SOLVED: {key}')
                        time.sleep(0.25)
        if n_false == 0: # reach the end and no false files are found
            solved = True
            print('MAKEFILE SOLVED!')
            time.sleep(1)
                    
    # clean and mrproper
    mk_lines.append(f'clean:\n\trm -rf {obj_path}*.o {obj_path}*.mod *.mod\n')
    mk_lines.append('mrproper: clean\n\t rm -rf $(EXEC)')
    print()
    return mk_lines

# write the makefile
def write_makefile(program_dir, lines):
    print('WRITING MAKEFILE')
    fname = os.path.join(program_dir, 'Makefile')
    f = open(fname, 'w')
    for line in lines:
        f.write(line)
    f.close()
    time.sleep(0.25)
    print(f'MAKEFILE WRITTEN: {program_dir}/Makefile')
    return