Twitch Chat PlayBack. The chat saved by my analysis tool gets opened by chatReplay, which cleans and animates it with emotes in a fluid, mobile-friendly, and activity-visualized format.

  - scrolling at 60fps actuated based on time

  - text movement and size based on sentiment volume
  
  - similar messages near each other are merged
  
  - quality filters and correction

usage: chatvid.py [filename]

chatReplay is queued in batches by "chathighlightqueue.py", once the desired clips have been selected in Adobe Premiere.

In this latest version I chose to omit the usernames of the chatters due to 40%+ of my audience viewing on 5 inch screens.

# The chat animation is synced with the origin livestream, to display the chat's interesting reaction to the stream. http://j.mp/pogchamp