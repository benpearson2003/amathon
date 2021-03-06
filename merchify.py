import os
from PIL import Image, ImageDraw

def run(width, height, inputDirectory, outputDirectory):
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
