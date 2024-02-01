# Program: Fortran Makefile Builder v1.0.0 - 01/30/2024 
# Written By: Benjamin Pieczynski - UCSD Astronomy & Astrophysics


 PURPOSE: This python program reads fortran files and builds a basic makefile
          by reading dependencies from the fortran files. The program also asks
          the user for different options such as COMPILER option and for flags.
          The program does not provide advanced makefile options.

 USE: python3 for_make [program_dir]

 INPUTS:

       -pd     --program_directory (current by default)
       -h      --help
       -ns     --no_src (no source directory)
       -no     --no_obj (no object directory)
       -nf     --no_mflags (no make flags to be specified)

 USAGE:
	python3 for_make.py [-h] [-pd Program_Directory] [-ns] [-no] [-nf] [-v]

 IMPORTANT NOTES:
	The makefile builder only works for modern fortran (specifically designed
	for Fortran 90). The programs ability to build the makefile depends on
	the users formatting of python files.

	1.) Use '! DEPENDENCIES' above module declarations.
		- declares module and program dependencies

	2.) DO NOT include comments after program main or module name.
		- this effects the parsers ability to map modules.

	3.) Currently no library functionality, which has to be added manually.
