# _*_ coding:utf8 _*_

'''
This software is licensed under the New BSD Licence.
*******************************************************************************
Copyright (c) 2013, Juliano Atanazio - juliano777@gmail.com
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

-        Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

-        Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

-        Neither the name of the Juliano Atanazio  nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*******************************************************************************
'''

import sys  # sys built-in library
import os  # os built-in library

# Show help function


def show_help(code_err):
    '''
    Function that shows the application usage and returns a code at exit.
    '''
    msg = '''
             Clean up PostgreSQL WAL archive files.

             Use {} ((--list | --remove) (directory or path) | --help)

             --list   List the files that can be deleted.

             --remove Remove the older xlog files that can be deleted.


             The second argument can be either a directory or simply the way
             for an archived xlog.
             If this second argument is a directory, all xlogs contained
             therein (including .backup files) will be deleted (--remove) or
             listed (--list).
             If the path to the archived xlog is this second parameter, which
             will be listed (--list) or removed (--remove) all xlogs older than
             it.
          '''
    print(msg.format(sys.argv[0]))
    sys.exit(code_err)

# Arguments


try:
    arg_1 = sys.argv[1]  # First argument
    arg_2 = sys.argv[2]  # Second argument

except:
    pass


# Arguments filtering


if ((len(sys.argv) == 1) or ((len(sys.argv) == 2) and (arg_1 != '--help')) or
   (len(sys.argv) > 4)):
    show_help(1)

if (arg_1 == '--help'):
    show_help(0)

elif ((len(sys.argv) > 2) and (arg_1 not in ('--list', '--remove'))):
    show_help(1)

else:
    pass


# List or Remove Function


def ls_or_rm(x, y):
    '''
    Function to list or  remove older WAL files from PostgreSQL archives.
    '''

    try:
        if (os.path.isdir(y)):
            directory = y
            bkp_files = [f for f in os.listdir(directory) if
                         f.endswith('.backup')]
            bkp_files.sort()
            ref_file = bkp_files[-1][0:24]
        else:
            directory = os.path.dirname(y)
            ref_file = os.path.basename(y)
            ref_file = ref_file[0:24]

    except Exception as e:
        print('{}\n{}'.format(Exception, e))

    files = [f for f in os.listdir(directory) if (f < ref_file)]

    if (x == '--list'):
        print('\nUnnecessary Files:\n')

        for file in files:
            print(file)

    else:
        print('\nRemoving the following files in {}:\n'.format(directory))
        for file in files:
            try:
                os.remove('{}/{}'.format(directory, file))
                print(file)

            except Exception as e:
                print('{}\n{}'.format(Exception, e))

# The main function


def main():
    '''
    Main function
    '''
    ls_or_rm(arg_1, arg_2)


# Test: If it is executed in command line

if __name__ == '__main__':
    main()
