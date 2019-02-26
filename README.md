# Treasure

A simple server which implements the Treasure card game. This server prioritizes simplicity 
and understandability, and lacks lots of features you would want in production. 


## The game
In this game, you and an opponent are competing for thirteen treasures, with point values ranging 1 to 13. Each round, a random treasure is displayed and then you and the opponent each choose a card from your hand, showing them at the same time. Whoever plays the higher card wins the treasure. If the two cards are euqal, nobody gets that treasure. There is one exception: a 1 beats a 13. Whoever has the most treasure points at the end wins. The server is (sometimes) running at treasure.chrisproctor.net. 

This project was developed as part of an [interface design assignment](http://beyondbitsandatoms.org/interface-design.html) in [Beyond Bits and Atoms](http://beyondbitsandatoms.org/), a course taught by Paulo Blikstein and his graduate scudents at Stanford and Teachers College. 

## Example clients
In addition to the server code, this repo contains three examples that might be useful if you're writing your own client:

- `treasure/client.py` is a command-line client that supports all the features of the server. You can log in and play against other opponents.
- `treasure/client_autoplay.py` is a simpler command-line client that only supports autoplay games. Instead of waiting for other players, the player always plays against the bot.
- `treasure/example_client.py` is an example of how the command-line client can be extended to provide a new interface.
