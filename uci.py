# -*- coding: utf-8 -*-
"""
UCI framework to allow use of these bots as a UCI engine.
"""

import logging
import sys
import traceback

import chess

from players import ALL_PLAYERS

def output(cmd):
    """Disable output buffering."""
    logging.debug("ENGINE: " + cmd)
    print(cmd, file=sys.stdout, flush=True)

class Engine(object):
    """A UCI engine that can communicate with a client."""

    def __init__(self):
        """Initial setup."""
        
        # Set up an internal board, ready for positions and moves.
        self.board = chess.Board()
        
        # All the commands that this engine might receive from the client.
        self.commands = {
                "uci": self.initialise_engine,
                "setoption": self.set_options,
                "ucinewgame": self.new_game,
                "isready": self.ready,
                "position": self.setup_position,
                "go": self.search,
                "stop": self.stop,
                "quit": sys.exit
                }
        
        self.current_player = None
        
        # In infinite mode the engine shouldn't return a move unless
        # explicitly told so with the "stop" command.
        self.infinite_mode = False
        
        # The best move to return - stored here for use in infinite mode.
        self.best_move = None

    def initialise_engine(self, *args):
        """Send init info and options, and tell the client we're ready."""
        output("id name Elephas")
        output("id author Philip Brien")
        playerstr = "option name Personality type combo default "
        
        # The default player is just the first one in the list.
        playerstr += ALL_PLAYERS[0].name
        for player in ALL_PLAYERS:
            playerstr += " var " + player.name
        output(playerstr)
        output("uciok")
    
    def set_options(self, cmdwords):
        """Set up which player we're using."""
        
        # The only option we currently allow is Personality, which selects
        # the appropriate Player.  Anything else should be ignored.
        if cmdwords[1] == "name" and cmdwords[2] == "Personality":
            playername = " ".join(cmdwords[4:])
            players = [p for p in ALL_PLAYERS if p.name == playername]
            if len(players) != 1:
                raise ValueError("Invalid player selected: {0}"
                                 .format(playername))
            
            # Initialise the player at this point.
            self.current_player = players[0]()
        else:
            pass
    
    def new_game(self, *args):
        """Do any processing ready to set up a new game."""
        self.board.reset()
        if self.current_player is not None:
            self.current_player.reset()
        else:
            # No player selected, so the client was fine with the default.
            # Initialise them here.
            self.current_player = ALL_PLAYERS[0]()

    def ready(self, *args):
        output("readyok")
    
    def setup_position(self, cmdwords):
        """Set up the provided position on the internal board."""
        # The "position" command always includes he parameter "moves", so find
        # this first.
        moves = cmdwords.index("moves")
        
        if cmdwords[1] == "startpos":
            self.board.reset()
        elif cmdwords[1] == "fen":
            # This is a board setup sent in FEN, so parse it into the board.
            # The FEN string consists of everything up to the word "moves".
            fenstring = " ".join(cmdwords[2:moves])
            self.board.set_fen(fenstring)
            
        # Now find all the moves in the string and play them into the board.
        for move in cmdwords[moves + 1:]:
            self.board.push_uci(move)
            
    def search(self, cmdwords):
        """Search for the best move to return."""
        
        # We ignore almost everything in the "go" command, because there's no
        # guarantee that any given Player implements it.  Most UCI clients
        # should cope with this.  In particular, pondering mode is not
        # supported - just ignore a ponder command.
        if "ponder" in cmdwords:
            pass
        
        self.best_move = self.current_player.take_turn(self.board).uci()
        
        if "infinite" in cmdwords:
            # In infinite mode, so don't return the recommendation yet.
            self.infinite_mode = True
        else:
            output("bestmove " + self.best_move)
            
    def stop(self):
        """Return the stored best move."""
        if self.infinite_mode:
            output("bestmove " + self.best_move)
        self.infinite_mode = False

    def input_loop(self):
        """Listen for input from the client and respond."""

        while True:
            cmdwords = sys.stdin.readline().strip().split(" ")
            logging.debug("CLIENT: " + " ".join(cmdwords))
            
            if cmdwords[0] in cmdwords:
                # This is a command we know about, so run the appropriate
                # function with the list of parameters.
                self.commands[cmdwords[0]](cmdwords)
            else:
                # We don't recognise this command, so ignore it.
                pass
        
if __name__ == "__main__":
    engine = Engine()
    logging.basicConfig(filename='elephas.log', 
                        format='%(asctime)s %(message)s',
                        level=logging.DEBUG)
    try:
        engine.input_loop()
    except:
        logging.debug(traceback.format_exc())
        raise