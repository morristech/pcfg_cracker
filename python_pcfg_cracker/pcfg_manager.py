#!/usr/bin/env python3

########################################################################################
#
# Name: PCFG Manager
#  --Probabilistic Context Free Grammar (PCFG) Password Guessing Program
#
#  Written by Matt Weir
#  Backend algorithm developed by Matt Weir, Sudhir Aggarwal, and Breno de Medeiros
#  Special thanks to Bill Glodek for work on an earlier version
#  Special thanks to the National Institute of Justice and the NW3C for support with the initial reasearch
#  Huge thanks to Florida State University's ECIT lab where this was developed
#  And the list goes on and on... And thank you whoever is reading this. Be good!
#
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#
#  Contact Info: cweir@vt.edu
#
#  pcfg_manager.py
#
#########################################################################################

##--Including this to print error message if python < 3.0 is used
from __future__ import print_function
import sys
###--Check for python3 and error out if not--##
if sys.version_info[0] < 3:
    print("This program requires Python 3.x", file=sys.stderr)
    sys.exit(1)
    
import argparse
import os  ##--Used for file path information

#Custom modules
from pcfg_manager.file_io import load_grammar
from pcfg_manager.core_grammar import PcfgClass, print_grammar
from pcfg_manager.priority_queue import PcfgQueue
from pcfg_manager.ret_types import RetType
from pcfg_manager.cracking_session import CrackingSession


#########################################################################################
# Holds the command line values
# Also holds the default values if you don't want to enter them every time you run this
#########################################################################################
class CommandLineVars:
    def __init__(self):
        self.rule_name = "Default"
        #Debugging printouts
        #-They actually are initialized false under parse_command_line regardless of the value here
        self.verbose = False  
        self.queue_info = False

        
####################################################
# Simply parses the command line
####################################################
def parse_command_line(command_line_results):
    parser = argparse.ArgumentParser(description='PCFG_Cracker: Used to generate password guesses for use in other cracking programs')
    parser.add_argument('--rule','-r', help='The rule set to use. Default is \"Default\"',metavar='RULE_SET',required=False, default= command_line_results.rule_name)
    parser.add_argument('--verbose','-v', help='Verbose prints. Only use for debugging otherwise it will generate junk guesses',dest='verbose', action='store_true')
    parser.add_argument('--queue_info','-q', help='Prints the priority queue info vs guesses. Used for debugging',dest='queue_info', action='store_true')
    try:
        args=parser.parse_args()
        command_line_results.rule_name = args.rule
        command_line_results.verbose = args.verbose
        command_line_results.queue_info = args.queue_info
    except:
        return RetType.COMMAND_LINE_ERROR

    return RetType.STATUS_OK 

    
###################################################################################
# Prints the startup banner when this tool is run
###################################################################################
def print_banner(program_details):
    print('',file=sys.stderr)
    print ("PCFG_Cracker version " + program_details['Version'], file=sys.stderr)
    print ("Written by " + program_details['Author'], file=sys.stderr)
    print ("Sourcecode available at " + program_details['Source'], file=sys.stderr)
    print('',file=sys.stderr)
    return RetType.STATUS_OK  


####################################################################################
# ASCII art for displaying an error state before quitting
####################################################################################
def print_error():
    print('',file=sys.stderr)
    print('An error occured, shutting down',file=sys.stderr)
    print('',file=sys.stderr)
    print(r' \__/      \__/      \__/      \__/      \__/      \__/          \__/',file=sys.stderr)
    print(r' (oo)      (o-)      (@@)      (xx)      (--)      (  )          (OO)',file=sys.stderr)
    print(r'//||\\    //||\\    //||\\    //||\\    //||\\    //||\\        //||\\',file=sys.stderr)
    print(r'  bug      bug       bug/w     dead      bug       blind      bug after',file=sys.stderr)
    print(r'         winking   hangover    bug     sleeping    bug     whatever you did',file=sys.stderr)
    print('',file=sys.stderr)
    return RetType.STATUS_OK

  
##################################################################
# Main function, not that exciting
##################################################################
def main():
    
    ##--Information about this program--##
    program_details = {
        'Program':'pcfg_manager.py',
        'Version': '3.1.3 Beta',
        'Author':'Matt Weir',
        'Contact':'cweir@vt.edu',
        'Source':'https://github.com/lakiw/pcfg_cracker'
    }
       
     ##--Print out banner
    print_banner(program_details)
    
    ##--Parse the command line ---##
    command_line_results = CommandLineVars()
    if parse_command_line(command_line_results) != RetType.STATUS_OK:
        return RetType.QUIT
   
    ##--Specify where the rule file is located
    rule_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)),'Rules', command_line_results.rule_name)   
   
    ##--Initialize the grammar--##
    grammar = []
    ret_value = load_grammar(rule_directory, grammar)
    if ret_value != RetType.STATUS_OK:
        print ("Error loading the PCFG grammar, exiting",file=sys.stderr)
        print_error()
        return ret_value
 
    pcfg = PcfgClass(grammar)
    
    ##--Setup is done, now start generating rules
    print ("Starting to generate password guesses",file=sys.stderr)
    print ("Press [ENTER] to display a status output",file=sys.stderr)
    
    current_cracking_session = CrackingSession(pcfg = pcfg, verbose = command_line_results.verbose)
    current_cracking_session.run(print_queue_info = command_line_results.queue_info)
      
    return RetType.STATUS_OK
    

if __name__ == "__main__":
    main()
