import os
from PIL import Image, ImageDraw
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
        art = art.resize((halfWidth,int(float(halfWidth)/artW*artH)))
    artW, artH = art.size

    # create blank shirt and paste art
    shirt = Image.new('RGBA',(width, height))
    shirt.paste(art, ((width-artW)/2,(height-artH)/2))

    # save shirt
    shirt.save(outputDirectory + '/' + os.path.splitext(filename)[0] + '_shirt.png', 'png')
