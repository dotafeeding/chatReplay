# only for @dotafeeding's personal use

# Twitch Chat PlayBack
#  - scrolling at 60fps actuated based on time
#  - text movement and size based on sentiment volume

# usage: chatvid.py [filename]
# Each line of chat is stored like this-> stream$user:message|chatTime
# This script is queued in batches by "chathighlightqueue.py", once the desired clips have been selected in Adobe Premiere.

#known issues: 
#extra large emotes abruptly cut off due to render time optimization of not rendering past 4 emotes

#output: f:/clipchat/[Clip Name]/[Frame Number].png 


#------
#Config

timeMergeDistance = 6.44			
timeMergeDistance = 99.95			
timeMergeDistance = 31.95			

timeMergeDistance = 7.44

#smaller merge intervals allow for more granular responses (great for when many events occur within a short space)
#large intervals are good for totaling response counts across the whole chat (great for when just one or few original thoughts appear in chat)

rightAlign = 1
#rightAlign = 0


msgLen = 22
msgLen = 69
#maximum length messages allowed


bannedphrase = ["d","albert","notatk"]#banned keywords

#-------


from PIL import Image, ImageDraw, ImageFont
import numpy, sys,os,time
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk	
from random import randint
from fuzzywuzzy import fuzz

scrollNeeded = 0
speed = 0
textHeight = 0
speeds=[]
end = 0

path = 'C:/Drive/Code/emotes'
emotes = []
for entry in os.scandir(path):
	entry = entry.name	
	emotes.append(entry.split(".")[0])
	
args = sys.argv

filename = 'f:/clipchat/' + args[1] + '/'
os.mkdir(filename)#runtime is broken if the directory already exists

with open("g:/clips/" + args[1]) as chatvid:
	chatvid = chatvid.readlines()
out = [x.strip() for x in chatvid]



blacklist = ["http","forsen","ᵃ","ᴇ","۞","⎠","📞","É","╣","tyler","sourpls","admiral","TOLI","","󀀀","贡","ȓ","񡠎","򬀀","ҏ"]


with open("D:/streamdata/helpers") as helpers:
	helpers = helpers.readlines()

helpers = [x.strip() for x in helpers]


for x in out:
	try:
		print(x)
		for y in blacklist:
			if y in x.lower():
				raise
	except:
		out.remove(x) #remove non utf-8 lines

mostPop={}
for chat in out:
	try:
		mostPop[chat.split(":")[1].split("|")[0]] +=1 
	except:
		mostPop[chat.split(":")[1].split("|")[0]] =1 
alreadyChecked = []
	
while True:
	breaker = 1
	try:
		for ch in out:
			if ch not in alreadyChecked:
				for ch2 in out:
					if ch.split(":")[0] ==  ch2.split(":")[0] and fuzz.ratio(ch.split(":")[1].split("|")[0].lower(),ch2.split(":")[1].split("|")[0].lower()) > 55 and ch != ch2:
						if mostPop[ch.split(":")[1].split("|")[0]] > mostPop[ch2.split(":")[1].split("|")[0]]:#remove similar message spam from the same user
							out.remove(ch2)
						else:
							out.remove(ch)
						raise
				alreadyChecked.append(ch)
	except:
		breaker = 0
		
		pass
	if breaker:
		break
mostPop = {}

print("spam removed")

for chat in out:
	try:
		mostPop[chat.split(":")[1].split("|")[0]] +=1 
	except:
		mostPop[chat.split(":")[1].split("|")[0]] =1 

alreadyChecked = []
			
		
while True:
	breaker = 1
	try:
		for ch in out:
			if ch not in alreadyChecked:
				for ranked in mostPop:
					if (fuzz.ratio(ch.split(":")[1].split("|")[0], ranked) > 83 or fuzz.token_sort_ratio(ch.split(":")[1].split("|")[0], ranked) > 95) and mostPop[ranked] > mostPop[ch.split(":")[1].split("|")[0]]:
						out.append(( ch.split(":")[0] + ":"+ranked + "|" + ch.split("|")[1] )) # rank the most common spellings. change extremely similar messages to use the most common spelling (misspelling correction) 
						out.remove(ch)
						raise
				alreadyChecked.append(ch)
				
	except:
		breaker = 0
		pass
				
	if breaker:
		break
alreadyChecked = []
			
print("corrections made")



