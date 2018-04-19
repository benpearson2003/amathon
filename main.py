import os
from PIL import Image, ImageDraw
import scrapeImages
import upload

keyword = 'reboot'
dailyLimit = 25
inputDirectory = 'art'
outputDirectory = 'upload'

if not os.path.exists(inputDirectory):
    os.makedirs(inputDirectory)

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

scrapeImages.run(keyword, inputDirectory, dailyLimit)
width = 4500
height = 5400

for filename in os.listdir(inputDirectory):
    # get file
    art = Image.open(inputDirectory + '/' + filename)

    # resize file if necessary
    artW, artH = art.size
    halfWidth = width/2
    if(artW < halfWidth):
        art = art.resize((int(halfWidth),int(halfWidth/artW*artH)))
    else:
        print ("didn't need resizing")
    artW, artH = art.size

    # create blank shirt and paste art
    shirt = Image.new('RGBA',(width, height))
    shirt.paste(art, (int((width-artW)/2),int((height-artH)/10)))

    # save shirt
    shirt.save(outputDirectory + '/' + os.path.splitext(filename)[0] + '_shirt.png', 'png')

upload.run(outputDirectory, dailyLimit)
os.rmtree(inputDirectory)
os.rmtree(outputDirectory)
