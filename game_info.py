#!/usr/bin/env python
# encoding: utf-8
'''
game_info -- parses top games from metacritic

@author:     joao ascenso

@copyright:  2015 organization_name. All rights reserved.

@license:    GLPv3

@contact:    joaoricardoascenso@gmail.com
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from game_info.parser_server import GameParserServer
import traceback

__all__ = []
__version__ = 0.1
__date__ = '2015-04-13'
__updated__ = '2015-04-13'

DEBUG = 1

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_description = '''%s

  Created by joaoascenso on %s.
  
USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_description, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-s", "--shell", dest="shell", action="store_true", help="output to shell")
        parser.add_argument("-p", "--port", dest="port", type=int, default=8080, help="port to run the rest interface")
        parser.add_argument("-u", "--url", dest="url", type=str, default="http://www.metacritic.com/game/playstation-4", help="url to parse game information from")

        # Process arguments
        args = parser.parse_args()

        shell = args.shell
        port  = args.port
        url = args.url

        server = GameParserServer(port, url)
        server.parse()
        if shell:
            server.print_games()
        else: 
            server.serve_rest_api()
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG:
            traceback.print_exc()
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    sys.exit(main())
