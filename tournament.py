# -*- coding: utf-8 -*-
"""
Automatic chess tournament using predefined players.
"""

from game import Game
from players import ALL_PLAYERS

import chess

# Tournament modes.
# In a round-robin tournament, everyone plays each other twice (White and 
# Black).
MODE_ROUNDROBIN = 1
# A multi-robin tournament has everyone play each other 2n times, where n is
# the number of entrants.
MODE_MULTIROBIN = 2

class Tournament(object):
    """A chess tournament."""
    def __init__(self, players=ALL_PLAYERS, mode=MODE_ROUNDROBIN):
        """Constructor - save these off."""
        self.players = [p() for p in players] # Instantiate the players here
        self.mode = mode
        self.games = []
        if mode == MODE_ROUNDROBIN:
            self.games = self.create_roundrobin()
        elif mode == MODE_MULTIROBIN:
            for _ in range(len(self.players)):
                self.games.extend(self.create_roundrobin())

    def create_roundrobin(self):
        games = []
        for player in self.players:
            opponents = [p for p in self.players if p != player]
            games.extend([Game(player, opp) for opp in opponents])
        return games
    
    def play(self):
        """Play all the scheduled games."""
        for game in self.games:
            game.play()
            
    def report(self):
        """Report the results."""
        scores = {p: 0 for p in self.players}
        for ix, game in enumerate(self.games):
            print("Game {0} ({1} vs {2}): {3}"
                  .format(ix + 1,
                          game.players[chess.WHITE].name,
                          game.players[chess.BLACK].name,
                          game.result))
            if game.result == "1-0":
                scores[game.players[chess.WHITE]] += 1
            elif game.result == "0-1":
                scores[game.players[chess.BLACK]] += 1
            else:
                scores[game.players[chess.WHITE]] += 0.5
                scores[game.players[chess.BLACK]] += 0.5
        
        print("\nOverall scores:")
        for player in sorted(scores, key=lambda x: scores[x], reverse=True):
            print("{0}: {1}".format(player.name, scores[player]))
            
    def export(self, index=None):
        """Export one or all the games in a single string of PGN format."""
        if index is not None:
            return self.games[index - 1].export()
        else:
            pgn = ""
            for game in self.games:
                pgn += game.export() + "\n\n"
            return pgn
        
if __name__ == "__main__":
    # Default behaviour when run as a script is to play a round-robin
    # tournament between all the players we know about.
    print("Playing a round-robin tournament between the {0} configured "
          "players...".format(len(ALL_PLAYERS)))
    tourn = Tournament()
    tourn.play()
    tourn.report()