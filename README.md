Twitch Chat PlayBack. The chat that is saved by my analysis tool gets opened by chatReplay, which cleans and animates it with emotes in a fluid, mobile-friendly, and visualized format.

  - scrolling at 60fps actuated based on time

  - text movement and size based on sentiment volume

# usage: chatvid.py [filename]

# chatReplay is queued in batches by "chathighlightqueue.py", once the desired clips have been selected in Adobe Premiere.

After some quality filters, similar messages within the same time of each other are merged together using levenshtein distance. Messages regardless of distance are used to correct each other.

In this iteration I chose to omit the usernames of the chatters due to 40%+ of my audience viewing on 5 inch screens.

The chat animation is synced with the origin livestream, to display the chat's interesting reaction to the stream. http://j.mp/pogchamp