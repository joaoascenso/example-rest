# example-rest
This repo contains example code on a simple rest implementation to parse video game information from metacritic top games

this repo was only properly tested on fedore machine and vm, some pip packages might have to be installed from the correspondent yum rpm on some other system. Python devel might alo need to be installed.

#requirements
This program requires python 2.7 because of the argparse module

Python package requirements are provided in requirements.txt and can be installed with pip
$ pip install -r requirements.txt 

# Instalation
to install, simply run
$ python setup.py install

the executable should be available as a shell command

#usage
to execute simple run game_info.py, use -h for usage
-s to output to shell
-p to define rest port
-u to send the url from metacritic to parse

available REST endpoints are:
/
/games
/games/game_name

#tests
tests are run by py.test framework, to run install the dependecies on the txt and run:
$ py.test tests/test_parser_server.py -vvv
