# LullabyPy
Discord music bot named Lullaby

## Current problems
1. Calling the save playlist command is supposed to save the playlist right that very moment. However, I can only copy the existing playlist instead of doing a deepcopy. While this should be enough to save the playlist, the saved playlist will change depending on the current list of songs that are being played.

For example, if I saved {A,B,C}, and then while listening to my songs I add songs {D,E,F}, the saved playlist has {D,E,F}. If I skip current song, the saved playlist also skips the current song.

This suggests that perhaps the saved playlist variable is referencing the actual playlist (via pointer). However, this should not be the case as I used the copy library to copy the original playlist insteda of assigning with "=". But who knows, code is weird sometimes. If anyone has a solution to this, please give me some suggestions so I can finish up this feature.

## I FOUND THE SOLUTION FOR IT
Although not implemented yet, instead of saving the playlist in a variable, I can save the songs in a text file. When the user runs the !loadsaved command, I will read the song names from those files and add them to the actual playlist. HOLY SHIT A GENIUS RIGHT HERE GUYS. However, since everything here is hosted on Heroku, contents of the file will be reset to its original form (the original contents during latest push) everyday (because Dyno cannot retain overwritten changes made after push).

A solution to this is to host the saved playlist file elsewhere (perhaps my computer localhost, idk man) but I will not care about this for now (until my users aka friends start complaining).
