#---------------------------------------------------------------------------------#
#
# MODULE: defaults
#
# WRITTEN BY: Benjamin Pieczynski - 01/30/2024
#
# PURPOSE: Store global variables, help descriptions and argparse arguments.
#
# INPUTS: NONE
#
# OUTPUTS: NONE
#
#---------------------------------------------------------------------------------#

# imports
import argparse
import os

# Defaults
prog_name    = 'Fortran Makefile Builder'
exec_name    = 'for_make'
version      = 'v1.0.0'
full_name    = f'{prog_name} - {version}'
programmer   = 'Benjamin Pieczynski'
affiliate    = 'UCSD ASTRONOMY & ASTROPHYSICS'
release_date = '01-30-2024'
cwd          = os.getcwd()
description  = '''
                  PROGRAM: {}
                  VERSION: {}
                  RELEASE DATE: {}
                  
                  WRITTEN BY: {} - {}
                  
                  This python program reads fortran files and builds a basic 
                  makefile by reading dependencies from the fortran files. 
                  The program also asks the user for different options such 
                  as COMPILER option and for flags. The program does not 
                  provide advanced makefile options.'''.format(prog_name, 
                                                               version,
                                                               release_date, 
                                                               programmer, 
                                                               affiliate)

# Set Up Parser
parser = argparse.ArgumentParser(prog=exec_name, description=description,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

# Help Information
vhelp     = '''Display current program version number.'''
ns_help   = '''Flag to set no source(src) file directory.'''
no_help   = '''Flag to set no object(obj) file directory.'''
nf_help   = '''Flag to specify no make flags.'''
prog_help = '''Program directory (use '.' for current directory).'''

# Parser Arguments
parser.add_argument('-pd', '--program_directory',              default=cwd,       help=prog_help)
parser.add_argument('-ns', '--no_src',    action='store_true', default=False,     help=ns_help  )
parser.add_argument('-no', '--no_obj',    action='store_true', default=False,     help=no_help  )
parser.add_argument('-nf', '--no_mflags', action='store_true', default=False,     help=nf_help  )
parser.add_argument('-v',  '--version',   action='version',    version=full_name, help=vhelp    )
