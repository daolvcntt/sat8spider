import re
import gzip
import shutil
import json
import pprint

# Get image from content
def getImageFromContent(content):
    matches = re.search('src="([^"]+)"', content)
    if matches != None :
        return matches.group(1)
    return None

# Make Gz file compress
def makeGzFile(filePath):
    filePathGzip = filePath + '.gz'
    with open(filePath , 'rb') as f_in, gzip.open(filePathGzip, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# Echo pretty print
def echo(data):
    pp = pprint.PrettyPrinter()
    pp.pprint(data)

# Parse json for query params
def parseJson4Params(data):
    jsonData = {}

    arrayStr = data.split("\n")

    for item in arrayStr:
        itemSplit = item.split(':')

        jsonData[str(itemSplit[0])] = str(itemSplit[1]).replace('\r', '')


    return jsonData
