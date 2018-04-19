import argparse
import os
from PIL import Image, ImageDraw
import merchify
import scrapeImages
import upload

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scrape", action="store_true")
parser.add_argument("-u", "--upload", action="store_true")
parser.add_argument("-k", "--keyword", type=str, help="to be searched")
parser.add_argument("-i", "--inputDirectory", type=str, help="to find artworks")
parser.add_argument("-o", "--outputDirectory", type=str, help="to save finished")
parser.add_argument("-l", "--limit", type=int, help="maximum uploads")
parser.add_argument("-w", "--width", type=int, help="width of finished")
parser.add_argument("-t", "--height", type=int, help="height of finished")
args = parser.parse_args()

keyword = args.keyword if args.keyword is not None else 'default'
dailyLimit = args.limit if args.limit is not None else 10
inputDirectory = args.inputDirectory if args.inputDirectory is not None else 'art'
outputDirectory = args.outputDirectory if args.outputDirectory is not None else 'upload'
width = args.width if args.width is not None else 4500
height = args.height if args.height is not None else 5400

if not os.path.exists(inputDirectory):
    os.makedirs(inputDirectory)

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

if args.scrape:
    scrapeImages.run(keyword, inputDirectory, dailyLimit)

merchify.run(width, height, inputDirectory, outputDirectory)

if args.upload:
    upload.run(outputDirectory, dailyLimit)