while True:
	breaker = 1
	try:
		for ch in out:
			if ch not in alreadyChecked:
				for ch2 in out:						#merge identical messages, while displaying username list ranked by fastest reaction time, and counting unique users saying each unique message
					if ch.split("|")[0].split(":")[1].lower() == ch2.split("|")[0].split(":")[1].lower() and float(ch2.split("|")[1]) - float(ch.split("|")[1]) < timeMergeDistance and float(ch2.split("|")[1])-float(ch.split("|")[1]) >= 0 and ch != ch2:
						popCheck={}
						for chat in mostPop:
							if chat.lower() == ch.split(":")[1].split("|")[0].lower():
								popCheck[chat] = mostPop[chat]
						phrase = max(popCheck, key=popCheck.get)
						helper = ""
						helpSum = 0
						if ch2.split(":")[0] in helpers:
							helpSum += 1
							helper += ch2.split(":")[0] +", "
						if ch.split(":")[0] in helpers:
							helpSum += 1
							helper += ch.split(":")[0] + ", "
							
						if len( (ch.split(":")[0] + ", " +ch2.split(":")[0]) ) > 32 or "+" in ch.split(":")[0] or "+" in ch2.split(":")[0]:
							
							total = ch2.split(":")[0].count(",")
							total+= ch.split(":")[0].count(",")
							
							try:
								total += int(ch2.split(":")[0].split("+")[1])
							except:
								pass
							try:
								total += int(ch.split(":")[0].split("+")[1])
							except:
								pass
							if "," not in ch.split(":")[0]:
								total+= 1
							if "," not in ch2.split(":")[0]:
								total+= 1
								
							total -= helpSum
							
							if "+" in ch.split(":")[0]:
								out.append(( helper + ch.split("+")[0]  + "+" + str(total) + ":" +phrase + "|" + ch.split("|")[1] ))
							else:
								out.append(( helper + ch.split(":")[0]  + ", +" + str(total) + ":" +phrase + "|" + ch.split("|")[1] ))
						else:
							if ch.split(":")[0] in helper and ch2.split(":")[0] in helper or (ch.split(":")[0] not in helper and ch2.split(":")[0] not in helper):
								out.append(( ch.split(":")[0] + ", " +ch2.split(":")[0] +":" +phrase + "|" + ch.split("|")[1] ))
							elif ch.split(":")[0] in helper:
								out.append(( helper +ch2.split(":")[0] +":" +phrase + "|" + ch.split("|")[1] ))
							elif ch2.split(":")[0] in helper:
								out.append(( helper + ch.split(":")[0] +":" +phrase + "|" + ch.split("|")[1] ))
						
						out.remove(ch)
						out.remove(ch2)
						raise
				
				alreadyChecked.append(ch)
	except:
		breaker = 0
		pass
	if breaker:
		break
	
	
count = 0
frameskip = 0
chat = {}
for ch in out:
	if len(ch.split("|")[0].split(":")[1]) < 35:
		doit = 1
		for x in ch.split("|")[0].split(":")[1].split(" "):
			if x.lower() in bannedphrase:
				doit = 0
		if ch.split("|")[0].split(":")[1].lower() in bannedphrase:
			doit = 0
		if doit:
			try:
				chat[ch.split("|")[0].split("$")[1]] = float(ch.split("|")[1])
			except:
				chat[ch.split("|")[0]] = float(ch.split("|")[1])

currentLines = {}
cLcount = 0
interval = 0.322
chatTime = chat[min(chat,key=chat.get)] - interval+1
color = (0,0,0)
colorKey = "#00ff00"
colorLota = (255,255,255)
colorLotaBlue = (0,255,255)
height = int(1400/700 * 900)
W = 1400
H = int(1400/700 * 45)

shakeCooldown = {}
size = int(W / 700 * 35)
font = ImageFont.truetype('D:/streamdata/DINPro-Medium.otf', size)
emoteSize = int(W / 700 * 35)

