import os
from PIL import Image, ImageDraw
import scrapeImages

scrapeImages.run('doodle')
width = 4500
height = 5400
inputDirectory = 'art'
outputDirectory = 'upload'

for filename in os.listdir(inputDirectory):
    # get file
    art = Image.open(inputDirectory + '/' + filename)

    # resize file if necessary
    artW, artH = art.size
    halfWidth = width/2
    if(artW < halfWidth):
        art = art.resize((int(halfWidth),int(halfWidth/artW*artH)))
    artW, artH = art.size

    # create blank shirt and paste art
    shirt = Image.new('RGBA',(width, height))
    shirt.paste(art, (int((width-artW)/2),int((height-artH)/10)))

    # save shirt
    shirt.save(outputDirectory + '/' + os.path.splitext(filename)[0] + '_shirt.png', 'png')
