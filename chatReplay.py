#Chat Message Summary Display. scrolling actuated based on time
#writes chat video and alpha mask video 
# usage: chatvid.py [filename]
#output: d:/chatanimation/[filename].mp4 x264 

from PIL import Image
from PIL import ImageDraw, ImageFont
import cv2, numpy, sys,os,time
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk	
try:
	args = sys.argv
	filename= str(args[1])
except:
	print("Usage: [output file name]")
	sys.exit

rightAlign = 1
#rightAlign = 0

updateInterval = 60 * 0.322
interval = updateInterval/60
color = (0,0,0)
colorKey = "#00ff00"
colorLota = (255,233,0)
colorLotaBlue = (0,255,255)
height = 900
W,H = 700,100

frames = []
oldNames = []
frame= 0
scrollNeeded = 0 # pixels needed to scroll up
speed = 0
textHeight = 0
text = Image.new("RGBA",(W,100))
speeds=[]
lastPause =0.0
end = 0
scrollPause = []
intervalCheck = 0
path = 'C:/Drive/Code/emotes'
emotes = []
for entry in os.scandir(path):
	entry = entry.name	
	emotes.append(entry.split(".")[0])
	
with open("d:/streamdata/chatvid") as chatvid:
	chatvid = chatvid.readlines()
chatvid = [x.strip() for x in chatvid]
#user:message|chatTime
chat = {}
for ch in chatvid:
	chat[ch.split("|")[0]] = float(ch.split("|")[1])

chatTime = chat[min(chat,key=chat.get)] - interval+1
	
path = 'D:/streamdata/chatanimation'
for entry in os.scandir(path):
	entry = entry.name
	oldNames.append(entry[:-4])
	
	
nameCount = 2	
while filename in oldNames:
	if nameCount != 2:
		filename = filename[:-len(numappend)]
	numappend = "(" + str(nameCount) + ")"
	nameCount += 1
	filename += numappend
	
filename = 'd:/streamdata/chatanimation/' + filename
	
with open(filename,"w") as chatBackup:
	for ch in chatvid:
		chatBackup.write(ch + "\n")	
		
for ch in chatvid:
	chat[ch.split("|")[0]] = float(ch.split("|")[1])
filename += '.mp4'

video = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*"X264"),60,(700,1000))
filename += ".key.mp4"
video2 = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*"X264"),60,(700,1000))


