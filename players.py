# -*- coding: utf-8 -*-
"""
Chess players (effectively plugins for the bot).
"""

import random

import chess

class Player(object):
    """A chess player.  All game logic should be in subclasses of this
    object."""
    
    # Player names can include spaces, but NO OTHER WHITESPACE.  Please keep
    # it ASCII-only.
    name = None
    def __init__(self):
        """Constructor.  Override this if your player needs extra parameters
        chosen at instantiation time, but make sure they do at least have a 
        name."""
        pass
        
    def take_turn(self, board):
        """Analyse the current board and return the move you want to take.
        The function must return a Move object that represents a valid move in
        this context, or the string "CLAIMDRAW" if they wish to claim a draw - 
        if the move is not valid or a draw is claimed when it isn't valid to do
        so, you instantly lose the game.  Note that players cannot offer draws.
        """
        
        # This example just plays the first valid move it finds.
        return [m for m in board.legal_moves][0]
    
    def reset(self):
        """If your player has any internal state that needs to be reset at the
        start of a game, do that here.  This function will be called whenever
        a new game begins."""
        pass
    
class RandyRandom(Player):
    """Randy Random picks a random move from the list of available moves."""
    
    name = "Randy Random"
    
    def take_turn(self, board):
        legal_moves = [m for m in board.legal_moves]
        return random.choice(legal_moves)

class Rhino(Player):
    """The Rhino is hyperaggressive and tries to take whatever it can.  It 
    doesn't much care for strategy and won't notice checkmates except by luck.
    """
    
    name = "The Rhino"
    
    def take_turn(self, board):
        # The Rhino might be aggressive but it's not stupid.  It only plays
        # legal moves.
        moves = {m: 0 for m in board.legal_moves}
        
        # Rate all the available moves depending on how aggressive they are.
        for move in moves:
            if board.gives_check(move):
                # Giving check is aggressive! We need a good bonus for that.
                moves[move] += 5
            if board.is_en_passant(move):
                # Pawn capture.  Not too shabby, even if en passant is weird.
                moves[move] += 1
            elif board.is_capture(move):
                # Captures are great.  Check what we would capture - the more
                # valuable the piece, the better.
                captured = board.piece_type_at(move.to_square)
                scores = {chess.PAWN: 1,
                          chess.KNIGHT: 3,
                          chess.BISHOP: 3,
                          chess.ROOK: 5,
                          chess.QUEEN: 9}
                moves[move] += scores[captured]
            
            # Moving forward is more aggressive than moving backwards or 
            # sideways, obviously.  Check which colour we're playing to work 
            # out which way is up.
            if board.turn == chess.WHITE:
                forward = (chess.square_rank(move.to_square) > 
                            chess.square_rank(move.from_square))
            else:
                forward = (chess.square_rank(move.to_square) < 
                           chess.square_rank(move.from_square))
            if forward:
                moves[move] += 1
        
        # Now that we have ratings for all the moves, pick the best.
        return sorted(moves.keys(), key=lambda x: moves[x], reverse=True)[0]
    
class FieldMarshal(Player):
    """The Field Marshal sends the little people out first to do his fighting.
    Decisive victory is good, but the main thing is that it's an absolute
    bloodbath.  But honourable.  Of course."""
    
    name = "Field Marshal"
    
    def take_turn(self, board):
        # Select only from the legal moves.  Would be dishonourable not to.
        moves = {m: 0 for m in board.legal_moves}
        
        # Rate the moves on a few criteria.
        for move in moves:
            # Try out the move and see if it's checkmate.  If so, just do that
            # straight away.  Decisive blow, what?
            board.push(move)
            if board.is_checkmate():
                return move
            else:
                board.pop()
            
            # Attacking another general?  Certainly not, sir.  Do not give 
            # check unless all of the enlisted men are off the field and can't
            # see us.
            our_pawns = [p for p in board.piece_map().values() 
                         if p.color == board.turn and 
                         p.piece_type == chess.PAWN]
            if board.gives_check(move) and len(our_pawns) > 0:
                moves[move] -= 10
            
            # Fighting is what the men do.  Not the officers unless we have to,
            # and certainly not women or his Majesty.
            scores = {chess.PAWN: 6,
                      chess.KNIGHT: 1,
                      chess.BISHOP: 1,
                      chess.ROOK: 1,
                      chess.QUEEN: -5,
                      chess.KING: -6}
            piece = board.piece_type_at(move.from_square)
            moves[move] += scores[piece] 
            
            if board.is_en_passant(move):
                # One of the enlisted, attacking in passing?  Seems a little
                # off to me, but I'll allow it.
                moves[move] += 4
            elif board.is_capture(move):
                # Good honest violence.  But try not to attack officers, what?
                # And good heavens, we don't attack women.
                captured = board.piece_type_at(move.to_square)
                moves[move] += scores[captured]

            # We move towards the enemy.  Only cowards retreat.  This means 
            # moving towards the far side of the board when they have at least
            # half their pieces, and towards the enemy king after that.
            enemy = chess.WHITE if board.turn == chess.BLACK else chess.BLACK
            move_rank_diff = (chess.square_rank(move.to_square) - 
                              chess.square_rank(move.from_square))
            move_king_diff = (chess.square_distance(board.king(enemy),
                                                    move.from_square) -
                              chess.square_distance(board.king(enemy),
                                                    move.to_square))
            enemy_pieces = [p for p in board.piece_map().values()
                            if p.color == enemy]
            if len(enemy_pieces) > 7:
                moves[move] += (move_rank_diff
                                if board.turn == chess.WHITE 
                                    else -move_rank_diff)
            else:
                moves[move] += 5 if move_king_diff > 0 else -5
                
            # Keep the enemy on their toes by being a little unpredictable.
            moves[move] += random.choice((-1, 0, 1))
        
        # Now make your move, sir.
        return sorted(moves.keys(), key=lambda x: moves[x], reverse=True)[0]

# New players should be added to this list so that they can be included in
# tournaments.    
ALL_PLAYERS = [RandyRandom, Rhino, FieldMarshal]