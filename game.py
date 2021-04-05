# -*- coding: utf-8 -*-
"""
Python chess bot
"""

from players import Player

import chess
import chess.pgn

class Game(object):
    """A game of chess with defined players."""
    
    def __init__(self, white, black):
        """Set up a new game."""
        if not all([isinstance(p, Player) for p in (white, black)]):
            raise ValueError("Game must be set up with valid Players")
        self.players = {chess.WHITE: white,
                        chess.BLACK: black}
        self.board = chess.Board()
        
        # Reset both players here in case they already had internal state.
        white.reset()
        black.reset()
        
        # Result is semi-independent of the board state because players can
        # lose by submitting an invalid move. 
        self.result = None
        
        # PGN exporter - use this to export the game for later analysis.
        self.exportgame = chess.pgn.Game({"White": 
                                              self.players[chess.WHITE].name,
                                          "Black":
                                              self.players[chess.BLACK].name})
        
    def play(self):
        """Play out the game to its conclusion."""
        while not self.board.is_game_over():
            # Work out whose turn it is.
            to_play = self.players[self.board.turn]
            
            # Ask them to take their turn. Create a copy of the board for them 
            # to use in analysis (so that they can't manipulate this one).
            attempted_move = to_play.take_turn(self.board.copy())
            if attempted_move in self.board.legal_moves:
                self.board.push(attempted_move)
                self.exportgame.end().add_main_variation(attempted_move)
            elif (attempted_move == "CLAIMDRAW" and 
                  self.board.can_claim_draw()):
                # Draw successfully claimed.
                self.result = "1/2-1/2"
                break
            else:
                # Player attempted an illegal move or claimed a draw when it
                # wasn't legal to do so - they immediately default.
                if to_play is chess.WHITE:
                    self.result = "0-1"
                else:
                    self.result = "1-0"
                break
        
        if self.result is None:
            self.result = self.board.result()

    def export(self):
        """Export the full game as a PGN string."""
        self.exportgame.headers["Result"] = self.result
        exporter = chess.pgn.StringExporter(headers=True, 
                                            variations=True, 
                                            comments=True)
        return self.exportgame.accept(exporter)
        