while len(chat) > 0 or scrollNeeded > 20 or end < 800:
	if frame - intervalCheck >= updateInterval:
		intervalCheck = frame
		chatTime += interval
	try:
		if chat[min(chat,key=chat.get)] - chatTime < interval:
			outUser = min(chat,key=chat.get).split(":")[0]
			outMsg = min(chat,key=chat.get).split(":")[1]
			#words = order : [word, width]
			words = {}
			size = 60
			addtext = Image.new("RGBA",(W,H))
			draw = ImageDraw.Draw(addtext)
			
			font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
			order = -1
			for word in outMsg.split(" "):
				order += 1
				w,h = draw.textsize(word, font=font)
				if word.lower() in emotes:
					w = 69
					h = 69
				words[order] = [word, w]
			totalWidth = 0
			
			spacing = 19#px
			
			while order !=-1:
				totalWidth += words[order][1]
				totalWidth += spacing
				order -=1
			widthsofar = 0
			order = 0
			while order != len(words):
				if words[order][0].lower() in emotes:
					emote = 'C:/Drive/Code/emotes/'
					emote += words[order][0].lower()
					emote+= '.png'
					try:
						emote = Image.open(emote, 'r')
						emote = emote.resize((69,69) ,Image.LANCZOS)
						addtext.paste(emote,( ( (713-totalWidth) *rightAlign  +widthsofar ) ,0 ),emote)
					except:
						print(words[order][0].lower() + " is an invalid emote image")
					widthsofar += 69 + 5
				else:
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar-4) ,4-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar+4) ,4-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar) ,4-4-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar) ,4+4-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar-1) ,4-3-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar-3) ,4-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar-3) ,4+3-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar) ,4-2-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar) ,4-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar) ,4+2-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar+2) ,4-1-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar+2) ,4-10)), words[order][0], font=font, fill=color)
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar+2) ,4+1-10)), words[order][0], font=font, fill=color)
					
					draw.text( ( ( (((713-totalWidth) * rightAlign  )+widthsofar) ,4-10)), words[order][0], font=font, fill=colorLota )
					widthsofar += words[order][1]
					try:
						if words[order+1][1] not in emotes:
							widthsofar += 19
					except:
						pass
				order += 1
			
			w,h = 1000,1000
			size = 20
			font = ImageFont.truetype('D:/streamdata/DINPro-Bold.otf', size)
			w,h = draw.textsize(outUser, font=font)
			
			
			
			
			
			#draw.text( ( ( (((692-w) * rightAlign  )+4-2) ,68)), outUser, font=font, fill=color)
			#draw.text( ( ( (((692-w) * rightAlign  )+4+2) ,68)), outUser, font=font, fill=color)
			#draw.text( ( ( (((692-w) * rightAlign  )+4) ,68-2)), outUser, font=font, fill=color)
			#draw.text( ( ( (((692-w) * rightAlign  )+4) ,68+2)), outUser, font=font, fill=color)
			draw.text( ( ( (((692-w) * rightAlign  )+4-1) ,68-1)), outUser, font=font, fill=color)
			draw.text( ( ( (((692-w) * rightAlign  )+4-1) ,68)), outUser, font=font, fill=color)
			draw.text( ( ( (((692-w) * rightAlign  )+4-1) ,68+1)), outUser, font=font, fill=color)
			draw.text( ( ( (((692-w) * rightAlign  )+4) ,68-1)), outUser, font=font, fill=color)
			draw.text( ( ( (((692-w) * rightAlign  )+4) ,68)), outUser, font=font, fill=color)
			draw.text( ( ( (((692-w) * rightAlign  )+4) ,68+1)), outUser, font=font, fill=color)
			draw.text( ( ( (((692-w) * rightAlign  )+4+1) ,68-1)), outUser, font=font, fill=color)
			draw.text( ( ( (((692-w) * rightAlign  )+4+1) ,68)), outUser, font=font, fill=color)
			draw.text( ( ( (((692-w) * rightAlign  )+4+1) ,68+1)), outUser, font=font, fill=color)
			
			draw.text( ( ( (((692-w) * rightAlign  )+4) ,68)), outUser, font=font, fill=colorLotaBlue )
			oldText = text
			text = Image.new("RGBA",(W,(textHeight + 100)))
			text.paste(oldText, (0,0))
			text.paste(addtext, (0,textHeight))
			
			textHeight += 100
			scrollNeeded += 100
			chat.pop(min(chat,key=chat.get))
	except:
		pass
		
	if scrollNeeded > 150:#speed changes on a curve
		speed = scrollNeeded/37
	elif scrollNeeded > 90:
		speed = scrollNeeded / 25
	elif scrollNeeded > 0:
		speed = scrollNeeded / 17
	else:
		speed = 0
	if speed >3.5:
		speed = 3.5
		
	if len(scrollPause) > 270:
		scrollPause.remove(scrollPause[0])
	
	pausecheck = 0
	for check in scrollPause:
		pausecheck += check
		
	currentTime = time.time()
	if pausecheck > 857 and currentTime -lastPause > 6:
		lastPause = time.time()
		
	if currentTime - lastPause <3.3 and currentTime - lastPause >0:
		speed /=75.2
		
	#after a pause, increase speed (get messages which have already been read, out of view)
	#is this too unpredictable?
	
	speeds.append(speed)
	if len(speeds) > 120:
		speeds.remove(speeds[0])
	fSpeed = speed
	
	for speed in speeds:
		fSpeed = (fSpeed * .68) + (speed *.32) 
	speed = fSpeed
	
	scrollPause.append(speed)
	
	newFrame = Image.new("RGBA",(700,1000))
	height -= speed
	heyight = int(height)
	scrollNeeded -= speed
	newFrame.paste(text,(0,heyight))
	if len(chat) == 0:
		end += 1
	
	frame += 1
	
	diff = Image.new("RGBA",(700,1000), (0,0,0) )
	
	
	differ = ImageDraw.Draw(diff)
	differ.bitmap((0,0),newFrame)
	
	#newFrame.save(name,"png")
	pil_image = newFrame.convert('RGB') 
	opencvImage = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
	
	video.write(opencvImage)
	
	
	
	
	
	pil_image = diff.convert('RGB') 
	opencvImage = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
	
	#img1 = cv2.imread(opencvImage)
	
	video2.write(opencvImage)
	

cv2.destroyAllWindows()
video.release()
video2.release()