pauselen = 45
pausedFrames = 0
while len(chat) > 0 or scrollNeeded > 20 or end < 40:
	chatTime += 1/60
	
	try:
		
		if chat[min(chat,key=chat.get)] - chatTime < interval:
			currentLines[cLcount] = (min(chat,key=chat.get).split(":")[0],min(chat,key=chat.get).split(":")[1])
			shakeCooldown[cLcount] = 0
			cLcount +=1
			chat.pop(min(chat,key=chat.get))
			textHeight += H
			scrollNeeded += H
	except:
		try:
			chat.pop(min(chat,key=chat.get))
		except:
			pass
		pass
	
	while height< -80:
		height = height + H
		currentLines.pop(min(currentLines))
	
	
	text = Image.new("RGBA",(W,textHeight+H))
	draw = ImageDraw.Draw(text)
	
	frameHeight = 0
	

	boostonce = 1
	draw13 = 0
	for line in currentLines:
		if draw13 < 25:
			outUser = currentLines[line][0]
			outMsg = currentLines[line][1]
			
			words = {}
			
			order = -1
			for word in outMsg.split(" "):
				order += 1
				w,h = draw.textsize(word, font=font)
				if word.lower() in emotes:
					w = emoteSize
					h = emoteSize
				words[order] = [word, w]
			totalWidth = 0
			
			spacing = W/700 *8
			
			while order !=-1:
				totalWidth += words[order][1]
				totalWidth += spacing
				order -=1
			widthsofar = 0
			order = 0
			
			intensity = 0
			
			if "+" in outUser:
				intensity = int(outUser.split("+")[1])
				cooldown = 1
				
				if intensity < 5 and shakeCooldown[line]>7:
					shake = 1
				elif intensity < 10 and shakeCooldown[line]>5:
					shake = 2
				elif intensity < 25 and shakeCooldown[line]>3:
					shake = 3
				elif intensity < 50 and shakeCooldown[line]>2:
					shake = 4
				elif intensity < 100 and shakeCooldown[line]>1:
					shake = 5
				elif intensity > 100:
					shake = 6
				else:
					cooldown =0
					
				if cooldown:
					shakeH = shake / randint(1,2)
					if randint(0,1):
						shakeH *= -1
						
					shakeW = shake / randint(1,2)
					if randint(0,1):
						shakeW *= -1
					
					x = randint(0,1)
				else:
					shakeW = 0
					shakeH = 0
				
				shakeCooldown[line] += 1
			else:
				shakeW = 0
				shakeH = 0
			
			while order != len(words):
				if words[order][0].lower() in emotes:
					emote = 'C:/Drive/Code/emotes/'
					emote += words[order][0].lower()
					emote+= '.png'
					try:
						emote = Image.open(emote, 'r')
						emote = emote.resize((emoteSize+intensity*3,emoteSize+intensity*3) ,Image.LANCZOS)
						if shakeW != 0 and shakeH !=0:
							emote = emote.rotate(int(randint(-1,1) * (shakeW * shakeH / 3) ), resample=Image.BILINEAR)
						text.paste(emote,( int( (W-totalWidth) *rightAlign  +widthsofar+int(shakeW) -intensity*3) ,0 +frameHeight+int(shakeH)),emote)
					except:
						print(words[order][0].lower() + " is an invalid emote image")
					widthsofar += emoteSize + 5
				else:
				
					#crude method of drawing an outer stroke
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW-2) ,4-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW+2) ,4-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW) ,4-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW) ,4-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW-1) ,4-1-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW+1) ,4-1-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW) ,4-2-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW) ,4-2-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW+1) ,4+1-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW-1) ,4+1-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW) ,4+2-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW) ,4+2-10+frameHeight+shakeH)), words[order][0], font=font, fill=color)
					
					draw.text( ( ( (((W-totalWidth) * rightAlign  )+widthsofar+shakeW) ,4-10+frameHeight+shakeH)), words[order][0], font=font, fill=colorLota )
					
					widthsofar += words[order][1]
					try:
						if words[order+1][1] not in emotes:
							widthsofar += spacing
					except:
						pass
				order += 1
			if scrollNeeded > 2000 and height < 0 and boostonce:
				boostonce = 0
				draw13 += 25
				
			frameHeight += H
			
			
	if scrollNeeded > 150:#speed changes on a curve
		speed = scrollNeeded/35
	elif scrollNeeded > 90:
		speed = scrollNeeded / 25
	elif scrollNeeded > 0:
		speed = scrollNeeded / 17
	else:
		speed = 0
	if speed > 9:
		speed = 9
		
		
	if pausedFrames == 0:
		speeds.append(speed)
		if len(speeds) > 120:
			speeds.remove(speeds[0])
		fSpeed = speed
		
		for speed in speeds:
			fSpeed = (fSpeed * .68) + (speed *.32) 
		speed = fSpeed
	
	if scrollNeeded > 2000 and height < 0:
		speed = 1000
	
	
	newFrame = Image.new("RGBA",(W,int(1400/700*1000)))
	height -= speed
	heyight = int(height)
	scrollNeeded -= speed
	newFrame.paste(text,(0,heyight))
	if len(chat) == 0:
		end += 1
	
	"""
	frameskip+=1
	if frameskip == 1:
		frameskip = 0
	"""
	count += 1
	newFrame.save(filename + str(count)+".png","png")