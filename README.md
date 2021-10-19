# LullabyPy
Discord music bot named Lullaby

## Future features
1. Allow individual saved playlists. Currently, there is only one saved playlist per server.

## Current problems
1. If I have to make changes to the bot, everyone's saved playlists will disappear. To deal with this, there are 2 ways:
    a. Declare the running and saved playlist outside of the actual cog (in the main player.py file maybe) so that when I make any adjustments to the cog, I can simply reload the cog without resetting the data.
    b. Setup a database that stores all the user's playlists (NoSQL MongoDB).

Since I absolutely cannot be arsed to make these changes at the moment I will not do it. If I do get complaints from my users (aka only my friends really) only then I will consider making these fixes. Until then, enjoy the bot as it is.
