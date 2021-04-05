# elephas
 Extendable chess engine for experimentation and computer chess tournaments
 
## Dependencies
Elephas requires Python 3 and [python-chess](https://pypi.org/project/chess/) 
(`pip install chess`). If you want to build an executable to use Elephas as a
UCI engine, you will also need [PyInstaller](https://www.pyinstaller.org/) 
(`pip install pyinstaller`).

## How to use it
Elephas can be used in two main ways - either as a framework for computer
chess tournaments, or as a UCI engine to connect to your favourite chess GUI 
(for example, [Lucas Chess](https://lucaschess.pythonanywhere.com/) or 
[Arena Chess GUI](http://www.playwitharena.de/)).

### Tournaments
Create your own chess engine by subclassing the `Player` object in players.py.
Override the `take_turn` function in your class and put all the relevant logic
in there. Elephas comes with three example players, with their own distinct
playing styles, which you can use as inspiration. Add any new players to the
ALL_PLAYERS list in players.py.

Once your players are all ready, you can run a tournament using the
`Tournament` class in tournament.py. Running this file as a script will run a
short round-robin tournament between all of the players in the ALL_PLAYERS
list. This is worth doing anyway because it will test your chess logic pretty
effectively.

### UCI engine
If you want to play against any of these players yourself, run build.py to
create an executable (tested only on Windows, but should theoretically work on
other platforms too) and point your favourite chess GUI at the resulting
executable (it should be in the new `dist` folder after the build completes).

Note that Elephas implements enough of the UCI protocol for a game, but not
enough to use it for analysis (it doesn't send any `info` messages to the
client and can't ponder on moves).

The built-in players all play very poor chess. You shouldn't have any 
difficulty beating them unless you are very much a beginner!

## Why "Elephas"?
It's the Latin word for elephant, which is apparently what the Romans sometimes
called their equivalent of the rook chess piece. Also, I like elephants.