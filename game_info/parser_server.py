'''
Created on 13 Apr 2015

@author: joaoascenso
'''

from lxml import html
import requests
import json

from flask import Flask
from flask_restful import Resource, Api, abort
from requests.exceptions import MissingSchema


class Game(object):
        """
        defines a game instance and provides methods for
        sorting my score and helping on the json serialization
        """
        def __init__(self,name,score):
            """
            @param name: name of the game
            @param score: score by metacritic 
            """
            self.name = name
            self.score = score

        def __cmp__(self, other):
            """
            compare function, used for sorting
            """
            return cmp(self.score, other.score)

        def __eq__(self, other):
            """
            compare objects
            """
            if isinstance(other, str):
                return self.name.lower() == other.lower()
            elif isinstance(other, unicode):
                return self.name.lower() == other.lower()
            elif isinstance(other, Game):
                return self.name.lower() == other.name.lower()

        def __ne__(self, other):
            """
            compare objects
            """
            if isinstance(other, str):
                return self.name.lower() != other.lower()
            elif isinstance(other, unicode):
                return self.name.lower() != other.lower()
            elif isinstance(other, Game):
                return self.name.lower() != other.name.lower()

        def __str__(self):
            """
            string representation
            """
            return str(self.to_dict())

        def to_dict(self):
            """
            dictionary representation
            """
            return {
                    "title": self.name,
                    "score": self.score
                      }

        def __repr__(self):
            return json.dumps(self.to_dict())


class ParserServerError(Exception):
    '''
    Generic exception to raise and log different fatal errors.
    '''
    def __init__(self, msg):
        super(ParserServerError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg
class ParseError(ParserServerError):
    pass
class SearchError(ParserServerError):
    pass


class GameParserServer(object):
    '''
    classdocs
    '''

    def __init__(self, serving_port=8080, url="http://www.metacritic.com/game/playstation-4"):
        '''
        Constructor

        @param port: port to serve the rest interface on 
        @param url: url to parse game info from 
        '''
        self.headers = {'user-agent': 'game_info_parser/1.0.0'}
        self.url = url
        self.topgames = []
        self.port = serving_port

    def serve_rest_api(self, debug=True):
        """
        serve the rest endpoint using flask rest
        """
        app = Flask(__name__)
        api = Api(app)

        search_game = self.search_game
        games_to_list = self.games_to_list

        def abort_if_game_doesnt_exist(game):
            """
            404 if game not in top game list

            @param game: game to search 
            """
            if game.lower() not in self.topgames:
                    abort(404, message="Game {} doesn't exist".format(game), status=404)

        class Status(Resource):
            """
            status rest endpoint
            """
            def get(self):
                return {
                    'status': 200,
                    'message': "success"
                    }

        class Games(Resource):
            """
            game information rest endpoint
            """
            def get(self, game=None):
                if game is None:
                    return {
                        'status': 200,
                        'message': "success",
                        'data': games_to_list()
                    }
                else:
                    abort_if_game_doesnt_exist(game)
                    game = search_game(game)
                    return {
                        'status': 200,
                        'message': "success",
                        'data': game
                    }

        api.add_resource(Status, '/')
        api.add_resource(Games, '/games/', '/games/<string:game>/')

        app.run(debug=debug, port=self.port)

    def parse(self):#
        """
        parse the url
        """
        try:
            r = requests.get(self.url, headers=self.headers)
        except MissingSchema:
            raise SearchError("error retreiving data from url")
        if r.status_code != requests.codes.ok:
            raise ParseError("request not ok")
        tree = html.fromstring(r.text)
        # find games by its tag
        games_html = tree.find_class('wrap product_wrap')
        for game_html in games_html:
            self.topgames.append(
                Game(
                     game_html.find_class('product_title')[0].text_content(),
                     game_html.find_class('metascore_w')[0].text_content()
                ))

    def sorted_games(self, reverse=True):
        """
        returns a list of the parsed games, sorted by score

        @param reverse: whether to reverse the order of the sorting to bigger score->lower
        @return: sorted list of games, by score
        """
        return sorted(self.topgames, reverse=reverse)

    def search_game(self, game):
        """
        search for a game on the parsed game list

        @param game: game to search
        @return: returns game object for the search
        """
        try:
            return self.topgames[self.topgames.index(game)].to_dict()
        except ValueError, e:
            if self.debug:
                raise e
            raise SearchError("{} does not exist".format(game))

    def games_to_list(self):
        """
        returns a json comprensible list of our games
        """
        return [e.to_dict() for e in self.sorted_games()]

    def print_games(self):
        """
        prints list of parsed games
        """
        print json.dumps(self.games_to_list(), indent=4)
        